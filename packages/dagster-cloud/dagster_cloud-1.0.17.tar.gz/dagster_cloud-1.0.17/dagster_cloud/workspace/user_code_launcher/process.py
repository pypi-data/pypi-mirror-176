import logging
import os
import sys
import threading
from collections import defaultdict
from typing import Collection, Dict, NamedTuple, Optional, Set, Tuple, Union

import dagster._seven as seven
from dagster import BoolSource, Field, IntSource
from dagster import _check as check
from dagster._core.errors import DagsterUserCodeUnreachableError
from dagster._core.types.loadable_target_origin import LoadableTargetOrigin
from dagster._grpc.client import DagsterGrpcClient, client_heartbeat_thread
from dagster._grpc.server import GrpcServerProcess
from dagster._serdes import ConfigurableClass, ConfigurableClassData
from dagster._serdes.ipc import open_ipc_subprocess
from dagster._utils import find_free_port, merge_dicts, safe_tempfile_path_unmanaged
from dagster_cloud.execution.cloud_run_launcher.process import CloudProcessRunLauncher
from dagster_cloud.pex.grpc import MultiPexGrpcClient
from dagster_cloud_cli.core.workspace import CodeDeploymentMetadata

from .user_code_launcher import (
    DEFAULT_SERVER_PROCESS_STARTUP_TIMEOUT,
    SHARED_USER_CODE_LAUNCHER_CONFIG,
    DagsterCloudGrpcServer,
    DagsterCloudUserCodeLauncher,
    ServerEndpoint,
)

CLEANUP_ZOMBIE_PROCESSES_INTERVAL = 5


class ProcessUserCodeEntry(
    NamedTuple(
        "_ProcessUserCodeEntry",
        [
            ("grpc_server_process", GrpcServerProcess),
            ("grpc_client", DagsterGrpcClient),
            ("heartbeat_shutdown_event", threading.Event),
            ("heartbeat_thread", threading.Thread),
        ],
    )
):
    def __new__(
        cls,
        grpc_server_process: GrpcServerProcess,
        grpc_client: DagsterGrpcClient,
        heartbeat_shutdown_event: threading.Event,
        heartbeat_thread: threading.Thread,
    ):
        return super(ProcessUserCodeEntry, cls).__new__(
            cls,
            check.inst_param(grpc_server_process, "grpc_server_process", GrpcServerProcess),
            check.inst_param(grpc_client, "grpc_client", DagsterGrpcClient),
            check.inst_param(heartbeat_shutdown_event, "heartbeat_shutdown_event", threading.Event),
            check.inst_param(heartbeat_thread, "heartbeat_thread", threading.Thread),
        )


class MultipexServerProcess:
    def __init__(
        self,
        metadata: CodeDeploymentMetadata,
    ):
        self.port = None
        self.socket = None

        if seven.IS_WINDOWS:
            self.port = find_free_port()
        else:
            self.socket = safe_tempfile_path_unmanaged()

        self.server_process = open_ipc_subprocess(
            metadata.get_multipex_server_command(self.port, self.socket)
        )

    @property
    def pid(self):
        return self.server_process.pid

    def wait(self, timeout=30):
        if self.server_process.poll() is None:
            seven.wait_for_process(self.server_process, timeout=timeout)


class MultipexUserCodeEntry(
    NamedTuple(
        "_MultipexUserCodeEntry",
        [
            ("grpc_server_process", MultipexServerProcess),
            ("grpc_client", MultiPexGrpcClient),
        ],
    )
):
    def __new__(
        cls,
        grpc_server_process: MultipexServerProcess,
        grpc_client: MultiPexGrpcClient,
    ):
        return super(MultipexUserCodeEntry, cls).__new__(
            cls,
            check.inst_param(grpc_server_process, "grpc_server_process", MultipexServerProcess),
            check.inst_param(grpc_client, "grpc_client", MultiPexGrpcClient),
        )


