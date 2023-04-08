from packaging.version import parse, InvalidVersion
import pathlib
import shutil

class VariantCollection:
    def __init__(self, repo):
        self.repo = repo
        self.branch = repo.branch
        self.default_branch = repo.default_branch

        self.html_dir = repo.working_dir / "html"

        self._branches = None
        self._latest = None
        self._stable = None
        self._stable_versions = None
        self._variants = None
        self._versions = None

    def copy_html(self, src, branch):
        dst = self.html_dir / branch

        # remove any previous directory of that name
        self.repo.remove(dst.as_posix(), working_tree=True,
                         r=True, ignore_unmatch=True)

        shutil.copytree(src, dst)
        self.repo.add(dst.as_posix())

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

    def get_variants_html(self):
        link_dir = (pathlib.PurePath("/") / self.repo.repository
                    / self.html_dir.relative_to(self.repo.working_dir))
        variants = []
        for variant in self.variants:
            href = link_dir / variant / "index.html"
            variants.append(f'<a href="{href}">{variant}</a>')

        return variants
