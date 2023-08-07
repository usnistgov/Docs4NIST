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
         - uses: usnistgov/NISTtheDocs2Death@0.1
           with:
             docs-folder: docs/
             pages-branch: 'nist-pages'
             pages-url: 'https://pages.nist.gov'
             formats: ''
             build-html-command: make html
             build-epub-command: make epub
             build-pdf-command: make epub
             pre-build-command: ''

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

The command used by |sphinxaction|_ to build your html documentation.

``build-epub-command``
~~~~~~~~~~~~~~~~~~~~~~

The command used by |sphinxaction|_ to build your ePUB documentation.

``build-pdf-command``
~~~~~~~~~~~~~~~~~~~~~

The command used by |sphinxaction|_ to build your PDF documentation.

pre-build-command
~~~~~~~~~~~~~~~~~

Run by |sphinxaction|_ before the build command.  You can use this to install
system level dependencies, for example, with "``apt-get update -y && apt-get
install -y perl``".

Implementation
--------------

This action implements a `composite workflow
<https://docs.github.com/en/actions/creating-actions/creating-a-composite-action>`_
with the following major steps:

1. |checkout|_
2. :ref:`BORGTHEDOCS`
3. |sphinxaction|_
4. :ref:`UPDATEPAGES`
5. |github-push-action|_
6. |upload-artifact|_


.. |checkout|       replace:: ``actions/checkout``
.. _checkout:       https://github.com/actions/checkout
.. |sphinxaction|   replace::   ``usnistgov/sphinx-action``
.. _sphinxaction:   https://github.com/usnistgov/sphinx-action
.. |github-push-action|  replace:: ``ad-m/github-push-action``
.. _github-push-action:  https://github.com/ad-m/github-push-action
.. |upload-artifact|     replace:: ``actions/upload-artifact``
.. _upload-artifact:     https://github.com/actions/upload-artifact
