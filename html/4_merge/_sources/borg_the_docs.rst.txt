.. _BORGTHEDOCS:

``borg_the_docs`` Sub-Action
============================

This `GitHub action <https://docs.github.com/en/actions>`_ is invoked by
the main :ref:`NISTTHEDOCS2DEATH` to modify the Sphinx configuration before
building the documentation.

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
        docs-folder: 'docs/'

.. note::

   This action must be synchronized with the invoked version of the
   :ref:`NISTTHEDOCS2DEATH`, but
   "``usnistgov/NISTtheDocs2Death/borg_the_docs@${{ github.action_ref }}``"
   `doesn't work
   <https://github.com/orgs/community/discussions/41927#discussioncomment-4605881>`_,
   hence the clumsy ``uses:`` statement.

Inputs
------

``docs-folder``
~~~~~~~~~~~~~~~

The folder containing your Sphinx configuration.

Outputs
-------

``borged-docs-folder``
~~~~~~~~~~~~~~~~~~~~~~

The folder containing the Sphinx configuration modified by this Action.

``borged-build-folder``
~~~~~~~~~~~~~~~~~~~~~~

The folder containing the Sphinx build outputs.


Implementation
--------------

This action implements a `Docker workflow step
<https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action>`_.
The Docker ``ENTRYPOINT`` installs any :file:`requirements.txt` in the
`Sphinx configuration directory
<https://www.sphinx-doc.org/en/master/usage/configuration.html>`_, wraps
the :file:`conf.py` file with a
:class:`~borg_the_docs_action.files.borgedconffile.BorgedConfFile` object,
and invokes
:meth:`~borg_the_docs_action.files.borgedconffile.BorgedConfFile.assimilate_theme`.


API
~~~

.. autosummary::
   :toctree: generated
   :recursive:

   borg_the_docs_action
