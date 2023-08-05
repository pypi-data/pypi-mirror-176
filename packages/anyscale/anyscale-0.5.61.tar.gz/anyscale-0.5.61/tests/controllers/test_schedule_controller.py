import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
from typing import List
from unittest.mock import Mock, patch

import click
import pytest
import yaml

from anyscale.controllers.job_controller import LogsLogger
from anyscale.controllers.schedule_controller import (
    assert_single_parameter,
    CreateScheduleConfig,
    load_yaml_file_with_overrides,
    ScheduleConfig,
    ScheduleController,
)


CONDA_DICT = {"dependencies": ["pip", {"pip": ["pip-install-test==0.5"]}]}
PIP_LIST = ["requests==1.0.0", "pip-install-test"]
ENV_VARS_DICT = {"TEST_ENV_VAR": "test_value"}


class FakeLogger(LogsLogger):
    logs: List[str] = []

    def open_block(self, *args, **kwargs,) -> None:
        pass

    def log(self, msg: str):
        self.logs.append(msg)
        print(msg)


@pytest.fixture
def test_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir)
        subdir = path / "subdir"
        subdir.mkdir(parents=True)
        requirements_file = subdir / "requirements.txt"
        with requirements_file.open(mode="w") as f:
            print("\n".join(PIP_LIST), file=f)

        good_conda_file = subdir / "good_conda_env.yaml"
        with good_conda_file.open(mode="w") as f:
            yaml.dump(CONDA_DICT, f)

        bad_conda_file = subdir / "bad_conda_env.yaml"
        with bad_conda_file.open(mode="w") as f:
            print("% this is not a YAML file %", file=f)

        old_dir = os.getcwd()
        os.chdir(tmp_dir)
        yield subdir, requirements_file, good_conda_file, bad_conda_file
        os.chdir(old_dir)


@pytest.fixture
def patch_jobs_anyscale_api_client(base_mock_anyscale_api_client: Mock):
    base_mock_anyscale_api_client.get_cluster_environment_build = Mock(
        return_value=Mock(result=Mock(status="succeeded"))
    )
    with patch.multiple(
        "anyscale.cluster_env",
        get_auth_api_client=Mock(
            return_value=Mock(anyscale_api_client=base_mock_anyscale_api_client)
        ),
    ):
        yield


s_config = {
    "name": "schedule",
    "entrypoint": "ls",
    "build_id": "build_id",
    "compute_config_id": "cc_id",
    "schedule": {"cron_expression": "ce"},
    "project_id": "prj_id",
    "runtime_env": {"pip": ["requests"]},
}


@pytest.fixture
def schedule_yaml_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir)
        subdir = path / "subdir"
        subdir.mkdir(parents=True)

        schedule_file = subdir / "schedule.yaml"
        with schedule_file.open(mode="w") as f:
            yaml.dump(s_config, f)

        old_dir = os.getcwd()
        os.chdir(tmp_dir)
        yield schedule_file
        os.chdir(old_dir)


def test_load_yaml_file(schedule_yaml_file, mock_auth_api_client):
    config = load_yaml_file_with_overrides(schedule_yaml_file, abc=123, name=None)
    assert config == {**s_config, "abc": 123}

    config = load_yaml_file_with_overrides(schedule_yaml_file, name="config_name")
    assert config == {**s_config, "name": "config_name"}


PIP_LIST = ["requests==1.0.0", "pip-install-test"]


def test_rewrite_re(mock_auth_api_client, patch_jobs_anyscale_api_client):
    with patch.multiple(
        "anyscale.controllers.schedule_controller",
        override_runtime_env_for_local_working_dir=Mock(
            return_value={"rewritten": True}
        ),
    ):
        config = CreateScheduleConfig(
            entrypoint="ls",
            build_id="123",
            compute_config_id="test",
            runtime_env={"pip": PIP_LIST},
            schedule=ScheduleConfig(cron_expression="* * * * *"),
            project_id="test_project_id",
        )
        assert config.runtime_env == {"rewritten": True}


def test_apply_schedule(
    schedule_yaml_file, mock_auth_api_client, patch_jobs_anyscale_api_client
):
    schedule_controller = ScheduleController()
    schedule_controller.api_client.get_compute_template_api_v2_compute_templates_template_id_get = Mock(
        return_value=Mock(result=Mock(archived_at=False))
    )
    with patch.multiple(
        "anyscale.controllers.schedule_controller",
        override_runtime_env_for_local_working_dir=Mock(
            return_value={"rewritten": True}
        ),
    ):
        schedule_controller.apply(schedule_yaml_file, "override_name")
        args = schedule_controller.api_client.create_or_update_job_api_v2_experimental_cron_jobs_put.call_args[
            0
        ][
            0
        ]
        assert args.to_dict() == {
            "config": {
                "build_id": "build_id",
                "compute_config": None,
                "compute_config_id": "cc_id",
                "entrypoint": "ls",
                "max_retries": 5,
                "runtime_env": {"rewritten": True},
                "runtime_env_config": None,
            },
            "description": None,
            "name": "override_name",
            "project_id": "prj_id",
            "schedule": {"cron_expression": "ce", "timezone": None},
        }


