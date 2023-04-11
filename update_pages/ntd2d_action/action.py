import pathlib

from .files import NoJekyllFile, VariantsFile, MenuFile, IndexFile

class NISTtheDocs2Death:
    def __init__(self, repo, docs, pages_url):
        self.repo = repo
        self.docs = docs
        self.pages_url = pages_url

    def update_pages(self, branch, sha):
        self.repo.clone(to_path="__nist-pages")

        # replace any built documents in directory named for current branch
        self.repo.copy_html(src=self.docs.html_dir, branch=branch)

        NoJekyllFile(repo=self.repo).write()

        variants = VariantsFile(repo=self.repo,
                                variants=self.repo.variant_collection,
                                pages_url=self.pages_url)
        variants.write()

        # Need an absolute url because this gets included from
        # many different levels
        MenuFile(repo=self.repo,
                 current_branch=branch,
                 variants_url=variants.get_url().geturl()).write()

        # This can be a relative url, because all variants should
        # be on the same server
        IndexFile(repo=self.repo, variants_url=variants.get_url().path).write()

        self.repo.commit(message=f"Update documentation for {branch}@{sha[:7]}")
