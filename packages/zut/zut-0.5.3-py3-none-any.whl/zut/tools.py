from __future__ import annotations
import os, shutil, logging, subprocess, sys, re
from pathlib import Path
from argparse import ArgumentParser
from glob import glob
from .network import get_configured_proxy_url
from .commands import command, add_object_commands, exec_command

try:
    from .credentials import CredentialsMixin
except ModuleNotFoundError:
    class CredentialsMixin:
        pass


logger = logging.getLogger(__name__)


CLEAN_DEFAULT_PATHS = [
    "build",
    "dist",
    ".eggs",
    "**/__pycache__",
    "**/*.egg-info",
]


LSO_DEFAULT_EXCLUDES = [
    ".venv",
    "node_modules",
]


def _clean_add_arguments(parser):
    parser.add_argument("--dry-run", "-n", action="store_true", help="do not actually perform any deletion: print what would be done")

@command(_clean_add_arguments)
def clean(paths: list[str] = None, dry_run: bool = False):
    """
    Delete generated files.
    """
    if not paths:
        paths = CLEAN_DEFAULT_PATHS

    for globpath in paths:
        for path in glob(globpath, recursive=True):
            if dry_run:
                print("would clean", path)
            else:
                print("clean", path)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.unlink(path)


def lso(excludes: list[str] = None):
    """
    Show list of files not tacken into account by git.
    """
    if not excludes:
        excludes = LSO_DEFAULT_EXCLUDES

    command = ["git", "ls-files", "-o"]
    for exclude in excludes:
        command += ["-x", exclude]
    subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr)


class CleanMixin:
    clean_paths: list[str]

    @command(doc=clean.__doc__, add_arguments=_clean_add_arguments)
    def clean(self, dry_run: bool = False):
        clean(paths=getattr(self, 'clean_paths', None), dry_run=dry_run)


class LsoMixin:
    lso_excludes: list[str]

    @command(doc=lso.__doc__)
    def lso(self):
        lso(excludes=getattr(self, 'lso_excludes', None))


class Dist:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
    
        m = re.match(r"^(?P<package>.+)\-(?P<version>[^\-]+)\-(?P<python_tag>[^\-]+)\-(?P<abi_tag>[^\-]+)\-(?P<platform_tag>[^\-]+).whl$", path.name)
        if not m:
            self.package = None
            self.version = None
            self.python_tag = None
            self.abi_tag = None
            self.platform_tag = None
        
        else:
            self.package = m.group("package")
            self.version = m.group("version")
            self.python_tag = m.group("python_tag")
            self.abi_tag = m.group("abi_tag")
            self.platform_tag = m.group("platform_tag")

    @property
    def tag(self):
        if self.python_tag is None or self.abi_tag is None or self.platform_tag is None:
            return None
        return f"{self.python_tag}-{self.abi_tag}-{self.platform_tag}"

    def __str__(self):
        return self.path.as_posix()


