.. NISTtheDocs2Death documentation master file, created by
   sphinx-quickstart on Sat Jul  1 09:15:57 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``NISTtheDocs2Death`` Action
============================

This is a `GitHub action <https://docs.github.com/en/actions>`_ that uses
the `Sphinx <https://www.sphinx-doc.org/>`_ tool to build documentation in
https://github.com/usnistgov projects and then host on
https://pages.nist.gov as an approximation of `ReadTheDocs
<https://readthedocs.org>`_.

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
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
