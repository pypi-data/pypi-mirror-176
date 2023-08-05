import os
from typing import Any

import click

from anyscale.authenticate import get_auth_api_client
from anyscale.client.openapi_client.models.create_experimental_workspace import (
    CreateExperimentalWorkspace,
)
from anyscale.client.openapi_client.models.execute_shell_command_options import (
    ExecuteShellCommandOptions,
)
from anyscale.controllers.cluster_controller import ClusterController
from anyscale.controllers.workspace_controller import WorkspaceController
from anyscale.project import find_project_root
from anyscale.shared_anyscale_utils.utils.byod import BYODInfo
from anyscale.util import get_endpoint
from anyscale.workspace import get_workspace_root_or_throw, write_workspace_id_to_disk


ANYSCALE_WORKSPACES_SSH_OPTIONS = [
    "-o",
    "StrictHostKeyChecking=no",
    "-o",
    "UserKnownHostsFile=/dev/null",
    "-o",
    "IdentitiesOnly=yes",
]


@click.group("workspace", help="Interact with workspaces on Anyscale.", hidden=True)
def workspace_cli() -> None:
    pass


@workspace_cli.command(
    name="create", help="Create a workspace on Anyscale.", hidden=True
)
@click.option(
    "--name", "-n", required=True, help="Name of the workspace to create.",
)
@click.option("--project-id", required=True)
@click.option("--cloud-id", required=True)
@click.option("--cluster-env-build-id", required=False)
@click.option(
    "--docker", required=False, default=None, help=("Custom docker image URI."),
)
@click.option(
    "--python-version",
    required=False,
    default=None,
    help=("Python version for the custom docker image."),
)
@click.option(
    "--ray-version",
    required=False,
    default=None,
    help=("Ray version for the custom docker image."),
)
@click.option("--compute-config-id", required=True)
def create(
    name: str,
    project_id: str,
    cloud_id: str,
    cluster_env_build_id: str,
    docker: str,
    python_version: str,
    ray_version: str,
    compute_config_id: str,
) -> None:
    if cluster_env_build_id is None and docker is None:
        raise click.ClickException(
            "Please specify one of `--docker` or `--cluster-env-build-id`."
        )
    if docker is not None:
        if cluster_env_build_id is not None:
            raise click.ClickException(
                "`--cluster-env-build-id` and `--docker` cannot both be "
                "specified. Please only provide one of these two arguments."
            )

        if python_version is None:
            raise click.ClickException(
                "`--python-version` should be specified when `--docker` is used."
            )
        if ray_version is None:
            raise click.ClickException(
                "`--ray-version` should be specified when `--docker` is used."
            )
        # Create docker build_id
        cluster_env_build_id = BYODInfo(docker, python_version, ray_version).encode()

    auth_api_client = get_auth_api_client()
    api_client = auth_api_client.api_client
    api_client.create_workspace_api_v2_experimental_workspaces_post(
        CreateExperimentalWorkspace(
            name=name,
            project_id=project_id,
            cloud_id=cloud_id,
            compute_config_id=compute_config_id,
            cluster_environment_build_id=cluster_env_build_id,
        )
    )


@workspace_cli.command(
    name="start", help="Start an existing workspace on Anyscale.", hidden=True
)
@click.option(
    "--name", "-n", required=True, help="Name of existing workspace to start.",
)
def start(name: str) -> None:
    cluster_controller = ClusterController()

    workspace = get_workspace_from_name(name)
    cluster_id = workspace.cluster_id

    cluster_controller.start(
        cluster_name=None,
        cluster_id=cluster_id,
        cluster_env_name=None,
        docker=None,
        python_version=None,
        ray_version=None,
        cluster_compute_name=None,
        cluster_compute_file=None,
        cloud_name=None,
        idle_timeout=None,
        project_id=None,
        project_name=None,
        user_service_access=None,
    )


@workspace_cli.command(
    name="terminate", help="Terminate a workspace on Anyscale.", hidden=True
)
@click.option(
    "--name", "-n", required=True, help="Name of existing workspace to terminate.",
)
def terminate(name: str) -> None:
    cluster_controller = ClusterController()
    workspace = get_workspace_from_name(name)
    cluster_id = workspace.cluster_id

    cluster_controller.terminate(
        cluster_name=None, cluster_id=cluster_id, project_id=None, project_name=None,
    )


@workspace_cli.command(name="clone", help="Clone a workspace on Anyscale.")
@click.option(
    "--name",
    "-n",
    required=True,
    default=None,
    help="Name of existing workspace to clone.",
)
def clone(name: str) -> None:
    """
    Clone the workspace to a local dir whose name is the name of the workspace.
    """
    _check_local()

    workspace = get_workspace_from_name(name)
    dest = workspace.name
    workspace_controller = WorkspaceController()
    if os.path.exists(dest):
        _exit_error(
            f"Cannot clone workspace: already cloned locally at '{os.path.abspath(dest)}'."
        )
    workspace_controller.clone(workspace)
    os.chdir(dest)
    _do_pull(pull_git_state=True)


@workspace_cli.command(name="activate")
@click.argument(
    "name", required=True, default=None,
)
def activate(name: str) -> None:
    """Activate a workspace.

    If the current directory is already a part of a workspace, change the workspace.
    Else, setup a new workspace rooted at the current directory

    Args:
        name: Name of the workspace to activate.
    """
    _check_local()
    root_dir = find_project_root(os.getcwd())
    if not root_dir:
        raise click.ClickException(
            "Could not find the root workspace directory. Please first run `anyscale workspace clone`"
        )
    try:
        workspace = get_workspace_from_name(name)
        workspace_id = workspace.id
    except Exception:
        workpaces_url = get_endpoint("/workspaces")
        raise click.ClickException(
            f"There is no workspace {name} registered with Anyscale. You can view your workspaces here: {workpaces_url}"
        )
    write_workspace_id_to_disk(workspace_id, root_dir)


