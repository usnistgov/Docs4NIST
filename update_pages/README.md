# `NISTtheDocs2Death`: `update_pages` Action

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
    :
    :
    - name: Commit documentation changes
      uses: ./../../_actions/current/update_pages
      with:
        docs-folder: ${{ steps.borg-the-docs.outputs.borged-docs-folder }}
        default-branch: ${{ github.event.repository.default_branch }}
        pages-branch: ${{ inputs.pages-branch }}
        pages-url: ${{ inputs.pages-url }}
    :
    :
```

This action adds built documentation for the specified branch to the `nist-pages`
branch.

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
    - name: Commit documentation changes
      uses: usnistgov/NISTtheDocs2Death/update_pages@${{ github.action_ref }}
      with:
    :
    :
```