class BuildMixin:
    twine_cert: Path|str
    twine_proxy: str
    build_skip_test = False
    upload_repository: str
    checkbuild_package: str
    checkbuild_version = re.compile(r"^\d+\.\d+\.\d+$")
    checkbuild_python_tag = "py3"
    checkbuild_abi_tag = "none"
    checkbuild_platform_tag = "any"
    test_args: list[str]

    def unittest(self):
        """
        Perform unit tests.
        """
        logger.info(f"run unit tests")
        cp = subprocess.run([sys.executable, "-m", "unittest"] + getattr(self, "test_args", []), text=True, stdout=sys.stdout, stderr=sys.stderr)

        if cp.returncode != 0:
            logger.error(f"tests fail")
            return False

        return True


    def _get_dists(self) -> list[Dist]:
        return [Dist(path) for path in Path.cwd().joinpath("dist").iterdir()]


    def checkbuild(self):
        """
        Check the wheel in `dist` directory.
        """

        # check generated wheel
        dists = self._get_dists()
        if len(dists) == 0:
            logger.error(f"no file generated in dist")
            return False

        ok = True
        for dist in dists:
            if not dist.package:
                logger.error(f"invalid file name format: {dist.name}")
                ok = False
                continue

            if hasattr(self, "checkbuild_package") and dist.package != self.checkbuild_package:
                logger.error(f"invalid wheel package \"{dist.package}\" for {dist.name} (expected \"{self.checkbuild_package}\")")
                ok = False
            elif not self.checkbuild_version.match(dist.version):
                logger.error(f"invalid wheel version \"{dist.version}\" for {dist.name} (expected pattern {self.checkbuild_version.pattern})")
                ok = False
            elif dist.python_tag != self.checkbuild_python_tag or dist.abi_tag != self.checkbuild_abi_tag or dist.platform_tag != self.checkbuild_platform_tag:
                logger.error(f"invalid wheel tag \"{dist.tag}\" for {dist.name} (expected {self.checkbuild_python_tag}-{self.checkbuild_abi_tag}-{self.checkbuild_platform_tag})")
                ok = False

        if not ok:
            return False

        if len(dists) >= 2:
            logger.error(f"several files generated in dist: {dists}")
            return False

        # "twine check": checks whether your distribution's long description will render correctly on PyPI.
        command = [sys.executable, "-m", "twine", "check", "--strict"] + [dist.path for dist in dists]
        cp = subprocess.run(command, text=True, stdout=sys.stdout, stderr=sys.stderr)
        if cp.returncode != 0:
            logger.error(f"check returned code {cp.returncode}")
            return False
        else:
            return dists


    def _upload_add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--repository", "-r", help="repository name, as declared in ~/.pypirc")


    def upload(self, repository=None, skip_check=False):
        """
        Upload the wheel from `dist` directory to a PyPI repository.
        """
        if skip_check:
            dists = self._get_dists()
        else:
            logger.info("check build")
            dists = self.checkbuild()
            if not dists:
                logger.warning(f"upload cancelled")
                return

        package = dists[0].package
        if not repository:
            try:
                repository = self.upload_repository
            except AttributeError:
                repository = package

        command = [sys.executable, "-m", "twine", "upload", "--repository", repository] + [dist.path for dist in dists]

        # Try to autoconfigure Twine
        env = {key: value for key, value in os.environ.items()}

        try:
            proxy_url = self.twine_proxy
        except AttributeError:
            proxy_url = get_configured_proxy_url(include_password=True)
        
        if proxy_url is not None:
            env["HTTP_PROXY"] = proxy_url
            env["HTTPS_PROXY"] = proxy_url
            
        try:
            env["TWINE_CERT"] = str(self.twine_cert)
        except AttributeError:
            pass

        # Run Twine
        logger.info(f"uploading to repository \"{repository}\": {', '.join(dist.name for dist in dists)}")
        cp = subprocess.run(command, text=True, env=env, stdout=sys.stdout, stderr=sys.stderr)
        if cp.returncode != 0:
            logger.error(f"twine upload returned code {cp.returncode}")


    def _build_add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--skip-test", action="store_true", help="do not run unit tests before build")
        parser.add_argument("--upload", "-u", action="store_true", help="upload to pypi after build")
        self._upload_add_arguments(parser)


    def build(self, upload = False, repository = None, skip_test = False):
        """
        Build a wheel in `dist` directory.
        """
        
        # Clean before build
        if hasattr(self, "clean"):
            logger.info("clean before build")
            self.clean()

        # Test
        if not self.build_skip_test and not skip_test:
            if not self.unittest():
                return

        # Build
        logger.info("build distribution")
        subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "-w", "dist", "."], check=True, stdout=sys.stdout, stderr=sys.stderr)

        # Check
        ok = True

        logger.info("check build")
        ok = ok and self.checkbuild()

        # Upload if required
        if upload:
            if not ok:
                logger.warning(f"upload cancelled")
                return
        
            logger.info(f"upload distribution")
            self.upload(repository=repository, skip_check=True)


class BaseTools(BuildMixin, CredentialsMixin, LsoMixin, CleanMixin):
    prog: str = None
    description: str = None
    version: str = None

    def exec(self):
        parser = ArgumentParser(prog=self.prog, description=self.description)
        parser.add_argument('--version', action='version', version=f"%(prog)s {self.version}")

        add_object_commands(parser, self, exclude=["exec"])
        exec_command(parser)
