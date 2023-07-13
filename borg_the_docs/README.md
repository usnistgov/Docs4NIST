# `NISTtheDocs2Death`: `borg_the_docs` Action

This action is not intended to be called by users.  It is invoked by a
GitHub action that uses sphinx to build documentation and then host on
<https://pages.nist.gov> as an approximation of
[ReadTheDocs](https://readthedocs.org).  This sub-action is invoked by the
root directory when it calls the following steps within its composite
action:

```yaml
runs:
  using: "composite"
  steps:
    :
    :
    - name: Symlink current Actions repo
      working-directory: ${{ github.action_path }}
      shell: bash
      run: ln -fs $(realpath ./)  /home/runner/work/_actions/current
    - name: Add cruft to theme
      id: borg-the-docs
      uses: ./../../_actions/current/borg_the_docs
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

The action in this directory is separate from that in the base directory
because a GitHub action can either be a Docker workflow or a composite
workflow, but not both simultaneously.  The repo using the workflow invokes
the composite workflow in `main`, which then invokes the Docker workflow in
this directory.

The following [sensible syntax is not
supported](https://github.com/orgs/community/discussions/41927):

```yaml
runs:
  using: "composite"
  steps:
    :
    :
    - name: Add cruft to theme
      id: borg-the-docs
      uses: usnistgov/NISTtheDocs2Death/borg_the_docs@${{ github.action_ref }}
      with:
        docs-folder: ${{ inputs.docs-folder }}
        separated-layout: ${{ inputs.separated-layout }}
    :
    :
```
