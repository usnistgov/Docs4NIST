import github_action_utils as gha_utils
from collections import UserList
import os
from packaging.version import parse, InvalidVersion
import pathlib
import re
import shutil

from .files import VariantsFile, MenuFile, IndexFile, CSSFile

class Variant:
    def __init__(self, repo, name, rebuild_menu=False, true_name=None):
        self.repo = repo
        self.name = name
        self.rebuild_menu = rebuild_menu
        if true_name is None:
            self.true_name = name
        else:
            self.true_name = true_name
        self.downloads = {}

        self.dir = repo.working_dir / "html" / name

    def rmdir(self):
        gha_utils.debug(f"{self.name}.rmdir()")
        self.repo.remove(self.dir.as_posix(), working_tree=True,
                         r=True, ignore_unmatch=True)

    def copy_dir(self, src, dst):
        gha_utils.debug(f"{self.name}.copy_dir(src={src}, dst={dst})")
        # remove any previous directory of that name
        self.rmdir()
        shutil.copytree(src, dst)
        self.repo.add(dst.as_posix())

    def copy_html(self, src):
        gha_utils.debug(f"{self.name}.copy_html(src={src})")
        self.copy_dir(src=src, dst=self.dir)

    def copy_file(self, src, dst):
        gha_utils.debug(f"{self.name}.copy_file(src={src}, dst={dst})")
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(src, dst)
        self.repo.add((dst / src.name).as_posix())

    def copy_static_file(self, src):
        self.copy_file(src=src, dst=self.dir / "_static")

    def copy_download_file(self, src, kind):
        gha_utils.debug(f"{self.name}.copy_download_file(src={src}, kind={kind})")
        dst = self.dir / "_downloads"
        if src.exists():
            self.copy_file(src=src, dst=dst)
            self.downloads[kind] = dst / src.name
            gha_utils.debug(f"{self.name}.downloads[{kind}] = {self.downloads[kind]}")

    def get_downloads_html(self):
        link_dir = pathlib.PurePath("/") / self.repo.repository
        downloads = []
        for kind, download in self.downloads.items():
            href = link_dir / download.relative_to(self.repo.working_dir)
            downloads.append(f'<li><a href="{href}">{kind}</a></li>')

        return "\n".join(downloads)

    def clone(self, name, cls=None):
        gha_utils.debug(f"{self.name}.clone({name})")
        if cls is None:
            cls = self.__class__
        clone = cls(repo=self.repo,
                    name=name,
                    rebuild_menu=True,
                    true_name=self.true_name)
        # this will clone any files in _static and _downloads, too
        clone.copy_html(src=self.dir)
        dst = clone.dir / "_downloads"
        for kind, download in self.downloads.items():
            clone.downloads[kind] = dst / download.name
            gha_utils.debug(f"{name}.downloads[{kind}] = {clone.downloads[kind]}")

        return clone

    @classmethod
    def from_variant(cls, variant):
        new_variant = cls(repo=variant.repo,
                          name=variant.name,
                          rebuild_menu=variant.rebuild_menu)
        new_variant.downloads = variant.downloads.copy()

        return new_variant

    def __lt__(self, other):
        return self.name < other.name

    @property
    def css_name(self):
        """Escape ref name to satisfy css class naming requirements

        Used to escape characters that are
        - allowed by `man git-check-ref-format`
        - disallowed by https://www.w3.org/International/questions/qa-escapes#cssescapes
        """

        esc = re.escape("!\"#$%&'()+,-./;<=>@]`{|}")
        return re.sub(f"([{esc}])", r"\\\1", self.name)

    def get_html(self):
        link_dir = (pathlib.PurePath("/") / self.repo.repository
                    / self.dir.relative_to(self.repo.working_dir))
        href = link_dir / "index.html"
        return f'<li class="ntd2d_{self.css_name}"><a href="{href}">{self.name}</a></li>'

