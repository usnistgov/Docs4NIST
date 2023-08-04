#!/usr/bin/env python3
import os

from update_pages_action.repository import Repository
from update_pages_action.sphinxdocs import SeparatedSphinxDocs, UnifiedSphinxDocs


def main():
    if os.environ['INPUT_SEPARATED-LAYOUT'] == 'true':
        docs = SeparatedSphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])
    else:
        docs = UnifiedSphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])

    repo = Repository(server_url=os.environ['GITHUB_SERVER_URL'],
                      repository=os.environ['GITHUB_REPOSITORY'],
                      branch=os.environ['INPUT_PAGES-BRANCH'],
                      default_branch=os.environ['INPUT_DEFAULT-BRANCH'],
                      docs=docs,
                      pages_url=os.environ['INPUT_PAGES-URL'])

    repo.update_pages(branch=os.environ['SANITIZED_REF_NAME'],
                      sha=os.environ['GITHUB_SHA'])

if __name__ == "__main__":
    main()
