# pyright: reportMissingImports=false, reportMissingModuleSource=false

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel


class PlatformWheel(bdist_wheel):
    """Mark wheels containing libcue as platform-specific."""

    def finalize_options(self) -> None:
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self) -> tuple[str, str, str]:
        _, _, platform = super().get_tag()
        return 'py3', 'none', platform


setup(cmdclass={'bdist_wheel': PlatformWheel})
