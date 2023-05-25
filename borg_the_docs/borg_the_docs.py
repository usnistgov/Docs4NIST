#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import shutil

from ntd2d_action.sphinxdocs import SphinxDocs
from ntd2d_action.files import ConfFile


def main():
    docs_folder_borged = f"{os.environ['INPUT_DOCS-FOLDER']}-BORGED"
    shutil.copytree(os.environ['INPUT_DOCS-FOLDER'], docs_folder_borged)

    conf = ConfFile(docs_dir=docs_folder_borged)
    conf.assimilate_theme(name="ntd2d")
    conf.write()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        gha_utils.error(e.__traceback__)
        raise
