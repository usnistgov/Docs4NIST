#!/usr/bin/env python3
import os
import subprocess

from ntd2d_action.repository import Repository
from ntd2d_action.sphinxdocs import SphinxDocs


def main():
    action = os.environ['INPUT_ACTION']
    docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS_FOLDER'])

    if action == 'update_pages':
        repo = Repository(server_url=os.environ['GITHUB_SERVER_URL'],
                          repository=os.environ['GITHUB_REPOSITORY'],
                          branch=os.environ['INPUT_PAGES_BRANCH'],
                          default_branch=os.environ['INPUT_DEFAULT_BRANCH'],
                          docs=docs,
                          pages_url=os.environ['INPUT_PAGES_URL'])

        repo.update_pages(branch=os.environ['SANITIZED_REF_NAME'],
                          sha=os.environ['GITHUB_SHA'])
    elif action == 'borg_the_docs':
        docs.assimilate_theme()

if __name__ == "__main__":
    main()
