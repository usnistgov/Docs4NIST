#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import subprocess

from update_pages_action.sphinxdocs import SphinxDocs


def main():
    docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])
    docs.install_requirements()

    # Modify the Sphinx theme
    # This needs to be a subprocess so that it sees packages installed above
    subprocess.check_call(["/update_pages.py"])

if __name__ == "__main__":
    main()
