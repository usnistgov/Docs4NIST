#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import pathlib
import shutil

from ntd2d_action.sphinxdocs import SphinxDocs
from ntd2d_action.files import ConfFile


def main():
    borged_folder = pathlib.Path(os.environ['INPUT_DOCS-FOLDER']).as_posix()
    borged_folder += "-BORGED"
    shutil.copytree(os.environ['INPUT_DOCS-FOLDER'], borged_folder)

    conf = ConfFile(docs_dir=borged_folder)
    conf.assimilate_theme(name="ntd2d")
    conf.write()

    gha_utils.warning(f"borged-docs-folder={borged_folder}")
    gha_utils.set_output("borged-docs-folder", borged_folder)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        gha_utils.error(e.__traceback__)
        raise