@workspace_cli.command(name="pull", help="Pull files from a workspace on Anyscale.")
@click.option(
    "--pull-git-state",
    required=False,
    is_flag=True,
    default=False,
    help="Also pull git state. This will add additional overhead.",
)
def pull(pull_git_state) -> None:
    _check_local()
    _check_workspace()
    _do_pull(pull_git_state)


@workspace_cli.command(name="push", help="Push files to a workspace on Anyscale.")
@click.option(
    "--push-git-state",
    required=False,
    is_flag=True,
    default=False,
    help="Also push git state. This is currently unoptimized and will be very slow.",
)
def push(push_git_state) -> None:
    _check_local()
    _check_workspace()
    _do_push(push_git_state)


@workspace_cli.command(
    name="run", help="Run a command in a workspace, syncing files first if needed."
)
@click.argument("command", required=True)
@click.option(
    "--web-terminal",
    "-w",
    required=False,
    is_flag=True,
    default=False,
    help="Run the command in the webterminal. Progress can be tracked from the UI.",
)
@click.option(
    "--as-job",
    "-j",
    required=False,
    is_flag=True,
    default=False,
    help="Run the command as a background job in a new cluster.",
)
@click.option(
    "--no-push",
    "-s",
    required=False,
    is_flag=True,
    default=False,
    help="Whether to skip pushing files prior to running the command.",
)
def run(command: str, web_terminal: bool, as_job: bool, no_push: bool,) -> None:
    _check_local()
    _check_workspace()
    if as_job:
        raise NotImplementedError("Running as a job isn't implemented yet.")
    workspace_controller = WorkspaceController()
    # Generally, we assume the user wants to run their command in the context of
    # their latest file changes.
    if not no_push:
        _do_push(push_git_state=False)
    workspace_controller = WorkspaceController()
    dir_name = workspace_controller.get_workspace_dir_name()
    if web_terminal:
        auth_api_client = get_auth_api_client()
        cluster_id = workspace_controller.get_activated_workspace().cluster_id
        results = auth_api_client.api_client.execute_shell_command_api_v2_sessions_session_id_execute_shell_command_post(
            cluster_id,
            ExecuteShellCommandOptions(shell_command=f"cd ~/{dir_name} && {command}"),
        )
        # TODO(ekl) show the workspace URL here and also block on completion.
        print()
        print(
            "Command submitted succcessfully! See the 'Command History' tab "
            f"of this workspace to view command status and output: {results}"
        )
        print()
    else:
        workspace_controller.run_cmd(
            ANYSCALE_WORKSPACES_SSH_OPTIONS, f"cd ~/{dir_name} && {command}",
        )


def _do_pull(pull_git_state):
    workspace_controller = WorkspaceController()
    dir_name = workspace_controller.get_workspace_dir_name()
    # Since workspaces store git objects in an EFS alternates dir, we have to force
    # a repack prior to pulling. Otherwise, the pulled git repo may not be fully
    # functional locally. A repack is expensive, but we assume pulls aren't frequent.
    if pull_git_state:
        workspace_controller.run_cmd(
            ANYSCALE_WORKSPACES_SSH_OPTIONS, f"cd ~/{dir_name} && git repack -a -d",
        )
    workspace_root = get_workspace_root_or_throw()
    workspace_controller.run_rsync(
        ANYSCALE_WORKSPACES_SSH_OPTIONS,
        workspace_root,
        down=True,
        rsync_filters=[".gitignore"],
        rsync_excludes=[".anyscale.yaml", ".git/objects/info/alternates"]
        + ([] if pull_git_state else [".git"]),
    )


def _do_push(push_git_state):
    workspace_controller = WorkspaceController()
    workspace_root = get_workspace_root_or_throw()
    workspace_controller.run_rsync(
        ANYSCALE_WORKSPACES_SSH_OPTIONS,
        workspace_root,
        down=False,
        rsync_filters=[".gitignore"],
        # TODO(ekl) to efficiently push the git state, we need to do this in two
        # phases: first sync the shared git objects to EFS, then sync non .git files.
        # Otherwise this will be very slow since our local git representation is
        # different from the remote one (has large .pack files).
        rsync_excludes=[".anyscale.yaml", ".git/objects/info/alternates"]
        + ([] if push_git_state else [".git"]),
    )


def _check_local():
    if "ANYSCALE_WORKING_DIR" in os.environ:
        _exit_error(
            "Error: This command cannot be run from inside an Anyscale cluster."
        )


def _check_workspace():
    if not os.path.exists(".anyscale.yaml"):
        _exit_error(
            "Error: This command must be run from the root of a cloned workspace directory."
        )


def get_workspace_from_name(name: str) -> Any:
    """Get a workspace from its name.
    """

    # Find the workspace by name
    auth_api_client = get_auth_api_client()
    results = auth_api_client.api_client.list_workspaces_api_v2_experimental_workspaces_get(
        name=name
    ).results
    if len(results) == 0:
        _exit_error("No workspace with name {} found.".format(name))
    elif len(results) > 1:
        _exit_error("Multiple workspaces with name {} found.".format(name))
    return results[0]


def _exit_error(msg: str) -> None:
    print()
    print(msg)
    exit(1)
