.. _UPDATEPAGES:

``update_pages`` Sub-Action
===========================

This `GitHub action <https://docs.github.com/en/actions>`_ is invoked by
the main :ref:`NISTTHEDOCS2DEATH` to move built documentation into your
designated :ref:`PAGES_BRANCH`.

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
        default-branch: 'main'
        pages-branch: 'nist-pages'
        pages-url: 'https://pages.nist.gov'
        pip-requirements: ''
        conda-environment: ''

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

``default-branch``
~~~~~~~~~~~~~~~~~~

The `default branch 
<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches#about-the-default-branch>`_,
as configured on GitHub.

.. _PAGES_BRANCH:

``pages-branch``
~~~~~~~~~~~~~~~~

The branch linked to your documentation server.

``pages-url``
~~~~~~~~~~~~~

URL of the web server for served documentation.

``pip-requirements``
~~~~~~~~~~~~~~~~~~~~

The path to the pip requirements file, relative to the root of the project.

``conda-environment``
~~~~~~~~~~~~~~~~~~~~~

The path to the Conda environment file, relative to the root of the
project.


Implementation
--------------

This action implements a `Docker workflow step
<https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action>`_.
The Docker ``ENTRYPOINT`` wraps the `Sphinx configuration directory
<https://www.sphinx-doc.org/en/master/usage/configuration.html>`_ in a
:class:`~update_pages_action.sphinxdocs.SphinxDocs` object, wraps the
:envvar:`GITHUB_REPOSITORY` in a
:class:`~update_pages_action.repository.Repository` object, and invokes
:meth:`~update_pages_action.repository.Repository.update_pages`.

API
~~~

.. autosummary::
   :toctree: generated
   :recursive:

   update_pages_action
