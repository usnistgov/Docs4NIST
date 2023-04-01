#!/usr/bin/env python3
import argparse
from ntd2d_action.action import NISTtheDocs2Death

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
