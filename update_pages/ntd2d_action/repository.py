import git
import github_action_utils as gha_utils
import pathlib

from .files import NoJekyllFile
from .variants import Variant, VariantCollection

class Repository:
    def __init__(self, server_url, repository, branch, default_branch, docs, pages_url):
        self.server_url = server_url
        self.url = f"{server_url}/{repository}.git"
        self.owner, self.repository = repository.split('/')
        self.tree_url = f"{server_url}/{self.owner}/{self.repository}/tree/{branch}"
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
        self.repo = git.Repo.clone_from(self.url,
                                        to_path=to_path,
                                        branch=self.branch)

    def commit(self, message):
        if len(self.repo.index.diff("HEAD")) > 0:
            # GitPython will make an empty commit if no changes,
            # so only commit if things have actually changed
            author = git.Actor("GitHub Action", "action@github.com")
            self.repo.index.commit(message=message, author=author)

            gha_utils.debug(f"Committed '{message}'")

    def remove(self, *args, **kwargs):
        self.repo.index.remove(*args, **kwargs)

    def update_pages(self, branch, sha):
        gha_utils.debug("Repository.update_pages")

        self.clone(to_path="__nist-pages")

        gha_utils.debug(f"clone()")

        NoJekyllFile(repo=self).write()

        gha_utils.debug(f".nojekyll")

        # replace any built documents in directory named for current branch
        variant = Variant(repo=self, name=branch)

        gha_utils.debug(f"Variant {variant.name}")

        variant.copy_html(src=self.docs.html_dir)
        variant.copy_download_file(src=self.docs.epub_file, kind="ePUB")
        variant.copy_download_file(src=self.docs.pdf_file, kind="PDF")

        VariantCollection(repo=self, current_variant=variant).write_files(pages_url=self.pages_url)

        self.commit(message=f"Update documentation for {branch}@{sha[:7]}")

        self.repo.remotes.origin.pull()
