#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import pathlib
import subprocess


def main():
    with gha_utils.group("Install Prerequisites"):
        # Adapted from https://github.com/ammaraskar/sphinx-action/blob/master/sphinx_action/action.py#LL102C1-L105C1
        # [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)

        # Install any pip packages needed for Sphinx.
        requirements = os.environ['INPUT_PIP-REQUIREMENTS']
        if requirements != "":
            requirements = pathlib.Path(requirements)
            if requirements.is_file():
                gha_utils.debug(f"pip installing")
                subprocess.check_call(["pip", "install", "-r", requirements.as_posix()])

        # Install any Conda packages needed for Sphinx.
        environment = os.environ['INPUT_CONDA-ENVIRONMENT']
        if environment != "":
            environment = pathlib.Path(environment)
            if environment.is_file():
                gha_utils.debug(f"conda installing")
                subprocess.check_call(["conda", "env", "update", "--quiet",
                                       "--name", "base",
                                       "--file", environment.as_posix()])

    # Actually NIST the Docs 2 Death
    # This needs to be a subprocess so that it sees packages installed above
    subprocess.check_call(["/ntd2d.py"])

if __name__ == "__main__":
    main()
