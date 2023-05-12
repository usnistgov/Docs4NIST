import git
import github_action_utils as gha_utils
import pathlib

from .files import NoJekyllFile, VariantsFile, MenuFile, IndexFile
from .variants import Variant, VariantCollection

class Repository:
    def __init__(self, server_url, repository, branch, default_branch, docs, pages_url):
        self.url = f"{server_url}/{repository}.git"
        self.owner, self.repository = repository.split('/')
        self.branch = branch
        self.default_branch = default_branch
        self.docs = docs
        self.pages_url = pages_url

    @property
    def working_dir(self):
        return pathlib.Path(self.repo.working_dir)

    def add(self, *args, **kwargs):
        self.repo.index.add(*args, **kwargs)

    def clone(self, to_path):
        self.repo = git.Repo.clone_from(self.url,
                                        to_path=to_path,
                                        branch=self.branch,
                                        single_branch=True)

    def commit(self, message):
        if len(self.repo.index.diff("HEAD")) > 0:
            # GitPython will make an empty commit if no changes,
            # so only commit if things have actually changed
            author = git.Actor("GitHub Action", "action@github.com")
            self.repo.index.commit(message=message, author=author)

            gha_utils.notice(f"Committed '{message}'")

    def remove(self, *args, **kwargs):
        self.repo.index.remove(*args, **kwargs)

    def update_pages(self, branch, sha):
        self.clone(to_path="__nist-pages")

        NoJekyllFile(repo=self).write()

        # replace any built documents in directory named for current branch
        variant = Variant(repo=self, name=branch)
        variant.copy_dir(src=self.docs.html_dir)

        if variant.name == self.default_branch:
            # replace any built documents in latest/
            # (but only do this for default branch of repo)
            latest = variant.clone("latest")

        variants = VariantsFile(repo=self,
                                variants=VariantCollection(repo=self),
                                pages_url=self.pages_url)
        variants.write()

        # Need an absolute url because this gets included from
        # many different levels
        MenuFile(repo=self,
                 current_branch=branch,
                 variants_url=variants.get_url().geturl()).write()

        # This can be a relative url, because all variants should
        # be on the same server
        IndexFile(repo=self, variants_url=variants.get_url().path).write()

        self.commit(message=f"Update documentation for {branch}@{sha[:7]}")

        self.repo.remotes.origin.pull()
