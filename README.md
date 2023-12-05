# Docs4NIST Action

This is a GitHub action that uses sphinx to build documentation and then
host on <https://pages.nist.gov> as an approximation of
[ReadTheDocs](https://readthedocs.org).

## Usage

- [Configure your repo for publishing on `pages.nist.gov`](https://github.com/usnistgov/pages-root/wiki/Configuring-your-repo-for-publishing-on-pages.nist.gov)
- Create a workflow, such as `.github/workflows/Docs4NIST.yml`:

    ```yaml
    name: "Build Documentation"

    on: [push, pull_request, delete]

    jobs:
      docs:
        runs-on: ubuntu-latest
        steps:
          - uses: usnistgov/Docs4NIST@0.5
            with:
              docs-folder: docs/
              formats: |-
                epub
                pdf
    ```

**Note:**
[GitHub Actions' YAML implementation does not support list or array](https://github.com/actions/toolkit/issues/184)
elements, so
[use a multiline string](https://stackoverflow.com/questions/75420197/how-to-use-array-input-for-a-custom-github-actions)
to declare formats, as illustrated above.

The self-generated documentation for this action is available at
<https://pages.nist.gov/Docs4NIST>.
