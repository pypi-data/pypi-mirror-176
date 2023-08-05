import sys
from time import sleep, time
from typing import Any, Dict, Optional, Union

from anyscale.api import configure_tcp_keepalive
from anyscale.sdk.anyscale_client.models.cluster_compute_config import ClusterComputeConfig
from anyscale.sdk.anyscale_client.models.create_cluster_compute import CreateClusterCompute
from anyscale.utils.runtime_env import upload_and_rewrite_working_dir
import anyscale.sdk.anyscale_client as anyscale_client
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi
from anyscale.version import __version__ as version
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
)
from anyscale.sdk.anyscale_client.models.create_byod_cluster_environment import (
    CreateBYODClusterEnvironment,
)
from anyscale.sdk.anyscale_client.models.cluster import Cluster
from anyscale.sdk.anyscale_client.models.cluster_environment_build import (
    ClusterEnvironmentBuild,
)
from anyscale.shared_anyscale_utils.headers import RequestHeaders
from anyscale.cli_logger import BlockLogger
from anyscale.util import get_endpoint
from anyscale.authenticate import AuthenticationBlock
from anyscale_client.models import ClusterEnvironmentBuildStatus
from anyscale.util import get_ray_and_py_version_for_default_cluster_env

def _upload_and_rewrite_working_dir_in_create_production_job(create_production_job):
    if create_production_job.config is not None:
        runtime_env = create_production_job.config.get("runtime_env")
        if runtime_env is not None:
            new_runtime_env = upload_and_rewrite_working_dir(runtime_env)
            create_production_job.config["runtime_env"] = new_runtime_env


def _is_create_byod_cluster_environment(obj: Any) -> bool:
    """
    Returns True if the object's config_json has "docker_image" set.
    The object can be either a dictionary or an object with "config_json"
    as an attribute.
    """
    config_json = None
    if isinstance(obj, dict):
        config_json = obj.get("config_json")
    else:
        config_json = getattr(obj, "config_json", None)
    return isinstance(config_json, dict) and "docker_image" in config_json

# Build states that are in progress
IN_PROGRESS_BUILD_STATES = [ClusterEnvironmentBuildStatus.IN_PROGRESS, ClusterEnvironmentBuildStatus.PENDING]