class ProcessUserCodeLauncher(DagsterCloudUserCodeLauncher, ConfigurableClass):
    def __init__(
        self,
        inst_data: Optional[ConfigurableClassData] = None,
        wait_for_processes: bool = False,
        **kwargs,
    ):
        self._inst_data = inst_data
        self._logger = logging.getLogger("dagster_cloud")

        # map from pid to server being spun up
        # (including old servers in the process of being shut down)
        self._process_entries: Dict[int, Union[ProcessUserCodeEntry, MultipexUserCodeEntry]] = {}

        # map from locationname to the pid(s) for that location-metadata combination.
        # Generally there should be only one pid per location unless an exception was raised partway
        # through an update
        self._active_pids: Dict[Tuple[str, str], Set[int]] = defaultdict(set)

        self._active_multipex_pids: Dict[Tuple[str, str], Set[int]] = defaultdict(set)

        self._heartbeat_ttl = 60
        self._wait_for_processes = wait_for_processes

        self._cleanup_zombies_shutdown_event = threading.Event()
        self._cleanup_zombies_thread = None

        self._run_launcher: Optional[CloudProcessRunLauncher] = None

        super(ProcessUserCodeLauncher, self).__init__(**kwargs)

    @property
    def requires_images(self) -> bool:
        return False

    def start(self, run_reconcile_thread=True):
        super().start(run_reconcile_thread=run_reconcile_thread)
        # TODO Identify if zombie processes are an issue on Windows and what
        # the proper way to clean them up is
        if sys.platform != "win32":
            self._cleanup_zombies_thread = threading.Thread(
                target=self._cleanup_zombie_processes,
                args=(self._cleanup_zombies_shutdown_event,),
                name="cleanup-zombie-processes",
                daemon=True,
            )
            self._cleanup_zombies_thread.start()

    def _cleanup_zombie_processes(self, shutdown_event):
        while True:
            shutdown_event.wait(CLEANUP_ZOMBIE_PROCESSES_INTERVAL)
            if shutdown_event.is_set():
                break

            # Clean up any child processes that have finished since last check
            while True:
                # This may need to be different on Windows because process groups are
                # handled differently.
                try:
                    pid, _exit_code = os.waitpid(0, os.WNOHANG)
                except ChildProcessError:
                    # Raised when there are no child processes
                    break

                if pid == 0:
                    break

    @property
    def inst_data(self) -> Optional[ConfigurableClassData]:
        return self._inst_data

    @classmethod
    def config_type(cls) -> Dict:
        return merge_dicts(
            {
                "server_process_startup_timeout": Field(
                    IntSource,
                    is_required=False,
                    default_value=DEFAULT_SERVER_PROCESS_STARTUP_TIMEOUT,
                    description="Timeout when waiting for a code server to be ready after it is created",
                ),
                "wait_for_processes": Field(
                    BoolSource,
                    is_required=False,
                    default_value=False,
                    description="When cleaning up the agent, wait for any subprocesses to "
                    "finish before shutting down. Generally only needed in tests/automation.",
                ),
            },
            SHARED_USER_CODE_LAUNCHER_CONFIG,
        )

    @staticmethod
    def from_config_value(
        inst_data: ConfigurableClassData, config_value: Dict
    ) -> "ProcessUserCodeLauncher":
        return ProcessUserCodeLauncher(inst_data=inst_data, **config_value)

    def _start_new_server_spinup(
        self, deployment_name: str, location_name: str, metadata: CodeDeploymentMetadata
    ) -> DagsterCloudGrpcServer:

        key = (deployment_name, location_name)

        server_process: Union[MultipexServerProcess, GrpcServerProcess]
        client: Union[MultiPexGrpcClient, DagsterGrpcClient]

        if metadata.pex_metadata:
            server_process = MultipexServerProcess(metadata)
            client = MultiPexGrpcClient(port=server_process.port, socket=server_process.socket)

            pid = server_process.pid

            self._process_entries[server_process.pid] = MultipexUserCodeEntry(
                server_process,
                client,
            )

            self._active_multipex_pids[key].add(pid)

        else:
            loadable_target_origin = self._get_loadable_target_origin(metadata)
            server_process = GrpcServerProcess(
                loadable_target_origin=loadable_target_origin,
                heartbeat=True,
                heartbeat_timeout=self._heartbeat_ttl,
                startup_timeout=self._server_process_startup_timeout,
                env={
                    **os.environ,
                    **metadata.get_grpc_inject_env_vars_cli_env(
                        deployment_name=deployment_name,
                        location_name=location_name,
                        instance=self._instance,
                    ),
                },
            )
            client = DagsterGrpcClient(
                port=server_process.port,
                socket=server_process.socket,
                host="localhost",
                use_ssl=False,
            )

            heartbeat_shutdown_event = threading.Event()
            heartbeat_thread = threading.Thread(
                target=client_heartbeat_thread,
                args=(client, heartbeat_shutdown_event),
            )
            heartbeat_thread.daemon = True
            heartbeat_thread.start()

            pid = server_process.pid

            self._process_entries[server_process.pid] = ProcessUserCodeEntry(
                server_process,
                client,
                heartbeat_shutdown_event,
                heartbeat_thread,
            )

            self._active_pids[key].add(pid)

        endpoint = ServerEndpoint(
            host="localhost",
            port=server_process.port,
            socket=server_process.socket,
        )

        return DagsterCloudGrpcServer(pid, endpoint, metadata)

    def _wait_for_new_server_ready(
        self,
        deployment_name: str,
        location_name: str,
        metadata: CodeDeploymentMetadata,
        server_handle: int,
        server_endpoint: ServerEndpoint,
    ) -> None:
        self._wait_for_dagster_server_process(
            client=server_endpoint.create_client(),
            timeout=self._server_process_startup_timeout,
        )

    def _get_loadable_target_origin(self, metadata: CodeDeploymentMetadata) -> LoadableTargetOrigin:
        return LoadableTargetOrigin(
            executable_path=metadata.executable_path if metadata.executable_path else "",
            python_file=metadata.python_file,
            package_name=metadata.package_name,
            module_name=metadata.module_name,
            working_directory=metadata.working_directory,
            attribute=metadata.attribute,
        )

    def _get_standalone_dagster_server_handles_for_location(
        self, deployment_name: str, location_name: str
    ) -> Collection[int]:
        return self._active_pids.get((deployment_name, location_name), set()).copy()

    def _get_multipex_server_handles_for_location(
        self, deployment_name: str, location_name: str
    ) -> Collection[int]:
        return self._active_multipex_pids.get((deployment_name, location_name), set()).copy()

    def _remove_server_handle(self, server_handle: int) -> None:
        pid = server_handle
        self._remove_pid(pid)

    def _remove_pid(self, pid):
        if pid in self._process_entries:
            process_entry = self._process_entries[pid]
            if isinstance(process_entry, ProcessUserCodeEntry):
                # Rely on heartbeat failure to eventually kill the process
                process_entry.heartbeat_shutdown_event.set()
                process_entry.heartbeat_thread.join()
            else:
                # multi-pex server processes don't yet have heartbeats, so just terminate
                # the multipex server process directly.
                process_entry.grpc_server_process.server_process.terminate()

            del self._process_entries[pid]

        for pids in self._active_pids.values():
            if pid in pids:
                pids.remove(pid)

        for pids in self._active_multipex_pids.values():
            if pid in pids:
                pids.remove(pid)

    def run_launcher(self) -> CloudProcessRunLauncher:
        if not self._run_launcher:
            self._run_launcher = CloudProcessRunLauncher()
            self._run_launcher.register_instance(self._instance)

        return self._run_launcher

    def _cleanup_servers(self):
        while len(self._process_entries):
            pid = next(iter(self._process_entries))
            process_entry = self._process_entries[pid]

            self._remove_pid(pid)
            if self._wait_for_processes:

                if isinstance(process_entry, ProcessUserCodeEntry):
                    try:
                        process_entry.grpc_client.shutdown_server()
                    except DagsterUserCodeUnreachableError:
                        # Server already shutdown
                        pass
                else:
                    process_entry.grpc_server_process.server_process.terminate()
                process_entry.grpc_server_process.wait()

    def __exit__(self, exception_type, exception_value, traceback):
        super().__exit__(exception_value, exception_value, traceback)

        if self._cleanup_zombies_thread:
            self._cleanup_zombies_shutdown_event.set()
            self._cleanup_zombies_thread.join()
