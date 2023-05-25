#!/usr/bin/env python3
import github_action_utils as gha_utils
import os

from ntd2d_action.sphinxdocs import SphinxDocs
from ntd2d_action.files import ClonedConfFile


def main():
    conf = ClonedConfFile(docs_dir=os.environ['INPUT_DOCS-FOLDER'])
    conf.assimilate_theme(name="ntd2d")
    conf.write()

    gha_utils.set_output("borged-docs-folder", conf.docs_dir.as_posix())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        gha_utils.error(e.__traceback__)
        raise
