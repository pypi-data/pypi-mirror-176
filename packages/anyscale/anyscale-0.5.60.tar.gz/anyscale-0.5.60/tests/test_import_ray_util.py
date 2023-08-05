import click
import pytest

from anyscale.utils.import_ray_util import try_import_ray


def test_try_import_ray():
    # This test verifies  that try_import_ray() runs successfully
    # if Ray is installed and returns the same version of Ray as
    # the local import statement. If Ray is not installed, try_import_ray()
    # should raise an error.

    # TODO(nikita): This test should be run in an environment that has Ray
    # installed, and one that doesn't have Ray installed. The
    # `import ray` statement inside the method cannot be mocked.
    try:
        import ray

        assert try_import_ray() == ray
    except ImportError:
        with pytest.raises(click.ClickException):
            try_import_ray()
