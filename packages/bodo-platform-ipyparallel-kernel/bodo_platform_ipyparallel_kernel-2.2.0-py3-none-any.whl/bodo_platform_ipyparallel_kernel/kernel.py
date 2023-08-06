import json
from signal import SIGKILL
from ipykernel.ipkernel import IPythonKernel
import ipyparallel as ipp
from ipyparallel.client.magics import ParallelMagics

from .platform_hostfile_update import update_hostfile
from .utils import BColor, colorize_output

IPYPARALLEL_LINE_MAGICS = ("px", "autopx", "pxconfig", "pxresult")
IPYPARALLEL_CELL_MAGICS = ("px",)
BODO_PLATFORM_CUSTOM_LINE_MAGICS = (
    "%pconda",
    "%ppip",
    "%psh",
    "%setup_adls",
    "%update_hostfile",
)

IPYPARALLEL_MAGICS = tuple(
    [f"%{m}" for m in IPYPARALLEL_LINE_MAGICS]
    + [f"%%{m}" for m in IPYPARALLEL_CELL_MAGICS]
)

# Should be kept in sync with https://github.com/Bodo-inc/bodo-platform-jupyterlab-extension/blob/master/src/types.ts
class SupportedLanguages:
    PYTHON = "Python"
    SQL = "SQL"


