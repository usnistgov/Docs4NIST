.. _NISTTHEDOCS2DEATH_INTRO:

``NISTtheDocs2Death``
=====================

This `GitHub action <https://docs.github.com/en/actions>`_ [#]_ uses the
`Sphinx <https://www.sphinx-doc.org/>`_ tool to build documentation in
https://github.com/usnistgov projects and then host that documentation on
https://pages.nist.gov, as an approximation of `ReadTheDocs
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
   :caption: Actions:

   nistthedocs2death
   borg_the_docs
   update_pages


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   api
   design
   customization
   QandA


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
