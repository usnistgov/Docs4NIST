import os
import pytest
import shutil

from ntd2d_action.repository import Repository
from ntd2d_action.sphinxdocs import SphinxDocs


# @pytest.fixture
def fake_filesystem():  # fs):
    # fs.create_dir("docs/")
    # fs.create_dir("__nist-pages")
    os.environ["GITHUB_SERVER_URL"] = "https://github.com"
    os.environ["GITHUB_REPOSITORY"] = "usnistgov/steppyngstounes"
    os.environ["GITHUB_REF_NAME"] = "NISTtheDocs2Death"
    os.environ["GITHUB_SHA"] = "deadbeef"

    os.environ['INPUT_DOCS-FOLDER'] = "/Users/guyer/Documents/research/FiPy/steppyngstounes/docs/"
    os.environ['INPUT_DEFAULT-BRANCH'] = "main"
    os.environ['INPUT_PAGES-BRANCH'] = "nist-pages"
    os.environ['INPUT_PAGES-URL'] = "https://pages.nist.gov"

#     yield fs


def test_my_fakefs(fake_filesystem):
    shutil.copytree(os.environ['INPUT_DOCS-FOLDER'], "test_docs")

    docs = SphinxDocs(docs_dir="test_docs")
    docs.assimilate_theme()

    repo = Repository(server_url=os.environ['GITHUB_SERVER_URL'],
                      repository=os.environ['GITHUB_REPOSITORY'],
                      branch=os.environ['INPUT_PAGES-BRANCH'],
                      default_branch=os.environ['INPUT_DEFAULT-BRANCH'],
                      docs=docs,
                      pages_url=os.environ['INPUT_PAGES-URL'])

    repo.update_pages(branch=os.environ['GITHUB_REF_NAME'],
                      sha=os.environ['GITHUB_SHA'])

if __name__ == "__main__":
    test_my_fakefs(fake_filesystem())
