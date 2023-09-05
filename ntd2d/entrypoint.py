#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import pathlib
import shutil
import shlex
import subprocess
import sys
import traceback


def main():
    # Install any APT packages
    apt_packages = os.environ['INPUT_APT-PACKAGES']
    if apt_packages != "":
        with gha_utils.group("Install APT packages", use_subprocess=True):
            subprocess.check_call(["apt-get", "update"])
            subprocess.check_call(["apt-get", "install",
                                   "--no-install-recommends", "--yes"]
                                  + shlex.split(apt_packages))
            subprocess.check_call(["apt-get", "autoremove"])
            subprocess.check_call(["apt-get", "clean"])
            for path in pathlib.Path("/var/lib/apt/lists/").glob("*"):
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()

    # Adapted from https://github.com/ammaraskar/sphinx-action/blob/master/sphinx_action/action.py#LL102C1-L105C1
    # [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)

    # Install any pip packages requested
    requirements = os.environ['INPUT_PIP-REQUIREMENTS']
    if requirements != "":
        with gha_utils.group("Install PIP packages", use_subprocess=True):
            requirements = pathlib.Path(requirements)
            if requirements.is_file():
                gha_utils.debug(f"pip installing", use_subprocess=True)
                subprocess.check_call(["pip", "install", "-r", requirements.as_posix()])

    # Install any Conda packages requested
    environment = os.environ['INPUT_CONDA-ENVIRONMENT']
    if environment != "":
        with gha_utils.group("Install Conda packages", use_subprocess=True):
            environment = pathlib.Path(environment)
            if environment.is_file():
                gha_utils.debug(f"conda installing", use_subprocess=True)
                subprocess.run(["conda", "env", "update",
                                # quiet to shut off progress bars
                                "--quiet",
                                # verbose to actually list what's installed
                                "--verbose",
                                "--name", "base",
                                "--file", environment.as_posix()],
                                bufsize=0,
                                timeout=60,
                                check=True,
                                capture_output=True)

    # Actually NIST the Docs 2 Death
    # This needs to be a subprocess so that it sees packages installed above
    subprocess.check_call(["/ntd2d.py"])

if __name__ == "__main__":
    try:
        try:
            main()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            if e.stdout is not None:
                gha_utils.echo(f"stdout: {e.stdout.decode('utf-8')}", use_subprocess=True)
            if e.stderr is not None:
                gha_utils.echo(f"stderr: {e.stderr.decode('utf-8')}", use_subprocess=True)
            raise
    except Exception as e:
        gha_utils.error("".join(traceback.format_exception(e)), use_subprocess=True)
        sys.exit(1)
