import github_action_utils as gha_utils
from packaging.version import parse, InvalidVersion
import pathlib
import shutil

from .files import VariantsFile, MenuFile, IndexFile

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

        return clone

    def __lt__(self, other):
        return self.name < other.name

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

    def __lt__(self, other):
        if isinstance(other, Version):
            return self.version < other.version
        else:
            return super().__lt__(other)

class VariantCollection:
    def __init__(self, repo, current_variant):
        self.repo = repo
        self.current_variant = current_variant

        self.html_dir = repo.working_dir / "html"

        self._latest = None
        self._stable = None
        self._branches = None
        self._versions = None

    @property
    def latest(self):
        gha_utils.start_group("VariantCollection.latest")
        if self._latest is None:
            for branch in self.branches:
                gha_utils.debug(f"{branch.name} =?= {self.repo.default_branch}")
                if branch.name == self.repo.default_branch:
                    # replace any built documents in latest/
                    # (but only do this for default branch of repo)
                    self._latest = branch.clone("latest")
                    gha_utils.debug(f"Cloned {branch.name} to {self._latest.name}")
                    break

        gha_utils.end_group()
        return self._latest

    @property
    def stable(self):
        gha_utils.start_group("VariantCollection.stable")
        if self._stable is None:
            # replace any built documents in stable/
            # (but only do this for highest non-prerelease version)
            if len(self.stable_versions) > 0:
                self._stable = self.stable_versions[0].clone("stable")
                gha_utils.debug(f"Cloned {self.stable_versions[0].name} to {self._stable.name}")
            else:
                self._stable = None

        gha_utils.end_group()
        return self._stable

    @property
    def stable_versions(self):
        return [version
                for version in self.versions
                if not version.version.is_prerelease]

    def _calc_branches_and_versions(self):
        def sanitize(refs):
            """Replace slashes in ref names

            In a PR, refs can be, e.g., `12/merge`,
            which causes downstream grief.
            """
            sanitized = [ref.name.replace("/", "_") for ref in refs]
            for name in sanitized:
                gha_utils.warning(name)
            return sanitized

        gha_utils.start_group("VariantCollection._calc_branches_and_versions")

        names = [variant.name for variant in self.html_dir.glob("*")]

        gha_utils.debug(f"self.repo.refs = {self.repo.refs}")

        self._branches = []
        self._versions = []
        for name in names:
            gha_utils.start_group(f"{name}")
            try:
                # Check if it's a PEP 440 version.
                # Retain the string literal for the tag or branch,
                # but use the Version for sorting.
                variant = Version(repo=self.repo, name=name)
                gha_utils.debug(f"Version({variant.name})")
            except InvalidVersion:
                variant = Variant(repo=self.repo, name=name)
                gha_utils.debug(f"Variant({variant.name})")

            if variant.name in ["latest", "stable"]:
                continue

            if (variant != self.current_variant
                and variant.name not in sanitize(self.repo.refs)
                and variant.name not in sanitize(self.repo.origin.refs)):
                # This variant has been removed from the repository,
                # so remove the corresponding docs
                gha_utils.warning(f"Deleting {variant.name}")
                variant.rmdir()
            elif isinstance(variant, Version):
                gha_utils.debug(f"Appending version")
                self._versions.append(variant)
            else:
                gha_utils.debug(f"Appending branch")
                self._branches.append(variant)
            gha_utils.end_group()
        self._branches.sort()
        self._versions.sort(reverse=True)

        gha_utils.end_group()

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

        variants = ([self.latest, self.stable]
                    + self.versions + self.branches)
        variants = [variant
                    for variant in variants
                    if variant is not None]

        return variants

    def get_html(self):
        link_dir = (pathlib.PurePath("/") / self.repo.repository
                    / self.html_dir.relative_to(self.repo.working_dir))
        variants = []
        for variant in self.variants:
            href = link_dir / variant.name / "index.html"
            variants.append(f'<a href="{href}">{variant.name}</a>')

        return variants

    def write_files(self, pages_url):
        variants_file = VariantsFile(repo=self.repo,
                                     variants=self,
                                     pages_url=pages_url)
        variants_file.write()

        url = variants_file.get_url()

        for variant in self.variants:
            # Need an absolute url because this gets included from
            # many different levels
            MenuFile(variant=variant,
                     variants_url=url.geturl()).write()

        # This can be a relative url, because all variants should
        # be on the same server
        IndexFile(repo=self.repo, variants_url=url.path).write()
