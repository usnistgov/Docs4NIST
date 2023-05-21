#!/usr/bin/env python3
import os

from ntd2d_action.sphinxdocs import SphinxDocs


def main():
    docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])

    docs.assimilate_theme()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        gha_utils.error(e.__traceback__)
        raise
