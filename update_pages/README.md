# NISTtheDocs2Death Action

This is a ***branch*** of a GitHub action that uses sphinx to build documentation and then
host on <https://pages.nist.gov> as an approximation of
[ReadTheDocs](https://readthedocs.org). This branch is invoked by the `main` 
branch when it calls the following steps within its composite action:

```yaml
runs:
  using: "composite"
  steps:
    :
    :
    - name: Modify documentation
      uses: usnistgov/NISTtheDocs2Death@workhorse
      with:
        action: borg_the_docs
        docs-folder: ${{ inputs.docs-folder }}
    :
    :
    - name: Commit documentation changes
      uses: usnistgov/NISTtheDocs2Death@workhorse
      with:
        action: update_pages
        docs-folder: ${{ inputs.docs-folder }}
        default-branch: ${{ github.event.repository.default_branch }}
        pages-branch: ${{ inputs.pages-branch }}
        pages-url: ${{ inputs.pages-url }}
    :
    :
```

## Sub-actions

This workflow takes an `action` parameter:

- `borg_the_docs`

    Modifies the [Sphinx configuration file]() with an [inherited theme]().
    This theme adds a version pop-up menu and a NIST header and footer to
    every page.
  
- `update_pages`

    Adds built documentation for the specified branch to the `nist-pages` 
    branch.

## Design

The actions in this branch are separate from those in `main` because 
a GitHub action can either be a Docker workflow or a composite workflow, 
but not both simultaneously. The repo using the workflow invokes the 
composite workflow in `main`, which then invokes the Docker workflow in 
this branch.