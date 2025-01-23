.. _DOCS4NIST_INTRO:

``Docs4NIST``
=============

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
- `Enable GitHub Actions for your repo
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository>`_
  and select "Allow all actions and reusable workflows" (you may need to
  submit a request to devops@nist.gov to enable this for you).
- For each branch of your repository where you want to host documentation, 
  add a workflow, such as :file:`.github/workflows/Docs4NIST.yml`:

.. code-block:: yaml

   name: "Build Documentation"

   on: [push, pull_request, delete]

   jobs:
     docs:
       runs-on: ubuntu-latest
       steps:
         - uses: usnistgov/Docs4NIST@0.6
           with:
             docs-folder: docs/
             formats: |-
               epub
               pdf

See :ref:`DOCS4NIST` for more information about configuration of
this workflow.

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   :hidden:

   customization
   QandA
   API

.. toctree::
   :maxdepth: 1
   :caption: Actions:
   :hidden:

   docs4nist
   ntd2d


Indices and tables
------------------

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
