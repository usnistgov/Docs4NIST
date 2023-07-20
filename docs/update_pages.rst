.. _UPDATEPAGES:

``update_pages`` Sub-Action
===========================

This `GitHub action <https://docs.github.com/en/actions>`_ implements a
`Docker workflow <>`_ that is invoked by the main :ref:`NISTTHEDOCS2DEATH`
to modify the Sphinx configuration before building the documentation.

Usage
-----

This action is invoked as a step of the composite workflow of the
:ref:`NISTTHEDOCS2DEATH`.  There is no reason to invoke this action
yourself.

.. code-block:: yaml

    - name: Commit documentation changes
      uses: ./../../_actions/current/update_pages
      with:
        docs-folder: ${{ steps.borg-the-docs.outputs.borged-docs-folder }}
        separated-layout: ${{ inputs.separated-layout }}
        default-branch: ${{ github.event.repository.default_branch }}
        pages-branch: ${{ inputs.pages-branch }}
        pages-url: ${{ inputs.pages-url }}

.. note::

   This action must by synchronized with the invoked version of the
   :ref:`NISTTHEDOCS2DEATH`, but
   "``usnistgov/NISTtheDocs2Death/borg_the_docs@${{ github.action_ref }}``"
   `doesn't work
   <https://github.com/orgs/community/discussions/41927#discussioncomment-4605881>`_,
   hence the clumsy ``uses:`` statement.

Inputs
------

``docs-folder``
~~~~~~~~~~~~~~~

The folder containing your Sphinx configuration (default: "``docs/``").

``separated-layout``
~~~~~~~~~~~~~~~~~~~~

Whether Sphinx is configued to have separate :file:`source/` and
:file:`build/` directories.  (default: false).

``default-branch``
~~~~~~~~~~~~~~~~~~

The `default branch 
<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches#about-the-default-branch>`_,
as configured on GitHub (default: "``main``").

``pages-branch``
~~~~~~~~~~~~~~~~

The branch linked to your documentation server (default: "``nist-pages``").

``pages-url``
~~~~~~~~~~~~~

URL of the web server for served documentation. (default: 
"https://pages.nist.gov").