class IPyParallelKernel(IPythonKernel):
    banner = "IPyParallel Kernel"

    def start(self):
        super().start()
        self.ipyparallel_cluster_started = False
        self.ipyparallel_cluster = None

    def _is_autopx_enabled(self):
        try:
            return self.shell.magics_manager.registry[ParallelMagics.__name__]._autopx
        except:
            return False

    def ipyparallel_magics_already_registered(self) -> bool:
        # Check if any IPyParallel magics are already registered
        return any(
            [
                x in self.shell.magics_manager.magics["line"]
                for x in IPYPARALLEL_LINE_MAGICS
            ]
            + [
                x in self.shell.magics_manager.magics["cell"]
                for x in IPYPARALLEL_CELL_MAGICS
            ]
        )

    def start_ipyparallel_cluster(self):
        if not self.ipyparallel_cluster_started:
            self.log.info("Updating Hostfile...")
            update_hostfile(self.log)

            self.log.info("Starting IPyParallel Cluster...")

            try:
                self.ipyparallel_cluster = ipp.Cluster(
                    engines="bodo"
                )  # Config is taken from ipcluster_config.py
                self.ipyparallel_rc = self.ipyparallel_cluster.start_and_connect_sync()
                self.ipyparallel_view = self.ipyparallel_rc.broadcast_view()
                self.ipyparallel_view.block = True
                self.ipyparallel_view.activate()
            except Exception as e:
                self.log.error(
                    "Something went wrong while trying to start the IPyParallel cluster..."
                )
                self.log.error(f"Error: {e}")
                self.log.info("Shutting Cluster down...")
                # Cluster might have been started, if so then stop it and remove any
                # lingering processes
                if self.ipyparallel_view is not None:
                    # In some cases just stop_cluster_sync left hanging engine processes so view.shutdown was added
                    self.ipyparallel_view.shutdown(hub=True)
                if self.ipyparallel_cluster is not None:
                    self.ipyparallel_cluster.stop_cluster_sync()
                raise e
            else:
                self.ipyparallel_cluster_started = True

    def _log_message(self, message: str):
        stream_content = {"name": "stderr", "text": message}
        self.send_response(self.iopub_socket, "stream", stream_content)

    async def do_execute(
        self,
        code: str,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        # If code is run without parallel magics, warn the user
        if not self._is_autopx_enabled() and not code.startswith(
            (*IPYPARALLEL_MAGICS, *BODO_PLATFORM_CUSTOM_LINE_MAGICS)
        ):
            message = colorize_output(
                BColor.WARNING,
                "No IPyParallel Magics detected. For parallel execution, please use an IPyParallel magic such as %%px or %autopx.",
            )
            self._log_message(message)

        # Start the IPyParallel cluster if any IPyParallel
        # magic is used
        if (
            code.startswith(IPYPARALLEL_MAGICS)
            # If magics are already registered, that means user has started an
            # IPyParallel cluster manually, so we shouldn't start one ourselves.
            # This lets users use this kernel as a direct replacement for a regular
            # kernel.
            and not self.ipyparallel_magics_already_registered()
        ):
            try:
                self.start_ipyparallel_cluster()
            except Exception:
                # Don't run any code since cluster creation failed
                code = "pass"

        # If the engines are not running, e.g. they were previously started but killed,
        # and code starts with "px" or "autopx", rather than executing the code,
        # we throw an error
        if self.ipyparallel_cluster_started and (
            self._is_autopx_enabled() or code.startswith(IPYPARALLEL_MAGICS)
        ):
            # If engines are not running, e.g. they previously errored out with an exit code, prompt user to restart the kernel and return
            # We use a try-except block here to make sure code doest throw an error for instances when
            # ipyparallel_cluster does not have a property engine_set. The other alternative would be to use a getter
            try:
                if (
                    not self.ipyparallel_cluster.engine_set.running
                    # still allow users to disable autopx
                    and not (code.startswith("%autopx") and self._is_autopx_enabled())
                    # still allow users to run %pxresult
                    and not code.startswith("%pxresult")
                ):
                    message = colorize_output(
                        BColor.FAIL,
                        "IPyParallel Cluster engines previously exited with an error. Please restart the kernel and try again",
                    )
                    self._log_message(message)
                    return
            except:
                pass

        # If autopx is enabled show users a warning and replace code with "pass"
        if self._is_autopx_enabled() and code.startswith((f"%px", f"%%px")):
            message = colorize_output(
                BColor.WARNING,
                "Using px while autopx is enabled is not supported.",
            )
            self._log_message(message)
            code = "pass"

        return await super().do_execute(
            code=code,
            silent=silent,
            store_history=store_history,
            user_expressions=user_expressions,
            allow_stdin=allow_stdin,
        )

    async def stop_ipyparallel_cluster(self):
        if self.ipyparallel_cluster_started:
            self.log.info("Stopping IPyParallel Cluster...")

            # If a MPI process is hanging/waiting for other processes
            # the normal IPP shutdown process leaves zombie engines
            # which can create OOM issues.
            # Sending SIGKILL to the engines ensures the processes are
            # stopped and their resources are released.
            # passing signal's int value instead of signal object since Slurm launcher
            # cannot handle objects (passed to scancel).
            await self.ipyparallel_cluster.signal_engines(SIGKILL.value)
            # Stop the controller separately since the engines should be
            # removed already.
            await self.ipyparallel_cluster.stop_controller()

            # If a cluster is left in a broken state the cluster file
            # isn't always removed so manually remove it
            self.ipyparallel_cluster.remove_cluster_file()

            try:
                # Just in case the above methods don't work
                self.ipyparallel_cluster.stop_cluster_sync()
            except FileNotFoundError:
                # Cluster.stop_engines will throw FileNotFoundError if logs are already removed.
                # Stop_cluster_sync calls cluster.stop_engines.
                pass

    async def do_shutdown(self, restart):
        await self.stop_ipyparallel_cluster()
        return super().do_shutdown(restart)

    async def execute_request(self, stream, ident, parent):
        """
        Modify the input code for handling the SQL language type
        This is where we have access to the metadata
        to get the required information, like the selected language,
        selected catalog, etc.
        In case of SQL, we add the `%%sql` magic. We also add `%%px`
        if autopx is not enabled.
        Else we pass it through as is.
        """
        lang = parent.get("metadata", {}).get("lang", SupportedLanguages.PYTHON)
        if lang == SupportedLanguages.SQL:
            catalog = parent.get("metadata", {}).get("bodo-catalog")
            # Handle the case where 'catalog' is "" or None. The "" handling is
            # essential since json.loads("") would error out.
            if not catalog:
                catalog = "{}"
            catalog_name = json.loads(catalog).get("name")
            if not catalog_name:
                # If catalog_name is not specified, the `%%sql` magic would complain,
                # but without a very intuitive error for users. So we show a warning
                # and modify the code to be "pass" so there's no side effects.
                message = colorize_output(
                    BColor.WARNING,
                    "Please select a catalog before executing a SQL cell.",
                )
                self._log_message(message)
                # One side effect is that `do_execute` will log a message saying that
                # no IPyParallel magics were detected, which might confuse the users.
                # TODO Make sure this works as expected after the Parallel-Python changes
                # (which gets rid of that message).
                parent["content"]["code"] = "pass"

            else:
                # We store the output in `LAST_SQL_OUTPUT`.
                # Users can choose to take this and store it in some other
                # variable if they want.
                # We don't create a unique/random name every time since
                # that would fill up the memory. This way, if the user
                # doesn't want to keep the output around, python
                # garbage collection will get rid of it.
                parent["content"]["code"] = (
                    (f"%%px\n" if not self._is_autopx_enabled() else "")
                    + f"%%sql --catalog_name {catalog_name} --output LAST_SQL_OUTPUT\n"
                    + parent["content"]["code"]
                )

        return await super().execute_request(stream, ident, parent)
