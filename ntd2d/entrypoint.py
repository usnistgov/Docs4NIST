#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import pathlib
import shutil
import subprocess
import sys
import traceback


def main():
    with gha_utils.group("Install APT packages", use_subprocess=True):
        # Install any APT packages
        apt_packages = os.environ['INPUT_APT-PACKAGES']
        if apt_packages != "":
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

    with gha_utils.group("Install PIP packages", use_subprocess=True):
        # Install any pip packages requested
        requirements = os.environ['INPUT_PIP-REQUIREMENTS']
        if requirements != "":
            requirements = pathlib.Path(requirements)
            if requirements.is_file():
                gha_utils.debug(f"pip installing", use_subprocess=True)
                subprocess.check_call(["pip", "install", "-r", requirements.as_posix()])

    with gha_utils.group("Install Conda packages", use_subprocess=True):
        # Install any Conda packages requested
        environment = os.environ['INPUT_CONDA-ENVIRONMENT']
        if environment != "":
            environment = pathlib.Path(environment)
            if environment.is_file():
                gha_utils.debug(f"conda installing", use_subprocess=True)
                subprocess.check_call(["conda", "env", "update", "--quiet",
                                       "--name", "base",
                                       "--file", environment.as_posix()])

    # Actually NIST the Docs 2 Death
    # This needs to be a subprocess so that it sees packages installed above
    subprocess.check_call(["/ntd2d.py"])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        for line in traceback.format_exception(e):
            for subline in line.rstrip().split('\n'):
                gha_utils.error(subline, use_subprocess=True)
        sys.exit(1)
