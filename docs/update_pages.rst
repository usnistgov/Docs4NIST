.. _UPDATEPAGES:

``update_pages`` Sub-Action
===========================

This `GitHub action <https://docs.github.com/en/actions>`_ is invoked by
the main :ref:`NISTTHEDOCS2DEATH` to modify the Sphinx configuration before
building the documentation.

Usage
-----

This action is invoked as a step of the composite workflow of the
:ref:`NISTTHEDOCS2DEATH`.  There is no reason to invoke this action
yourself.

.. code-block:: yaml

    - name: Commit documentation changes
      uses: ./../../_actions/current/update_pages
      with:
        docs-folder: 'docs/'
        separated-layout: false
        default-branch: 'main'
        pages-branch: 'nist-pages'
        pages-url: 'https://pages.nist.gov'

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

``separated-layout``
~~~~~~~~~~~~~~~~~~~~

Whether Sphinx is configued to have separate :file:`source/` and
:file:`build/` directories.

``default-branch``
~~~~~~~~~~~~~~~~~~

The `default branch 
<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches#about-the-default-branch>`_,
as configured on GitHub.

``pages-branch``
~~~~~~~~~~~~~~~~

The branch linked to your documentation server.

``pages-url``
~~~~~~~~~~~~~

URL of the web server for served documentation.


Implementation
--------------

This action implements a `Docker workflow <>`_ that ???
