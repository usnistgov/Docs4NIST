.. _NISTTHEDOCS2DEATH:

``NISTtheDocs2Death`` Action
============================

This `GitHub action <https://docs.github.com/en/actions>`_ uses the `Sphinx
<https://www.sphinx-doc.org/>`_ tool to build documentation in
https://github.com/usnistgov projects and then host on
https://pages.nist.gov as an approximation of `ReadTheDocs
<https://readthedocs.org>`_.

Usage
-----

This action is invoked by adding a workflow file to your repository, such 
as :file:`.github/workflows/NISTtheDocs2Death.yml`:

.. code-block:: yaml

   name: "Build Documentation"

   on: [push, pull_request, delete]

   jobs:
     docs:
       runs-on: ubuntu-latest
       steps:
         - uses: usnistgov/NISTtheDocs2Death@0.4
           with:
             docs-folder: docs/
             pages-branch: 'nist-pages'
             pages-url: 'https://pages.nist.gov'
             formats: ''
             build-html-command: make html
             build-epub-command: make epub
             build-pdf-command: make latexpdf
             pre-build-command: ''
             apt-packages: ''
             pip-requirements: ''
             conda-environment: ''
             push-pulls-pages: false
             include-header-footer: true

Inputs
------

``docs-folder``
~~~~~~~~~~~~~~~

The folder containing your Sphinx configuration.

.. _PAGES_BRANCH:

``pages-branch``
~~~~~~~~~~~~~~~~

The branch linked to your documentation server.

.. _PAGES_URL:

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

The command used by |sphinxaction|_ to build your html documentation.

``build-epub-command``
~~~~~~~~~~~~~~~~~~~~~~

The command used by |sphinxaction|_ to build your ePUB documentation.

``build-pdf-command``
~~~~~~~~~~~~~~~~~~~~~

The command used by |sphinxaction|_ to build your PDF documentation.

``pre-build-command``
~~~~~~~~~~~~~~~~~~~~~

Run by |sphinxaction|_ before the build command.  You can use this to install
system level dependencies, for example, with "``apt-get update -y && apt-get
install -y perl``", although those are better installed with
:ref:`APTPACKAGES`.

.. _APTPACKAGES:

``apt-packages``
~~~~~~~~~~~~~~~~~~~~

List of any `APT <https://en.wikipedia.org/wiki/APT_(software)>`_ packages
that should be installed.

.. _PIPREQUIREMENTS:

``pip-requirements``
~~~~~~~~~~~~~~~~~~~~

The path to the pip requirements file, relative to the root of the project.

.. _CONDAENVIRONMENT:

``conda-environment``
~~~~~~~~~~~~~~~~~~~~~

The path to the Conda environment file, relative to the root of the
project.

``push-pulls-pages``
~~~~~~~~~~~~~~~~~~~~

Whether the results of pull requests should be pushed to
:ref:`PAGES_BRANCH`.  For
`security <https://github.blog/2020-08-03-github-actions-improvements-for-fork-and-pull-request-workflows/>`_
`reasons <https://securitylab.github.com/research/github-actions-preventing-pwn-requests/>`_,
this is impossible for pull requests from repository forks, but it is
generally undesirable in any case (they appear with cryptic names like
`merge_1234` and are redundant to the branch the pull is from).  As long as
this action is set to run `on: push`, then any build products from branches
in the same repository will appear at :ref:`PAGES_URL`.

``include-header-footer``
~~~~~~~~~~~~~~~~~~~~~~~~~

Whether to insert the
`NIST header and footer <https://pages.nist.gov/nist-header-footer>`_.
This content conflicts with, e.g.,
`sphinx_rtd_theme <https://sphinx-rtd-theme.readthedocs.io/>`_.

Implementation
--------------

This action implements a `composite workflow
<https://docs.github.com/en/actions/creating-actions/creating-a-composite-action>`_
with the following major steps:

1. |checkout|_
2. :ref:`NTD2D`
3. |github-push-action|_
4. |upload-artifact|_


.. |checkout|       replace:: ``actions/checkout``
.. _checkout:       https://github.com/actions/checkout
.. |sphinxaction|   replace::   ``usnistgov/sphinx-action``
.. _sphinxaction:   https://github.com/usnistgov/sphinx-action
.. |github-push-action|  replace:: ``ad-m/github-push-action``
.. _github-push-action:  https://github.com/ad-m/github-push-action
.. |upload-artifact|     replace:: ``actions/upload-artifact``
.. _upload-artifact:     https://github.com/actions/upload-artifact
