import argparse
import git
import os
from packaging.version import parse, InvalidVersion
import pathlib
import shutil
import textwrap
from urllib.parse import urlparse


class NISTtheDocs2Death(object):
    def __init__(self, docs_dir, default_branch, pages_branch, pages_url):
        self.repo_url = (f"{os.environ['GITHUB_SERVER_URL']}"
                         f"/{os.environ['GITHUB_REPOSITORY']}.git")
        self.branch = os.environ['GITHUB_REF_NAME']
        self.sha = os.environ['GITHUB_SHA']

        self.docs_dir = pathlib.Path(docs_dir)
        self.default_branch = default_branch
        self.pages_branch = pages_branch
        self.pages_url = pages_url

        parsed = urlparse(self.repo_url)
        self.repository = pathlib.PurePath(parsed.path).stem

        self.build_dir = self.docs_dir / "_build" / "html"

        self.action_dir = pathlib.Path(__file__).parent

        self.repo = None
        self.working_dir = None
        self.html_dir = None
        self.versions_html = None

        self._branches = None
        self._latest = None
        self._stable = None
        self._stable_versions = None
        self._variants = None
        self._versions = None

    def clone(self):
        self.repo = git.Repo.clone_from(self.repo_url,
                                        to_path="__nist-pages",
                                        branch=self.pages_branch,
                                        single_branch=True)

        self.working_dir = pathlib.Path(self.repo.working_dir)
        self.html_dir = self.working_dir / "html"

    def copy_html(self, branch, src=None):
        dst = self.html_dir / branch

        # remove any previous directory of that name
        self.repo.index.remove(dst.as_posix(), working_tree=True,
                               r=True, ignore_unmatch=True)
        if src is None:
            src = self.build_dir
        shutil.copytree(src, dst)
        self.repo.index.add(dst.as_posix())

    @property
    def latest(self):
        if self._latest is None:
            # replace any built documents in latest/
            # (but only do this for default branch of repo)
            if self.branch == self.default_branch:
                self.copy_html(branch="latest")
                self._latest = ["latest"]

        return self._latest

    @property
    def stable(self):
        if self._stable is None:
            stable_versions = self.stable_versions

            # replace any built documents in stable/
            # (but only do this for highest non-prerelease version)
            if len(stable_versions) > 0:
                stable = stable_versions[0]
                self.copy_html(branch=stable,
                               src=self.html_dir / stable)
                self._stable = stable

        return self._stable

    @property
    def stable_versions(self):
        if self._stable_versions is None:
            self._stable_versions = [(version, label)
                                     for (version, label) in self.versions
                                     if not version.is_prerelease]

        return self._stable_versions

    def _calc_branches_and_versions(self):
        variants = [variant.name for variant in self.html_dir.glob("*")]

        self._branches = []
        self._versions = []
        for variant in variants:
            try:
                # Check if it's a PEP 440 version.
                # Retain the string literal for the tag or branch,
                # but use the Version for sorting.
                self._versions.append((parse(variant), variant))
            except InvalidVersion:
                self._branches.append(variant)
        self._branches.sort()
        self._versions.sort(reverse=True)

    @property
    def branches(self):
        if self._branches is None:
            self._calc_branches_and_versions()

        return self._branches

    @property
    def versions(self):
        if self._versions is None:
            self._calc_branches_and_versions()

        return self._versions

    @property
    def variants(self):
        """Collect tags and versions with documentation
        """
        # variants = ["v1.0.0", "stables", "1.2.3", "latest", "4b1",
        #             "0.2", "neat_idea", "doesn't_work", "experiment"]

        if self._variants is None:
            self._variants = ([self.latest, self.stable]
                              + self.versions + self.branches)
            self._variants = [variant
                              for variant in self._variants
                              if variant is not None]

        return self._variants

    def get_versions(self):
        link_dir = (pathlib.PurePath("/") / self.repository
                    / self.html_dir.relative_to(self.working_dir))
        versions = []
        print(self.variants)
        for version in self.variants:
            href = link_dir / version / "index.html"
            versions.append(f'<a href="{href}">{version}</a>')

        versions = textwrap.indent("\n".join(versions), "  ")

        versions_template = self.load_template(name="versions.html")
        return versions_template.format(versions=versions)

    def get_menu(self):
        # Need an absolute url because this gets included from
        # many different levels
        versions = self.get_iframe(src=self.versions_html.geturl())

        menu_template = self.load_template(name="menu.html")
        return menu_template.format(versions=textwrap.indent(versions, "    "),
                                    branch=self.branch)

    def load_template(self, name):
        # look in _templates/ directory of nist-pages branch
        template_fname = self.working_dir / "_templates" / name
        if not template_fname.exists():
            # look in templates/ directory of this action
            template_fname = self.action_dir / "templates" / name

        with open(template_fname, mode='r') as template_file:
            template = template_file.read()

        return template

    def get_iframe(self, src):
        iframe_template = self.load_template(name="iframe.html")
        return iframe_template.format(src=src)

    def get_index(self):
        """build index.html with available documentation versions
        """
        # This can be a relative url, because all version should
        # be on the same server
        versions = self.get_iframe(src=self.versions_html.path)
        versions = textwrap.indent(versions, "    ")

        index_template = self.load_template(name="index.html")
        return index_template.format(versions=versions,
                                     repository=self.repository)

    def set_versions_html(self, versions_html):
        full_url = "/".join([self.pages_url,
                             self.repository,
                             str(versions_html.relative_to(self.working_dir))])

        self.versions_html = urlparse(full_url)

    def write_nojekyll(self):
        # jekyll conflicts with sphinx' underlined directories and files
        nojekyll = self.working_dir / ".nojekyll"
        nojekyll.touch()
        self.repo.index.add(nojekyll)

    def write_global_versions(self):
        includes = self.working_dir / "_includes"
        includes.mkdir(exist_ok=True)
        versions_html = includes / "ntd2d_versions.html"
        with open(versions_html, mode='w') as version_file:
            version_file.write(self.get_versions())
        self.repo.index.add(versions_html)

        self.set_versions_html(versions_html)

    def write_local_versions(self):
        static = self.html_dir / self.branch / "_static"
        static.mkdir(exist_ok=True)
        menu_html = static / "ntd2d_versions.html"
        with open(menu_html, mode='w') as menu_file:
            menu_file.write(self.get_menu())
        self.repo.index.add(menu_html)

    def write_index_html(self):
        index_html = self.working_dir / "index.html"
        with open(index_html, mode='w') as index_file:
            index_file.write(self.get_index())
        self.repo.index.add(index_html)

    def commit(self):
        if len(self.repo.index.diff("HEAD")) > 0:
            # GitPython will make an empty commit if no changes,
            # so only commit if things have actually changed
            message = f"Update documentation for {self.branch}@{self.sha[:7]}"
            author = git.Actor("GitHub Action", "action@github.com")
            self.repo.index.commit(message=message, author=author)

    def update_pages(self):
        self.clone()

        # replace any built documents in directory named for current branch
        self.copy_html(branch=self.branch)

        self.write_nojekyll()
        self.write_global_versions()
        self.write_local_versions()
        self.write_index_html()

        self.commit()


def main():
    description = 'Update nist-pages branch based on sphinx builds'
    parser = argparse.ArgumentParser(
                        prog='NistTheDocs2Death',
                        description=description)

    parser.add_argument('docs_dir')
    parser.add_argument('default_branch')
    parser.add_argument('pages_branch')
    parser.add_argument('pages_url')

    args = parser.parse_args()

    ntd2d = NISTtheDocs2Death(docs_dir=args.docs_dir,
                              default_branch=args.default_branch,
                              pages_branch=args.pages_branch,
                              pages_url=args.pages_url)
    ntd2d.update_pages()


if __name__ == "__main__":
    main()
