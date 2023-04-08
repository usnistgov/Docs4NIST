import git
import pathlib

from .versions import VariantCollection

class Repository:
    def __init__(self, server_url, repository, branch, default_branch):
        self.url = f"{server_url}/{repository}.git"
        self.owner, self.repository = repository.split('/')
        self.branch = branch
        self.default_branch = default_branch

        self.working_dir = None
        self.variant_collection = None

    def add(self, *args, **kwargs):
        self.repo.index.add(*args, **kwargs)

    def clone(self, to_path):
        self.repo = git.Repo.clone_from(self.url,
                                        to_path=to_path,
                                        branch=self.branch,
                                        single_branch=True)

        self.working_dir = pathlib.Path(self.repo.working_dir)

        self.variant_collection = VariantCollection(repo=self)

    def commit(self, message):
        if len(self.repo.index.diff("HEAD")) > 0:
            # GitPython will make an empty commit if no changes,
            # so only commit if things have actually changed
            author = git.Actor("GitHub Action", "action@github.com")
            self.repo.index.commit(message=message, author=author)

    def copy_html(self, *args, **kwargs):
        self.variant_collection.copy_html(*args, **kwargs)

    def get_versions(self):
        return self.variant_collection.get_versions()

    def remove(self, *args, **kwargs):
        self.repo.index.remove(*args, **kwargs)
