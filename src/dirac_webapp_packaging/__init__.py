import os
import shlex
import shutil
import subprocess

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

from setuptools import Command
# Note: distutils must be imported after setuptools
from distutils import log
from setuptools.command.develop import develop as _develop
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class build_extjs_sources(Command):
    user_options = []
    # _docker_image = "diracgrid/dirac-distribution:latest"
    _docker_image = "chrisburr/dirac-distribution:latest"
    _available_exes = [
        "docker",
        "singularity",
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_inputs(self):
        return []

    def get_outputs(self):
        return []

    def run(self):
        cmd = self._cmd
        log.info('> %r', shlex.join(cmd))
        subprocess.check_call(cmd)

    @property
    def _pkg_name(self):
        packages = [x for x in self.distribution.packages if "." not in x]
        if len(packages) != 1:
            raise NotImplementedError("Failed to find the package name")
        return packages[0]

    @property
    def _path(self):
        return os.path.abspath(os.getcwd())

    @property
    def _cmd(self):
        for self._exe in self._available_exes:
            full_exe = shutil.which(self._exe)
            if full_exe is not None:
                break
        else:
            raise NotImplementedError("Unable to find a suitable command")

        cmd = [full_exe]
        cmd += getattr(self, f"_{self._exe}_args")
        cmd += ["-D=/opt/src", f"-n={self._pkg_name}", "--py3-style"]
        return cmd

    @property
    def _docker_args(self):
        return [
            "run",
            "--rm",
            f"-v={self._path}:/opt",
            "-w=/opt",
            f"-u={os.getuid()}:{os.getgid()}",
            self._docker_image,
            "/dirac-webapp-compile.py",
        ]

    @property
    def _singularity_args(self):
        return [
            "run",
            "--writable",
            "--containall",
            "--bind",
            f"{self._path}:/opt",
            f"docker://{self._docker_image}",
            "/dirac-webapp-compile.py",
        ]


class develop(_develop):
    def run(self):
        self.run_command("build_extjs_sources")
        super().run()


class bdist_wheel(_bdist_wheel):
    def run(self):
        self.run_command("build_extjs_sources")
        super().run()


extjs_cmdclass = {
    "develop": develop,
    "bdist_wheel": bdist_wheel,
    "build_extjs_sources": build_extjs_sources,
}
