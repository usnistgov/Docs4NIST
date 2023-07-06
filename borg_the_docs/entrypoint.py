#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import pathlib
import subprocess


def main():
    # Install any packages needed for Sphinx
    # Adapted from https://github.com/ammaraskar/sphinx-action/blob/master/sphinx_action/action.py#LL102C1-L105C1
    # [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)
    source_dir = pathlib.Path(os.environ['INPUT_DOCS-FOLDER'])
    if os.environ['INPUT_SEPARATED-LAYOUT'] == 'true':
        source_dir = source_dir / "source"
    docs_requirements = source_dir / "requirements.txt"
    if docs_requirements.is_file():
        gha_utils.debug(f"pip installing")
        subprocess.check_call(["pip", "install", "-r", docs_requirements.as_posix()])

    gha_utils.warning(f"separated-layout = {os.environ['INPUT_SEPARATED-LAYOUT']}")

    # Modify the Sphinx theme
    # This needs to be a subprocess so that it sees packages installed above
    subprocess.check_call(["/borg_the_docs.py"])

if __name__ == "__main__":
    main()
