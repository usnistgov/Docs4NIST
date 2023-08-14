#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import subprocess

from borg_the_docs_action.sphinxdocs import SphinxDocs


def main():
    docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])
    docs.install_requirements(requirements=os.environ['INPUT_PIP-REQUIREMENTS'])
    docs.install_environment(environment=os.environ['INPUT_CONDA-ENVIRONMENT'])

    # Modify the Sphinx theme
    # This needs to be a subprocess so that it sees packages installed above
    subprocess.check_call(["/borg_the_docs.py"])

if __name__ == "__main__":
    main()
