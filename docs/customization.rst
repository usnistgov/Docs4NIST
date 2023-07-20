Customization
=============

NISTtheDocs2Death uses two sets of templates that determine the appearance 
of the hosted documentation.

1. The first set is used by the :ref:`BORGTHEDOCS` to modify the 

   These templates can be customized by forking this repository.

   - `conf.py <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/ntd2d_action/files/templates/conf.py>`_
     overlays the `html_theme <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme>`_
     you chose for your documentation with the ``ntd2d`` theme, described next.
   - `ntd2d/ <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/ntd2d_action/files/templates/ntd2d/>`_
     is a `Sphinx theme <https://www.sphinx-doc.org/en/master/development/theming.html>`_
     that modifies your chosen documentation theme.

     - `layout.html <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/ntd2d_action/files/templates/ntd2d/layout.html>`_
       inserts standard NIST headers and footers and a dropdown menu
       that allows selecting different versions of your documentation.
     - `static/ntd2d.css_t <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/borg_the_docs/ntd2d_action/files/templates/ntd2d/static/ntd2d.css_t>`_
       controls the appearance of the dropdown menu.

2. The second set is used by the :ref:`UPDATEPAGES` sub-action to modify the 

   You can customize any of these templates copying them to a
   :file:`_templates/` directory at the root of your `nist-pages` branch
   and editing them to suit.

   These templates use
   `Python string format syntax 
   <https://docs.python.org/3/tutorial/inputoutput.html#the-string-format-method>`_
   (Sphinx and pages.nist.gov already fight over Jekyll templating, so
   we're not getting fancy, here).

   - `downloads.html <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/ntd2d_action/files/templates/downloads.html>`_:
     A section inserted into :file:`menu.html` if a documentation variant
     has any downloadable output (e.g., PDF or ePUB).

     Available subsitution keywords are:

     - ``downloads``: A pre-formatted string with HTML ``<li>`` list items 
       corresponding to each downloadable output.

   - `index.html <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/ntd2d_action/files/templates/index.html>`_:
     The default page for your documentation displayed at 
     https://pages.nist.gov/`{repository}`.

     Available subsitution keywords are:

     - ``owner``: The GitHub 
       `user or organization 
       <https://docs.github.com/en/get-started/learning-about-github/types-of-github-accounts>`_
       for your repository.
     - ``repository``: The name of your repository.
     - ``variants``: The result of filling the :file:`variants.html` 
       template.

   - `menu.html <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/ntd2d_action/files/templates/menu.html>`_:
     The dropdown menu that allows selecting different branches and tags 
     of your documentation.

     Available subsitution keywords are:

     - ``downloads``: The result of filling the :file:`downloads.html` 
       template.
     - ``tree_url``: The GitHub URL corresponding to this branch or tag.
     - ``variant``: The branch or tag name of the active documentation.
     - ``variants``: The result of filling the :file:`variants.html` 
       template.

   - `ntd2d_active.css <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/ntd2d_action/files/templates/ntd2d_active.css>`_:
     controls the appearance of the active tag or branch in the dropdown 
     menu.

     Available subsitution keywords are:

     - ``variant``: The branch or tag name of the active documentation.

   - `variants.html <https://github.com/usnistgov/NISTtheDocs2Death/blob/main/update_pages/ntd2d_action/files/templates/variants.html>`_:
     Lists tags and branches that are :ref:`configured <USAGE>` to serve
     documentation with this Action.

     Available subsitution keywords are:

     - ``branches``: A pre-formatted string with HTML ``<li>`` list items 
       corresponding to each git branch.
     - ``latest``: A pre-formatted string with an HTML ``<li>`` list item 
       corresponding to the ``HEAD`` of the `default GitHub branch 
       <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches#about-the-default-branch>`_.
     - ``stable``: A pre-formatted string with an HTML ``<li>`` list item 
       corresponding to the the ``stable_version`` with the highest 
       version identifier.
     - ``stable_versions``: A pre-formatted string with HTML ``<li>`` list items 
       corresponding to the tags or branches that satisfy the :pep:`440`
       version specification and aren't
       `pre-releases <https://peps.python.org/pep-0440/#pre-releases>`_.
     - ``versions``: A pre-formatted string with HTML ``<li>`` list items 
       corresponding to the tags or branches that satisfy the :pep:`440`
       version specification.

