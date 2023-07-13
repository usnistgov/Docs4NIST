# `NISTtheDocs2Death`: `update_pages` Action

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
    - name: Commit documentation changes
      uses: usnistgov/NISTtheDocs2Death@update_pages
      with:
        docs-folder: ${{ inputs.docs-folder }}
        separated-layout: ${{ inputs.separated-layout }}
        default-branch: ${{ github.event.repository.default_branch }}
        pages-branch: ${{ inputs.pages-branch }}
        pages-url: ${{ inputs.pages-url }}
    :
    :
```

This action adds built documentation for the specified branch to the `nist-pages`
branch.

## Design

The actions in this branch are separate from those in `main` because 
a GitHub action can either be a Docker workflow or a composite workflow, 
but not both simultaneously. The repo using the workflow invokes the 
composite workflow in `main`, which then invokes the Docker workflow in 
this branch.