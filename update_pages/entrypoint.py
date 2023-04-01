#!/usr/bin/env python3
import argparse
import os

from ntd2d_action.action import NISTtheDocs2Death

def main():
    description = 'Update nist-pages branch based on sphinx builds'
    parser = argparse.ArgumentParser(
                        prog='NISTTheDocs2Death',
                        description=description)

    args = parser.parse_args()

    ntd2d = NISTtheDocs2Death(docs_dir=os.environ['INPUT_DOCS-FOLDER'],
                              default_branch=os.environ['INPUT_DEFAULT-BRANCH'],
                              pages_branch=os.environ['INPUT_PAGES-BRANCH'],
                              pages_url=os.environ['INPUT_PAGES-URL'])
    ntd2d.update_pages()


if __name__ == "__main__":
    main()