class Version(Variant):
    """A Variant that satisfies the PEP 440 version specification

    Raises
    ------
    InvalidVersion
        If the name is not parsable by packaging.version
    """
    def __init__(self, repo, name, rebuild_menu=False):
        super().__init__(repo=repo, name=name, rebuild_menu=rebuild_menu)
        self.version = parse(name)

    def __lt__(self, other):
        if isinstance(other, Version):
            return self.version < other.version
        else:
            return super().__lt__(other)


class VariantCollection(UserList):
    def get_html(self):
        return "\n".join(variant.get_html() for variant in self)


class VariantCollector(object):
    def __init__(self, repo, current_variant):
        self.repo = repo
        self.current_variant = current_variant

        self.html_dir = repo.working_dir / "html"

        self.latest = VariantCollection()
        self.stable = VariantCollection()
        self.branches = VariantCollection()
        self.versions = VariantCollection()

        self._calc_branches_and_versions()

    @property
    def stable_versions(self):
        return VariantCollection([version
                                  for version in self.versions
                                  if not version.version.is_prerelease])

    def _calc_branches_and_versions(self):
        gha_utils.debug("VariantCollector._calc_branches_and_versions")

        names = [variant.name for variant in self.html_dir.glob("*")]

        gha_utils.debug(f"self.repo.refs = {self.repo.refs}")

        for name in names:
            gha_utils.debug(f"{name}")
            try:
                # Check if it's a PEP 440 version.
                # Retain the string literal for the tag or branch,
                # but use the Version for sorting.
                if name == self.current_variant.name:
                    # re-use existing variant
                    variant = Version.from_variant(variant=self.current_variant)
                else:
                    variant = Version(repo=self.repo, name=name)
                gha_utils.debug(f"Version({variant.name})")
            except InvalidVersion:
                if name == self.current_variant.name:
                    # re-use existing variant
                    variant = self.current_variant
                else:
                    variant = Variant(repo=self.repo, name=name)
                gha_utils.debug(f"Variant({variant.name})")

            if variant.name == "latest":
                self.latest[:] = [variant]
                continue
            elif variant.name == "stable":
                self.stable[:] = [variant]
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
                # so remove the corresponding docs.
                # current_variant may correspond to a PR, which
                # won't be listed in the refs.
                gha_utils.debug(f"Deleting {variant.name}")
                variant.rmdir()
            elif isinstance(variant, Version):
                gha_utils.debug(f"Appending version {variant.name}")
                self.versions.append(variant)
            else:
                gha_utils.debug(f"Appending branch {variant.name}")
                self.branches.append(variant)

        self.branches.sort()
        if self.current_variant.name == self.repo.default_branch:
            # replace any built documents in latest/
            # (but only do this if just rebuilt default branch of repo)
            self.latest[:] = [self.current_variant.clone("latest")]

            gha_utils.debug(f"Cloned {self.current_variant.name} to {self.latest[0].name}")

        self.versions.sort(reverse=True)
        if len(self.stable_versions) > 0:
            if self.current_variant.name == self.stable_versions[0]:
                # replace any built documents in stable/
                # (but only do this if just rebuilt highest non-prerelease version)
                self.stable[:] = [self.stable_versions[0].clone("stable",
                                                                cls=Variant)]
                gha_utils.debug(f"Cloned {self.stable_versions[0].name} to {self.stable[0].name}")

    def write_files(self, pages_url):
        gha_utils.debug(f"VariantCollector.write_files(pages_url={pages_url})")
        variants_file = VariantsFile(repo=self.repo,
                                     variants=self,
                                     pages_url=pages_url)
        variants_file.write()

        url = variants_file.get_url()

        # Need an absolute url because this gets included from
        # many different levels
        for variant in self.latest + self.stable + [self.current_variant]:
            if variant.rebuild_menu:
                MenuFile(variant=variant,
                         variants_url=url.geturl()).write()
                CSSFile(variant=variant).write()


        # This can be a relative url, because all variants should
        # be on the same server
        IndexFile(repo=self.repo, variants_url=url.path).write()
