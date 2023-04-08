import os
import pytest

from ntd2d_action.repository import Repository
from ntd2d_action.action import NISTtheDocs2Death


@pytest.fixture
def fake_filesystem():  # fs):
    # fs.create_dir("docs/")
    # fs.create_dir("__nist-pages")
    os.environ["GITHUB_SERVER_URL"] = "https://github.com"
    os.environ["GITHUB_REPOSITORY"] = "usnistgov/steppyngstounes"
    os.environ["GITHUB_REF_NAME"] = "NISTtheDocs2Death"
    os.environ["GITHUB_SHA"] = "deadbeef"

#     yield fs


def test_my_fakefs(fake_filesystem):
    repo = Repository(server_url=os.environ['GITHUB_SERVER_URL'],
                      repository=os.environ['GITHUB_REPOSITORY'],
                      branch="nist-pages",
                      default_branch="main")

    docs_dir = "/Users/guyer/Documents/research/FiPy/steppyngstounes/docs/"
    xx = NISTtheDocs2Death(repo=repo,
                           docs_dir=docs_dir,
                           pages_url="https://pages.nist.gov")

    xx.update_pages(branch=os.environ['GITHUB_REF_NAME'],
                    sha=os.environ['GITHUB_SHA'])
