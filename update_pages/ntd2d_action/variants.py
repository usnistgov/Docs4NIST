from packaging.version import parse, InvalidVersion
import pathlib
import shutil

class Variant:
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name

        self.dir = repo.working_dir / "html" / name

    def rmdir(self):
        self.repo.remove(self.dir.as_posix(), working_tree=True,
                         r=True, ignore_unmatch=True)

    def copy_dir(self, src):
        # remove any previous directory of that name
        self.rmdir()
        shutil.copytree(src, self.dir)
        self.repo.add(self.dir.as_posix())

    def clone(self, name):
        clone = Variant(repo=self.repo, name=name)
        clone.copy_dir(src=self.dir)

    def __del__(self):
        self.rmdir()

class Version(Variant):
    """A Variant that satisfies the PEP 440 version specification

    Raises
    ------
    InvalidVersion
        If the name is not parsable by packaging.version
    """
    def __init__(self, repo, name):
        super().__init__(repo=repo, name=name)
        self.version = parse(name)

class VariantCollection:
    def __init__(self, repo):
        self.repo = repo

        self.html_dir = repo.working_dir / "html"

        self._branches = None
        self._latest = None
        self._stable = None
        self._stable_versions = None
        self._variants = None
        self._versions = None

    @property
    def latest(self):
        if self._latest is None:
            latest = [branch in self.branches if branch.name == "latest"]
            if len(latest) > 0:
                self._latest = latest[0]

        return self._latest

    @property
    def stable(self):
        if self._stable is None:
            # replace any built documents in stable/
            # (but only do this for highest non-prerelease version)
            if len(self.stable_versions) > 0:
                self._stable = self.stable_versions[0].clone("stable")

        return self._stable

    @property
    def stable_versions(self):
        if self._stable_versions is None:
            self._stable_versions = [version
                                     for in self.versions
                                     if not version.version.is_prerelease]

        return self._stable_versions

    def _calc_branches_and_versions(self):
        names = [variant.name for variant in self.html_dir.glob("*")]

        self._branches = []
        self._versions = []
        for name in names:
            try:
                # Check if it's a PEP 440 version.
                # Retain the string literal for the tag or branch,
                # but use the Version for sorting.
                variant = Version(repo=self.repo, name=name)
            except InvalidVersion:
                variant = Variant(repo=self.repo, name=variant)

            if isinstance(variant, Version):
                self._versions.append(variant)
            else:
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
            href = link_dir / variant.name / "index.html"
            variants.append(f'<a href="{href}">{variant.name}</a>')

        return variants
