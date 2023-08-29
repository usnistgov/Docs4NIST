.. _NTD2D:

``ntd2d`` Sub-Action
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
      uses: ./../../_actions/current/ntd2d
      with:
        docs-folder: docs/
        pages-branch: 'nist-pages'
        pages-url: 'https://pages.nist.gov'
        formats: ''
        build-html-command: make html
        build-epub-command: make epub
        build-pdf-command: make epub
        pre-build-command: ''
        apt-packages: ''
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

``pages-branch``
~~~~~~~~~~~~~~~~

The branch linked to your documentation server.

``pages-url``
~~~~~~~~~~~~~

URL of the web server for served documentation.

``formats``
~~~~~~~~~~~

Type(s) of output desired in addition to html (``pdf``, and/or ``epub``).

.. note::

   `GitHub Actions' YAML implementation does not support list or array elements
   <https://github.com/actions/toolkit/issues/184>`_, so
   `use a multiline string
   <https://stackoverflow.com/questions/75420197/how-to-use-array-input-for-a-custom-github-actions>`_
   to declare formats, e.g.,

   .. code-block:: yaml

             formats: |-
               epub
               pdf


``build-html-command``
~~~~~~~~~~~~~~~~~~~~~~

The command used to build your html documentation.

``build-epub-command``
~~~~~~~~~~~~~~~~~~~~~~

The command used to build your ePUB documentation.

``build-pdf-command``
~~~~~~~~~~~~~~~~~~~~~

The command used to build your PDF documentation.

``pre-build-command``
~~~~~~~~~~~~~~~~~~~~~

Run before the build command.  You can use this to install
system level dependencies, for example, with "``apt-get update -y && apt-get
install -y perl``", although those are better installed with
:ref:`APTPACKAGES`.

``apt-packages``
~~~~~~~~~~~~~~~~~~~~

List of any `APT <https://en.wikipedia.org/wiki/APT_(software)>`_ packages
that should be installed.

``pip-requirements``
~~~~~~~~~~~~~~~~~~~~

The path to the pip requirements file, relative to the root of the project.

``conda-environment``
~~~~~~~~~~~~~~~~~~~~~

The path to the Conda environment file, relative to the root of the
project.


Outputs
-------

``borged-build-folder``
~~~~~~~~~~~~~~~~~~~~~~~

The folder containing the Sphinx build outputs.


Implementation
--------------

This action implements a `Docker workflow step
<https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action>`_.
The Docker ``ENTRYPOINT``
- installs any specified :ref:`APTPACKAGES`, :ref:`PIPREQUIREMENTS`,
  and :ref:`CONDAENVIRONMENT`.
- wraps the `Sphinx configuration directory
  <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_ in a
  :class:`~ntd2d_action.borgedsphinxdocs.BorgedSphinxDocs` object,
- invokes
  :meth:`~ntd2d_action.borgedsphinxdocs.BorgedSphinxDocs.assimilate_theme`
- executes any :envvar:`INPUT_PRE-BUILD-COMMAND`,
- invokes
  :meth:`~ntd2d_action.borgedsphinxdocs.BorgedSphinxDocs.build_docs` for
  html and any other formats specified in :envvar:`INPUT_FORMATS`,
- wraps the
  :envvar:`GITHUB_REPOSITORY` in a
  :class:`~ntd2d_action.repository.Repository` object,
- invokes
  :meth:`~ntd2d_action.repository.Repository.update_pages`.

API
~~~

.. autosummary::
   :toctree: generated
   :recursive:

   ntd2d_action