class AnyscaleSDK(DefaultApi):  # type: ignore
    def __init__(
        self, auth_token: Optional[str] = None, host: str = "https://api.anyscale.com",
    ):
        # Special handling for `console.` host names
        if host.startswith("https://console."):
            host = host.replace("console.", "api.", 1)

        # Adds base path "v0" for API endpoints
        endpoint_url = host.rstrip("/") + "/v0"
        configuration = anyscale_client.Configuration(host=endpoint_url)
        configuration.connection_pool_maxsize = 100
        if auth_token is None:
            auth_token, _ = AuthenticationBlock._load_credentials()
        api_client = anyscale_client.ApiClient(
            configuration, cookie=f"cli_token={auth_token}"
        )
        configure_tcp_keepalive(api_client)
        api_client.set_default_header(RequestHeaders.CLIENT, "SDK")
        api_client.set_default_header(RequestHeaders.CLIENT_VERSION, version)

        self.log: BlockLogger = BlockLogger()

        super(AnyscaleSDK, self).__init__(api_client)

    def build_cluster_environment(
        self,
        create_cluster_environment: Union[CreateClusterEnvironment, CreateBYODClusterEnvironment],
        poll_rate_seconds: int = 15,
        timeout_seconds: Optional[int] = None,
        log_output: bool = False,
    ) -> ClusterEnvironmentBuild:
        """
        Creates a new Cluster Environment and waits for build to complete.

        If a Cluster Environment with the same name already exists, this will
        create an updated build of that environment.

        Args:
            create_cluster_environment - CreateClusterEnvironment object
            poll_rate_seconds - seconds to wait when polling build operation status; defaults to 15
            timeout_seconds - maximum number of seconds to wait for build operation to complete before timing out; defaults to no timeout

        Returns:
            Newly created ClusterEnvironmentBuild object

        Raises:
            Exception if building Cluster Environment failed or timed out
        """

        self.log.log_output = log_output
        cluster_environments = self.search_cluster_environments(
            {
                "name": {"equals": create_cluster_environment.name},
                "paging": {"count": 1},
            }
        ).results

        if not cluster_environments:
            self.log.info(
                f"Creating new cluster environment {create_cluster_environment.name}"
            )
            if _is_create_byod_cluster_environment(create_cluster_environment):
                cluster_environment = self.create_byod_cluster_environment(
                    create_cluster_environment
                ).result
            else:
                cluster_environment = self.create_cluster_environment(
                    create_cluster_environment
                ).result
            build = self.list_cluster_environment_builds(
                cluster_environment.id
            ).results[0]
            build_operation_id = build.id
        else:
            self.log.info(
                f"Building new revision of cluster environment {create_cluster_environment.name}"
            )
            cluster_environment = cluster_environments[0]
            if _is_create_byod_cluster_environment(create_cluster_environment):
                build = self.create_byod_cluster_environment_build(
                    {
                        "cluster_environment_id": cluster_environment.id,
                        "config_json": create_cluster_environment.config_json,
                    }
                ).result
            else:
                build = self.create_cluster_environment_build(
                    {
                        "cluster_environment_id": cluster_environment.id,
                        "config_json": create_cluster_environment.config_json,
                    }
                ).result
            build_operation_id = build.id

        return self.wait_for_cluster_environment_build_operation(
            build_operation_id, poll_rate_seconds, timeout_seconds, log_output
        )

    def wait_for_cluster_environment_build_operation(
        self,
        operation_id: str,
        poll_rate_seconds: int = 15,
        timeout_seconds: Optional[int] = None,
        log_output: bool = False,
    ) -> ClusterEnvironmentBuild:
        """
        Waits for a Cluster Environment Build operation to complete.

        Args:
            operation_id - ID of the Cluster Environment Build operation
            poll_rate_seconds - seconds to wait when polling build operation status; defaults to 15
            timeout_seconds - maximum number of seconds to wait for build operation to complete before timing out; defaults to no timeout

        Returns:
            ClusterEnvironmentBuild object

        Raises:
            Exception if building Cluster Environment fails or times out.
        """

        self.log.log_output = log_output
        timeout = time() + timeout_seconds if timeout_seconds else None

        operation = self.get_build(operation_id)
        url = get_endpoint(
            f"configurations/app-config-details/{operation_id}"
        )
        self.log.info(
            f"Waiting for cluster environment to build. View progress at {url}."
        )
        self.log.info(f"status: {operation.result.status}")
        while operation.result.status in IN_PROGRESS_BUILD_STATES:
            if timeout and time() > timeout:
                raise Exception(
                    f"Building Cluster Environment timed out after {timeout_seconds} seconds."
                )

            sleep(poll_rate_seconds)
            self.log.info(f"status: {operation.result.status}")
            operation = self.get_build(
                operation_id
            )
        if operation.result.status != ClusterEnvironmentBuildStatus.SUCCEEDED:
            raise Exception(
                f"Failed to build Cluster Environment, you can check the full logs at: {url}."
            )
        else:
            self.log.info("Cluster environment successfully finished building.")
            return self.get_build(
                operation_id
            ).result

    def launch_cluster(
        self,
        project_id: Optional[str],
        cluster_name: str,
        cluster_environment_build_id: Optional[str] = None,
        cluster_compute_id: Optional[str] = None,
        poll_rate_seconds: int = 15,
        timeout_seconds: Optional[int] = None,
        idle_timeout_minutes: Optional[int] = None,
        cluster_compute_config: Optional[ClusterComputeConfig] = None,
    ) -> Cluster:
        """
        Starts a Cluster in the specified Project.
        If a Cluster with the specified name already exists, we will update that Cluster.
        Otherwise, a new Cluster will be created.

        Args:
            project_id - ID of the Project the Cluster belongs to or None to launch cluster without a project.
            cluster_name - Name of the Cluster
            cluster_environment_build_id - Cluster Environment Build to start this Cluster with
                                           If none, uses a default cluster_environment_build
            cluster_compute_id - Cluster Compute to start this Cluster with
                                 If none, it checks if `cluster_compute_config` is specified.
                                 If `cluster_compute_config` is none, it uses a default cluster_compute.
            poll_rate_seconds - seconds to wait when polling Cluster operation status; defaults to 15
            timeout_seconds - maximum number of seconds to wait for Cluster operation to complete before timing out; defaults to no timeout
            idle_timeout_minutes - Idle timeout (in minutes), after which the Cluster is terminated
            cluster_compute_config - One-off Cluster Compute that this Cluster will use.

        Returns:
            Cluster object

        Raises:
            Exception if starting Cluster fails or times out
        """

        if not project_id:
            default_project = self.get_default_project().result
            search_project_id = default_project.id
        else:
            search_project_id = project_id

        clusters = self.search_clusters(
            {"project_id": search_project_id, "name": {"equals": cluster_name}}
        ).results

        if clusters:
            cluster = clusters[0]
        else:
            if not cluster_environment_build_id:
                # Use default cluster environment build when starting cluster without specifying an id
                ray_version, py_version = get_ray_and_py_version_for_default_cluster_env()
                cluster_environment_build_id = self.get_default_cluster_environment_build(
                    f"py{py_version}", ray_version
                ).result.id

            if not cluster_compute_id:
                if cluster_compute_config:
                    cluster_compute_id = self.create_cluster_compute(CreateClusterCompute(config=cluster_compute_config, anonymous=True)).result.id
                else:
                    # Use default cluster compute when starting cluster without specifying an id
                    cluster_compute_id = self.get_default_cluster_compute().result.id

            create_cluster_payload: Dict[str, Any] = {
                "name": cluster_name,
                "project_id": project_id,
                "cluster_environment_build_id": cluster_environment_build_id,
                "cluster_compute_id": cluster_compute_id,
            }
            if idle_timeout_minutes:
                create_cluster_payload["idle_timeout_minutes"] = idle_timeout_minutes

            cluster = self.create_cluster(create_cluster_payload).result

        start_operation = self.start_cluster(
            cluster.id,
            {
                "cluster_environment_build_id": cluster_environment_build_id,
                "cluster_compute_id": cluster_compute_id,
            },
        ).result

        return self.wait_for_cluster_operation(
            start_operation.id, poll_rate_seconds, timeout_seconds
        )

    def launch_cluster_with_new_cluster_environment(
        self,
        project_id: Optional[str],
        cluster_name: str,
        create_cluster_environment: CreateClusterEnvironment,
        cluster_compute_id: Optional[str] = None,
        poll_rate_seconds: int = 15,
        timeout_seconds: Optional[int] = None,
        idle_timeout_minutes: Optional[int] = None,
        cluster_compute_config: Optional[ClusterComputeConfig] = None,
    ) -> Cluster:
        """
        Builds a new Cluster Environment, then starts a Cluster in the specified Project with the new build.
        If a Cluster with the specified name already exists, we will update that Cluster.
        Otherwise, a new Cluster will be created.

        Args:
            project_id - ID of the Project the Cluster belongs to or None to launch a cluster without a project.
            cluster_name - Name of the Cluster
            create_cluster_environment - CreateClusterEnvironment object
            cluster_compute_id - Cluster Compute to start this Cluster with
                                 If none, it checks if `cluster_compute_config` is specified.
                                 If `cluster_compute_config` is  none, it uses a default cluster_compute.
            poll_rate_seconds - seconds to wait when polling for operations; defaults to 15
            timeout_seconds - maximum number of seconds to wait for each operation to complete before timing out; defaults to no timeout
            idle_timeout_minutes - Idle timeout (in minutes), after which the Cluster is terminated
            cluster_compute_config - One-off Cluster Compute that this Cluster will use.

        Returns:
            Cluster object

        Raises:
            Exception if building the new Cluster Environment fails or starting the Cluster fails.
        """

        cluster_environment_build = self.build_cluster_environment(
            create_cluster_environment, poll_rate_seconds, timeout_seconds
        )

        return self.launch_cluster(
            project_id,
            cluster_name,
            cluster_environment_build.id,
            cluster_compute_id,
            poll_rate_seconds,
            timeout_seconds,
            idle_timeout_minutes,
            cluster_compute_config,
        )

    def wait_for_cluster_operation(
        self,
        operation_id: str,
        poll_rate_seconds: int = 15,
        timeout_seconds: Optional[int] = None,
    ) -> Cluster:
        """
        Waits for a Cluster operation to complete, most commonly used when starting, terminating, or updating a Cluster.

        Args:
            operation_id - ID of the Cluster Operation
            poll_rate_seconds - seconds to wait when polling build operation status; defaults to 15
            timeout_seconds - maximum number of seconds to wait for build operation to complete before timing out; defaults to no timeout

        Returns:
            Cluster object when the operation completes successfully

        Raises:
            Exception if building Cluster operation fails or times out
        """

        timeout = time() + timeout_seconds if timeout_seconds else None

        operation = self.get_cluster_operation(operation_id).result
        while not operation.completed:
            if timeout and time() > timeout:
                raise Exception(
                    f"Cluster start up timed out after {timeout_seconds} seconds."
                )

            sleep(poll_rate_seconds)
            operation = self.get_cluster_operation(operation_id).result

        if operation.result.error:
            raise Exception("Failed to start Cluster", operation.result.error)
        else:
            return self.get_cluster(operation.cluster_id).result

    def fetch_actor_logs(self, actor_id: str) -> str:
        """
        Retrieves logs for an Actor.
        This function may take several minutes if the Cluster this Actor ran on has been terminated.

        Args:
            actor_id - ID of the Actor

        Returns
            Log output for the Actor as a string

        Raises
            Exception if we fail to fetch logs
        """

        # Timeout in 5 minutes
        timeout = time() + 300

        logs = self.get_actor_logs(actor_id).result
        while not logs.ready:
            if time() > timeout:
                raise Exception(f"Failed to get logs from Actor {actor_id}")

            sleep(15)
            logs = self.get_actor_logs(actor_id).result

        return str(logs.logs)

    def fetch_job_logs(self, job_id: str) -> str:
        """
        Retrieves logs for a Ray Job or Interactive Session.
        This function may take several minutes if the Cluster this Job ran on has been terminated.

        Args:
            job_id - ID of the Job

        Returns
            Log output for the Job as a string

        Raises
            Exception if we fail to fetch logs
        """

        # Timeout in 5 minutes
        timeout = time() + 300

        logs = self.get_job_logs(job_id).result

        while not logs.ready:
            if time() > timeout:
                raise Exception(f"Failed to get logs from Job {job_id}")

            sleep(15)
            logs = self.get_job_logs(job_id).result

        return str(logs.logs)

    def get_production_job_logs(self, job_id: str) -> str:
        """
        Retrieves logs for latest run of a Production Job.

        Args:
            job_id - ID of the Job

        Returns
            Log output for the Job as a string

        Raises
            Exception if we fail to fetch logs
        """

        latest_job_run_id = self.get_production_job(
            production_job_id=job_id
        ).result.last_job_run_id
        if not latest_job_run_id:
            raise Exception(f"Production Job {job_id} does not have a job run.")

        return self.get_job_logs(latest_job_run_id)

    def fetch_production_job_logs(self, job_id: str) -> str:
        """
        Retrieves logs for latest run of a Production Job.
        Waits 5 min for logs to be ready.
        This function may take several minutes if the Cluster this Job ran on has been terminated.

        Args:
            job_id - ID of the Job

        Returns
            Log output for the Job as a string

        Raises
            Exception if we fail to fetch logs
        """

        # Timeout in 5 minutes
        timeout = time() + 300

        logs = self.get_production_job_logs(job_id).result

        while not logs.ready:
            if time() > timeout:
                raise Exception(f"Failed to get logs from Job {job_id}")

            sleep(15)
            logs = self.get_production_job_logs(job_id).result

        return str(logs.logs)

    def create_job(self, create_production_job, **kwargs):
        _upload_and_rewrite_working_dir_in_create_production_job(create_production_job)
        return super().create_job(create_production_job, **kwargs)

    def create_service(self, create_production_service, **kwargs):
        _upload_and_rewrite_working_dir_in_create_production_job(
            create_production_service
        )
        return super().create_service(create_production_service, **kwargs)

    def apply_service(self, create_production_service, **kwargs):
        _upload_and_rewrite_working_dir_in_create_production_job(
            create_production_service
        )
        return super().apply_service(create_production_service, **kwargs)

    def get_cluster_token(self, project_id: str, cluster_name: str) -> str:
        """
        Retrieves cluster token for a Cluster.
        This cluster token can be used to authenticate Anyscale services (eg: serve, jupyter, grafana)

        Args:
            project_id - ID of the Project the Cluster belongs to
            cluster_name - Name of the Cluster

        Returns
            string containing cluster token

        Raises
            Exception if invalid cluster name
        """
        clusters = self.search_clusters(
            {"project_id": project_id, "name": {"equals": cluster_name}}
        ).results

        if clusters:
            cluster = clusters[0]
        else:
            raise Exception(
                (
                    f"Cluster named {cluster_name} does not exist in Project {project_id} "
                    "or this user does not have read permissions for it."
                )
            )
        cluster_token = cluster.access_token
        return cluster_token
