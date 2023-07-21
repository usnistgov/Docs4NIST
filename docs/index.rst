.. _NISTTHEDOCS2DEATH:

``NISTtheDocs2Death`` Action
============================

This `GitHub action <https://docs.github.com/en/actions>`_ [#]_ implements a
`composite  workflow <>`_ that uses the `Sphinx <https://www.sphinx-doc.org/>`_
tool to build documentation in https://github.com/usnistgov projects and
then host on https://pages.nist.gov as an approximation of `ReadTheDocs
<https://readthedocs.org>`_.

.. _USAGE:

Usage
-----

- `Configure your repo for publishing on pages.nist.gov
  <https://github.com/usnistgov/pages-root/wiki/Configuring-your-repo-for-publishing-on-pages.nist.gov>`_.
- For each branch of your repository where you want to host documentation, 
  add a workflow, such as :file:`.github/workflows/NISTtheDocs2Death.yml`:

.. code-block:: yaml

   name: "Build Documentation"

   on: [push, pull_request, delete]

   jobs:
     docs:
       runs-on: ubuntu-latest
       steps:
         - uses: usnistgov/NISTtheDocs2Death@main
           with:
             docs-folder: docs/
             formats: |-
               epub
               pdf

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   borg_the_docs
   update_pages
   customization
   QandA

Inputs
------

``docs-folder``
~~~~~~~~~~~~~~~

The folder containing your Sphinx configuration (default: "``docs/``").

``separated-layout``
~~~~~~~~~~~~~~~~~~~~

Whether Sphinx is configured to have separate :file:`source/` and
:file:`build/` directories or if the source files and the :file:`_build/`
directory is inside the configuration directory.  (default: false).

``pages-branch``
~~~~~~~~~~~~~~~~

The branch linked to your documentation server (default: "``nist-pages``").

``pages-url``
~~~~~~~~~~~~~

URL of the web server for served documentation. (default: 
"https://pages.nist.gov").

``formats``
~~~~~~~~~~~

Type(s) of output desired in addition to html (``pdf``, and/or ``epub``) 
(default: "").

.. note::

   `GitHub Actions' YAML implementation does not support list or array elements
   <https://github.com/actions/toolkit/issues/184>`_, so
   `use a multiline string
   <https://stackoverflow.com/questions/75420197/how-to-use-array-input-for-a-custom-github-actions>`_
   to declare formats, as illustrated above.

``build-html-command``
~~~~~~~~~~~~~~~~~~~~~~

The command used by |sphinxaction|_ to build your html documentation
(default: "``make html``").

``build-epub-command``
~~~~~~~~~~~~~~~~~~~~~~

The command used by |sphinxaction|_ to build your ePUB documentation
(default: "``make epub``).

``build-pdf-command``
~~~~~~~~~~~~~~~~~~~~~

The command used by |sphinxaction|_ to build your PDF documentation 
(default: "``make latexpdf``").

pre-build-command
~~~~~~~~~~~~~~~~~

Run by |sphinxaction|_ before the build command.  You can use this to install
system level dependencies, for example, with "``apt-get update -y && apt-get
install -y perl``" (default: "").



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

----

.. [#] Certain commercial firms and trade names are identified in this
    document in order to specify the installation and usage procedures
    adequately, or to provide context.  Such identification is not intended
    to imply recommendation or endorsement by the `National Institute of
    Standards and Technology <https://www.nist.gov>`_, nor is it intended
    to imply that related products are necessarily the best available for
    the purpose.



.. |sphinxaction|   replace::   ``usnistgov/sphinx-action``
.. _sphinxaction:   https://github.com/usnistgov/sphinx-action
