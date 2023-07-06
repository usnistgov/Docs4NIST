# `NISTtheDocs2Death`: `borg_the_docs` Action

This is a ***branch*** of a GitHub action that uses sphinx to build documentation and then
host on <https://pages.nist.gov> as an approximation of
[ReadTheDocs](https://readthedocs.org). This branch is invoked by the `main` 
branch when it calls the following step within its composite action:

```yaml
runs:
  using: "composite"
  steps:
    :
    :
    - name: Modify documentation
      uses: usnistgov/NISTtheDocs2Death@borg_the_docs
      with:
        docs-folder: ${{ inputs.docs-folder }}
        separated-layout: ${{ inputs.separated-layout }}
    :
    :
```

This modifies the [Sphinx configuration
file](https://www.sphinx-doc.org/en/master/usage/configuration.html) with
an [inherited
theme](https://www.sphinx-doc.org/en/master/development/theming.html).
This theme adds a version pop-up menu and a NIST header and footer to every
page.

## Design

The action in this branch is separate from that in `main` because
a GitHub action can either be a Docker workflow or a composite workflow, 
but not both simultaneously. The repo using the workflow invokes the 
composite workflow in `main`, which then invokes the Docker workflow in 
this branch.