Customization
=============

NISTtheDocs2Death uses two sets of templates that determine the appearance 
of the hosted documentation.

``borg_the_docs`` templates
---------------------------

The first set of templates is used by the :ref:`BORGTHEDOCS` to modify the
Sphinx configuration.

These templates can be customized by forking this repository.

|conf.py|_
~~~~~~~~~~

This template file overlays the `html_theme
<https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme>`_
you chose for your documentation with the ``ntd2d`` theme, described next.

.. NTD2DTHEME:

|ntd2d|_
~~~~~~~~

This template directory provides a `Sphinx theme
<https://www.sphinx-doc.org/en/master/development/theming.html>`_ that
modifies your chosen documentation theme.

|layout.html|_
..............

This template file inserts standard NIST headers and footers and a dropdown
menu that allows selecting different versions of your documentation.

|static/ntd2d.css_t|_
.....................

This template file controls the appearance of the dropdown menu.

.. |conf.py|  replace:: :file:`conf.py`
.. _conf.py:  https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/borg_the_docs_action/files/templates/conf.py
.. |ntd2d|    replace:: :file:`ntd2d/`
.. _ntd2d:    https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/borg_the_docs_action/files/templates/ntd2d/
.. |layout.html|  replace:: :file:`ntd2d/layout.html`
.. _layout.html:  https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/borg_the_docs_action/files/templates/ntd2d/layout.html
.. |static/ntd2d.css_t|  replace:: :file:`ntd2d/static/ntd2d.css_t`
.. _static/ntd2d.css_t:  https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/borg_the_docs_action/files/templates/ntd2d/static/ntd2d.css_t

``update_pages`` templates
--------------------------

The second set of tempaltes is used by the :ref:`UPDATEPAGES` sub-action to
create the pages on the hosting site that enable switching between
different documentation variants.

You can customize any of these templates copying them to a
:file:`_templates/` directory at the root of your `nist-pages` branch and
editing them to suit.

These templates use `Python string format syntax
<https://docs.python.org/3/tutorial/inputoutput.html#the-string-format-method>`_
(Sphinx and pages.nist.gov already fight over Jekyll templating, so we're
not getting fancy, here).

.. _DOWNLOADS_HTML:

|downloads.html|_
~~~~~~~~~~~~~~~~~

A section inserted into :ref:`MENU_HTML` if a documentation variant has
any downloadable output, e.g., PDF or ePUB.

Available subsitution keywords are:

- ``downloads``: A pre-formatted string with each downloadable output
  formatted by :ref:`DOWNLOAD_ITEM_HTML`.

.. _DOWNLOAD_ITEM_HTML:

|download_item.html|_
~~~~~~~~~~~~~~~~~~~~~

Formats a link to a single downloadable output.

Available subsitution keywords are:

- ``href``: URL of the downloadable output.
- ``kind``: Type of downloadable output, e.g., PDF or ePUB.

.. _INDEX_HTML:

|index.html|_
~~~~~~~~~~~~~

The default page for your documentation displayed at
https://pages.nist.gov/`{repository}`.

Available subsitution keywords are:

- ``owner``: The GitHub
  `user or organization
  <https://docs.github.com/en/get-started/learning-about-github/types-of-github-accounts>`_
  for your repository.
- ``repository``: The name of your repository.
- ``variants``: The result of filling the :ref:`VARIANTS_HTML` template.

.. _MENU_HTML:

|menu.html|_
~~~~~~~~~~~~

The dropdown menu that allows selecting different branches and tags of your
documentation.

Available subsitution keywords are:

- ``downloads``: The result of filling the :ref:`DOWNLOADS_HTML` template.
- ``tree_url``: The GitHub URL corresponding to this branch or tag.
- ``variant``: The branch or tag name of the active documentation.
- ``variants``: The result of filling the :ref:`VARIANTS_HTML` template.

.. _NTD2D_ACTIVE_CSS:

|ntd2d_active.css|_
~~~~~~~~~~~~~~~~~~~

Style sheet that controls the appearance of the active tag or branch in the
dropdown menu.

Available subsitution keywords are:

- ``variant``: The branch or tag name of the active documentation.

.. _VARIANTS_HTML:

|variants.html|_
~~~~~~~~~~~~~~~~

Lists tags and branches that are :ref:`configured <USAGE>` to serve
documentation with this Action.

Available subsitution keywords are:

- ``branches``: A pre-formatted string with each git branch formatted by
  :ref:`VARIANT_ITEM_HTML`.
- ``latest``: A pre-formatted string with the ``HEAD`` of the
  `default GitHub branch
  <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches#about-the-default-branch>`_
  formatted by :ref:`VARIANT_ITEM_HTML`.
- ``stable``: A pre-formatted string with the ``stable_version`` that has the
  highest version identifier, as formatted by :ref:`VARIANT_ITEM_HTML`.
- ``stable_versions``: A pre-formatted string with the tags or branches
  that satisfy the :pep:`440` version specification and aren't
  `pre-releases <https://peps.python.org/pep-0440/#pre-releases>`_,
  each formatted by :ref:`VARIANT_ITEM_HTML`.
- ``versions``: A pre-formatted string with the tags or branches that
  satisfy the :pep:`440` version specification, each formatted by
  :ref:`VARIANT_ITEM_HTML`.

.. _VARIANT_ITEM_HTML:

|variant_item.html|_
~~~~~~~~~~~~~~~~~~~~~

Formats a link to a single tag or branch.

Available subsitution keywords are:

- ``href``: URL of the downloadable output.
- ``kind``: Type of downloadale output, e.g., PDF or ePUB.


.. |downloads.html|   replace:: :file:`downloads.html`
.. _downloads.html:   https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/update_pages_action/files/templates/downloads.html
.. |download_item.html| replace:: :file:`download_item.html`
.. _download_item.html: https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/update_pages_action/files/templates/download_item.html
.. |index.html|       replace:: :file:`index.html`
.. _index.html:       https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/update_pages_action/files/templates/index.html
.. |menu.html|        replace:: :file:`menu.html`
.. _menu.html:        https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/update_pages_action/files/templates/menu.html
.. |ntd2d_active.css| replace:: :file:`ntd2d_active.css`
.. _ntd2d_active.css: https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/update_pages_action/files/templates/ntd2d_active.css
.. |variants.html|    replace:: :file:`variants.html`
.. _variants.html:    https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/update_pages_action/files/templates/variants.html
.. |variant_item.html| replace:: :file:`variant_item.html`
.. _variant_item.html: https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/update_pages_action/files/templates/variant_item.html

