.. _BORGTHEDOCS:

``borg_the_docs`` Sub-Action
============================

This `GitHub action <https://docs.github.com/en/actions>`_ implements a
`Docker workflow <>`_ that is invoked by the main :ref:`NISTTHEDOCS2DEATH`
to modify the Sphinx configuration before building the documentation.

Usage
-----

This action is invoked as a step of the composite workflow of the
:ref:`NISTTHEDOCS2DEATH`.  There is no reason to invoke this action
yourself.

.. code-block:: yaml

    - name: Add cruft to theme
      id: borg-the-docs
      uses: ./../../_actions/current/borg_the_docs
      with:
        docs-folder: ${{ inputs.docs-folder }}
        separated-layout: ${{ inputs.separated-layout }}

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

Outputs
-------

``borged-docs-folder``
~~~~~~~~~~~~~~~~~~~~~~

The folder containing modified Sphinx configuration modified by this 
Action.
