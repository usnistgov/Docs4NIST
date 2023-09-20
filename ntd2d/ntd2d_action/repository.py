"""Interface to a git/GitHub repositories.
"""
__docformat__ = 'restructuredtext'

import git
import github_action_utils as gha_utils
import pathlib

from .files import NoJekyllFile
from .variants import Variant, VariantCollector

class Repository:
    """Interface to a git/GitHub repository.

    Parameters
    ----------
    server_url : url
      The URL of the GitHub server (:envvar:`GITHUB_SERVER_URL`).
    repository : str
      The owner and repository name (:envvar:`GITHUB_REPOSITORY`).
    branch : str
      The branch linked to your documentation server (:ref:`NTD2D_PAGES-BRANCH`).
    default-branch : str
      The default branch configured in GitHub (:ref:`NTD2D_DEFAULT-BRANCH`).
    docs : ~ntd2d_action.sphinxdocs.SphinxDocs
      The documentation being built.
    pages_url : url
      URL of the web server for served documentation (:ref:`NTD2D_PAGES-URL`).
    """

    def __init__(self, server_url, repository, branch, default_branch, docs, pages_url):
        self.server_url = server_url
        self.url = f"{server_url}/{repository}.git"
        self.owner, self.repository = repository.split('/')
        self.tree_url = f"{server_url}/{self.owner}/{self.repository}/tree"
        self.branch = branch
        self.default_branch = default_branch
        self.docs = docs
        self.pages_url = pages_url

    @property
    def working_dir(self):
        return pathlib.Path(self.repo.working_dir)

    @property
    def refs(self):
        return self.repo.refs

    @property
    def origin(self):
        return self.repo.remotes.origin

    def add(self, *args, **kwargs):
        self.repo.index.add(*args, **kwargs)

    def clone(self, to_path):
        gha_utils.echo(f"Clone {self.url}@{self.branch} -> {to_path}",
                       use_subprocess=True)

        self.repo = git.Repo.clone_from(self.url,
                                        to_path=to_path,
                                        branch=self.branch)

    def commit(self, message):
        if len(self.repo.index.diff("HEAD")) > 0:
            # GitPython will make an empty commit if no changes,
            # so only commit if things have actually changed
            author = git.Actor("GitHub Action", "action@github.com")
            self.repo.index.commit(message=message, author=author)

            gha_utils.echo(f"Commit '{message}'",
                           use_subprocess=True)

    def remove(self, *args, **kwargs):
        self.repo.index.remove(*args, **kwargs)

    def update_pages(self, branch, sha):
        """Commit built documentation to :ref:`NTD2D_PAGES-BRANCH`.

        Parameters
        ----------
        branch : str
          The sanitized ('/' removed) short ref name of the branch or tag
          that triggered the workflow (:envvar:`GITHUB_REF_NAME`).
        sha : str
          The commit SHA that triggered the workflow (:envvar:`GITHUB_SHA`).
        """

        gha_utils.debug("Repository.update_pages", use_subprocess=True)

        self.clone(to_path="__nist-pages")

        gha_utils.debug(f"clone()", use_subprocess=True)

        NoJekyllFile(repo=self).write()

        gha_utils.debug(f".nojekyll", use_subprocess=True)

        # replace any built documents in directory named for current branch
        variant = Variant(repo=self, name=branch, rebuild_menu=True)

        gha_utils.debug(f"Variant {variant.name}", use_subprocess=True)

        variant.copy_html(src=self.docs.html_dir)
        variant.copy_download_file(src=self.docs.epub_file, kind="ePUB")
        variant.copy_download_file(src=self.docs.pdf_file, kind="PDF")

        VariantCollector(repo=self, current_variant=variant).write_files(pages_url=self.pages_url)

        self.commit(message=f"Update documentation for {branch}@{sha[:7]}")

        self.repo.remotes.origin.pull(ff_only=True)
