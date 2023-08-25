#!/usr/bin/env python3
import github_action_utils as gha_utils
import pathlib
import shlex
import subprocess

from .files import ConfFile
from .files import SphinxLog


class SphinxDocs:
    """Sphinx configuration directory."""

    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)

        if (self.docs_dir / "source" / "conf.py").is_file():
            self.source_dir = self.docs_dir / "source"
            self.build_dir = self.docs_dir / "build"
        else:
            self.source_dir = self.docs_dir
            self.build_dir = self.docs_dir / "_build"

        self.conf = self.make_conf_file()

    def make_conf_file(self):
        return ConfFile(source_dir=self.source_dir)

    @property
    def html_dir(self):
        return self.build_dir / "html"

    @property
    def epub_file(self):
        return self.build_dir / "epub" / f"{self.conf.project}.epub"

    @property
    def pdf_file(self):
        return self.build_dir / "latex" / f"{self.conf.project.lower()}.pdf"

    def build_docs(build_command):
        """Build Sphinx Documentation

        Adapted from https://github.com/ammaraskar/sphinx-action/blob/master/sphinx_action/action.py
        [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)
        """
        if not build_command:
            raise ValueError("Build command may not be empty")

        with tempfile.TemporaryDirectory() as tmpdirname:
            log_file = pathlib.Path(tmpdirname) / "sphinx-log"
            log_file.unlink(missing_ok=True)

            sphinx_options = f'--keep-going --no-color -w "{log_file}"'
            # If we're using make, pass the options as part of the SPHINXOPTS
            # environment variable, otherwise pass them straight into the command.
            build_command = shlex.split(build_command)
            if build_command[0] == "make":
                # Pass the -e option into `make`, this is specified to be
                #   Cause environment variables, including those with null values, to override macro assignments within makefiles.
                # which is exactly what we want.
                build_command += ["-e"]
                print(f"[sphinx-action] Running: {build_command}")

                return_code = subprocess.call(
                    build_command,
                    env=dict(os.environ, SPHINXOPTS=sphinx_options),
                    cwd=self.docs_dir,
                )
            else:
                build_command += shlex.split(sphinx_options)
                print(f"[sphinx-action] Running: {build_command}")

                return_code = subprocess.call(build_command, cwd=self.docs_dir)

            if log_file.exists():
                log = SphinxLog(file=log_file)
                log.parse_sphinx_warnings()

        return return_code
