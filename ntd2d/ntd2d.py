#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import sys
import traceback

from ntd2d_action.sphinxdocs import SphinxDocs
from ntd2d_action.borgedsphinxdocs import BorgedSphinxDocs
from ntd2d_action.repository import Repository


def main():
    with gha_utils.group("Borg the Docs"):
        original_docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])
        docs = BorgedSphinxDocs(original_docs=original_docs)
        docs.assimilate_theme(name="ntd2d")
    
        gha_utils.set_output("borged-build-folder", docs.build_dir.as_posix())

    with gha_utils.group("Update Pages"):
        repo = Repository(server_url=os.environ['GITHUB_SERVER_URL'],
                          repository=os.environ['GITHUB_REPOSITORY'],
                          branch=os.environ['INPUT_PAGES-BRANCH'],
                          default_branch=os.environ['INPUT_DEFAULT-BRANCH'],
                          docs=docs,
                          pages_url=os.environ['INPUT_PAGES-URL'])

        repo.update_pages(branch=os.environ['SANITIZED_REF_NAME'],
                          sha=os.environ['GITHUB_SHA'])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        for line in traceback.format_exception(e.):
            gha_utils.error(line)
        sys.exit(1)
