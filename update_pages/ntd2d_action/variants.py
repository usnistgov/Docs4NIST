import github_action_utils as gha_utils
import os
from packaging.version import parse, InvalidVersion
import pathlib
import shutil

from .files import VariantsFile, MenuFile, IndexFile

class Variant:
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name
        self.downloads = {}

        self.dir = repo.working_dir / "html" / name

    def rmdir(self):
        self.repo.remove(self.dir.as_posix(), working_tree=True,
                         r=True, ignore_unmatch=True)

    def copy_dir(self, src, dst):
        # remove any previous directory of that name
        self.rmdir()
        shutil.copytree(src, dst)
        self.repo.add(dst.as_posix())

    def copy_html(self, src):
        self.copy_dir(src=src, dst=self.dir)

    def copy_file(self, src, dst):
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(src, dst)
        self.repo.add((dst / src.name).as_posix())

    def copy_static_file(self, src):
        self.copy_file(src=src, dst=self.dir / "_static")

    def copy_download_file(self, src, kind):
        dst = self.dir / "_downloads"
        if src.exists():
            self.copy_file(src=src, dst=dst)
            self.downloads[kind] = dst / src.name

    def get_downloads_html(self):
        link_dir = pathlib.PurePath("/") / self.repo.repository
        downloads = []
        for kind, download in self.downloads.items():
            href = link_dir / download.relative_to(self.repo.working_dir)
            downloads.append(f'<a href="{href}">{kind}</a>')

        return "\n".join(downloads)

    def clone(self, name):
        clone = Variant(repo=self.repo, name=name)
        # this will clone any files in _static, too
        clone.copy_html(src=self.dir)

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

            gha_utils.debug(f"variant.name = {variant.name}")
            gha_utils.debug(f"self.current_variant.name = {self.current_variant.name}")
            gha_utils.debug(f"self.repo.refs")
            for ref in self.repo.refs:
                gha_utils.debug(f"...{ref}")
            gha_utils.debug(f"sself.repo.origin.refs")
            for ref in self.repo.origin.refs:
                gha_utils.debug(f"...{ref}")

            if (variant.name != self.current_variant.name
                and variant.name not in self.repo.refs
                and variant.name not in self.repo.origin.refs):
                # This variant has been removed from the repository,
                # so remove the corresponding docs
                gha_utils.debug(f"Deleting {variant.name}")
                variant.rmdir()
            elif isinstance(variant, Version):
                gha_utils.debug(f"Appending version {variant.name}")
                self._versions.append(variant)
            else:
                gha_utils.debug(f"Appending branch {variant.name}")
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

        return "\n".join(variants)

    def write_files(self, pages_url):
        variants_file = VariantsFile(repo=self.repo,
                                     variants=self,
                                     pages_url=pages_url)
        variants_file.write()

        url = variants_file.get_url()

        # Need an absolute url because this gets included from
        # many different levels
        MenuFile(variant=self.current_variant,
                 variants_url=url.geturl()).write()

        # This can be a relative url, because all variants should
        # be on the same server
        IndexFile(repo=self.repo, variants_url=url.path).write()
