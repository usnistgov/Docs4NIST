#!/usr/bin/env python3
import github_action_utils as gha_utils
import os

import sys
gha_utils.debug(f"sys.path = {sys.path}")

from borg_the_docs_action.files import BorgedConfFile


def main():
    if os.environ['INPUT_SEPARATED-LAYOUT'] == 'true':
        source_rel = "source"
    else:
        source_rel = ""

    conf = BorgedConfFile(docs_dir=os.environ['INPUT_DOCS-FOLDER'],
                          source_rel=source_rel)
    conf.assimilate_theme(name="ntd2d")
    conf.write()

    gha_utils.set_output("borged-docs-folder", conf.docs_dir.as_posix())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        gha_utils.error(e.__traceback__)
        raise
