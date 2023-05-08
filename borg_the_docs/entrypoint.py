#!/usr/bin/env python3
import os

from ntd2d_action.repository import Repository
from ntd2d_action.sphinxdocs import SphinxDocs


def main():
    action = os.environ['INPUT_ACTION']
    docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])

    if action == 'update_pages':
        repo = Repository(server_url=os.environ['GITHUB_SERVER_URL'],
                          repository=os.environ['GITHUB_REPOSITORY'],
                          branch=os.environ['INPUT_PAGES-BRANCH'],
                          default_branch=os.environ['INPUT_DEFAULT-BRANCH'],
                          docs=docs,
                          pages_url=os.environ['INPUT_PAGES-URL'])

        repo.update_pages(branch=os.environ['GITHUB_REF_NAME'],
                          sha=os.environ['GITHUB_SHA'])
    elif action == 'borg_the_docs':
        docs.assimilate_theme()

if __name__ == "__main__":
    main()
