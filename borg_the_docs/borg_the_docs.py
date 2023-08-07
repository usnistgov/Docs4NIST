#!/usr/bin/env python3
import github_action_utils as gha_utils
import os

from borg_the_docs_action.sphinxdocs import SphinxDocs
from borg_the_docs_action.borgedsphinxdocs import BorgedSphinxDocs


def main():
    original_docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])
    docs = BorgedSphinxDocs(original_docs=original_docs)
    docs.assimilate_theme(name="ntd2d")

    gha_utils.set_output("borged-docs-folder", docs.docs_dir.as_posix())
    gha_utils.set_output("borged-build-folder", docs.build_dir.as_posix())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        gha_utils.error(e.__traceback__)
        raise
