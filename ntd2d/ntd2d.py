#!/usr/bin/env python3
import github_action_utils as gha_utils
import os
import subprocess
import sys
import traceback

from ntd2d_action.sphinxdocs import SphinxDocs
from ntd2d_action.borgedsphinxdocs import BorgedSphinxDocs
from ntd2d_action.repository import Repository


def main():
    with gha_utils.group("Borg the Docs", use_subprocess=True):
        original_docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])
        docs = BorgedSphinxDocs(original_docs=original_docs)
        docs.assimilate_theme(name="ntd2d")
    
        gha_utils.set_output("borged-build-folder", docs.build_dir.as_posix())

    pre_build_command = os.environ['INPUT_PRE-BUILD-COMMAND']
    if pre_build_command != "":
        with gha_utils.group("Executing pre-build-command", use_subprocess=True):
            gha_utils.debug(f"pre-build-command: {pre_build_command}", use_subprocess=True)
            try:
                subprocess.check_output(pre_build_command, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                gha_utils.error(e.stdout.decode('utf-8'), use_subprocess=True)
                raise

    with gha_utils.group("Build HTML", use_subprocess=True):
        docs.build_docs(build_command=os.environ['INPUT_BUILD-HTML-COMMAND'])

    formats = os.environ['INPUT_FORMATS'].lower().split()

    if "pdf" in formats:
        with gha_utils.group("Build PDF", use_subprocess=True):
            docs.build_docs(build_command=os.environ['INPUT_BUILD-PDF-COMMAND'])

    if "epub" in formats:
        with gha_utils.group("Build ePub", use_subprocess=True):
            docs.build_docs(build_command=os.environ['INPUT_BUILD-EPUB-COMMAND'])

    with gha_utils.group("Update Pages", use_subprocess=True):
        repo = Repository(server_url=os.environ['GITHUB_SERVER_URL'],
                          repository=os.environ['GITHUB_REPOSITORY'],
                          branch=os.environ['INPUT_PAGES-BRANCH'],
                          default_branch=os.environ['INPUT_DEFAULT-BRANCH'],
                          docs=docs,
                          pages_url=os.environ['INPUT_PAGES-URL'])

        repo.update_pages(branch=os.environ['SANITIZED_REF_NAME'],
                          sha=os.environ['GITHUB_SHA'])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        gha_utils.error("".join(traceback.format_exception(e)), use_subprocess=True)
        sys.exit(1)