def test_assert_single_parameter_valid_cases(mock_auth_api_client):
    assert_single_parameter(name="name")
    assert_single_parameter(name="name", description=None, file=None)
    assert_single_parameter(name=None, description="description", file=None)
    assert_single_parameter(name=None, description=None, file="file")


def test_assert_single_parameter_invalid_cases(mock_auth_api_client):
    with pytest.raises(click.ClickException):
        assert_single_parameter()

    with pytest.raises(click.ClickException):
        assert_single_parameter(name="name", description="description")

    with pytest.raises(click.ClickException):
        assert_single_parameter(name=None, description=None)

    with pytest.raises(click.ClickException):
        assert_single_parameter(name="name", description="description", file=None)

    with pytest.raises(click.ClickException):
        assert_single_parameter(name="name", description=None, file="f")


def test_resolve_id(mock_auth_api_client):
    controller = ScheduleController()
    controller.schedule_api = Mock()
    controller.schedule_api.get.return_value = SimpleNamespace(id="returned_id")

    result = controller.resolve_file_name_or_id(id="id")
    assert result == "returned_id"


def test_resolve_id_fail(mock_auth_api_client):
    controller = ScheduleController()
    controller.schedule_api = Mock()

    def r(*args, **kwargs):
        raise Exception()

    controller.schedule_api.get = r

    with pytest.raises(click.ClickException):
        controller.resolve_file_name_or_id(id="id")


def test_resolve_name(mock_auth_api_client):
    controller = ScheduleController()
    controller.schedule_api = Mock()
    controller.schedule_api.get.return_value = SimpleNamespace(id="returned_id")
    controller.schedule_api.list.return_value = [
        SimpleNamespace(id="returned_id", name="schedule_1"),
        SimpleNamespace(id="returned_id_2", name="schedule_2"),
    ]
    result = controller.resolve_file_name_or_id(name="schedule_1")
    assert result == "returned_id"


def test_resolve_name_too_many(mock_auth_api_client):
    controller = ScheduleController()
    controller.schedule_api = Mock()
    controller.schedule_api.get.return_value = SimpleNamespace(id="returned_id")
    controller.schedule_api.list.return_value = [
        Mock(id="returned_id", name="schedule_1"),
        Mock(id="returned_id_2", name="schedule_1"),
    ]
    with pytest.raises(click.ClickException):
        controller.resolve_file_name_or_id(name="schedule_1")


def test_resolve_name_too_few(mock_auth_api_client):
    controller = ScheduleController()
    controller.schedule_api = Mock()
    controller.schedule_api.get.return_value = SimpleNamespace(id="returned_id")
    controller.schedule_api.list.return_value = []
    with pytest.raises(click.ClickException):
        controller.resolve_file_name_or_id(name="schedule_1")


def test_resolve_file(
    schedule_yaml_file, mock_auth_api_client, patch_jobs_anyscale_api_client
):
    schedule_controller = ScheduleController()
    schedule_controller.api_client.get_compute_template_api_v2_compute_templates_template_id_get = Mock(
        return_value=Mock(result=Mock(archived_at=False))
    )
    with patch.multiple(
        "anyscale.controllers.schedule_controller",
        override_runtime_env_for_local_working_dir=Mock(
            return_value={"rewritten": True}
        ),
    ):
        schedule_controller.schedule_api = Mock()
        schedule_controller.schedule_api.list.return_value = [
            SimpleNamespace(id="returned_id", name="schedule"),
        ]
        id = schedule_controller.resolve_file_name_or_id(
            schedule_config_file=schedule_yaml_file
        )
        assert id == "returned_id"


def test_pause(mock_auth_api_client):
    schedule_controller = ScheduleController()
    schedule_controller.schedule_api = Mock()
    schedule_controller.pause(id="id")
    schedule_controller.schedule_api.pause.assert_called_once()


def test_trigger(mock_auth_api_client):
    schedule_controller = ScheduleController()
    schedule_controller.schedule_api = Mock()
    schedule_controller.trigger(id="id")
    schedule_controller.schedule_api.trigger.assert_called_once()
