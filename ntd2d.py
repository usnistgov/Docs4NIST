import git
import pathlib
import shlib

def copy_docs(from, to, repo):
# remove any previous directory of that name
    repo.index.remove(to, r=True, ignore_unmatch=True)
    shlib.copytree(from, to)
    repo.index.add(to)
    
def get_versions(docs, project, nist_pages):
    versions = []
    for version in html.glob("*"):
        href = File(f"/{project}") / version / "index.html"
        versions.append(f'<a href="{href}">{version.name}</a>')
        
    versions = "/n".join(versions)
    versions = textwrap.dedent(versions)
    versions = textwrap.indent(versions, "  ")
    
    # build index.html with available documentation versions
    return f"""
        <div class="ntd2dwrapper">
        {versions}
        </div>
    """

def get_menu():
    # static_dir="${html}/${{ github.ref_name }}/_static"
    # versions_html="${static_dir}/versions.html"
    
    src = "https://pages.nist.gov/${{ github.event.repository.name }}/includes/versions.html"
    
    return f"""
        <div class="dropdown">
          <div class="dropdown-content">
            <p>Versions</p>
              {get_iframe(src)}
            <p>Downloads</p>
            <hr>
          </div>
          <button class="dropbtn">v: ${{ github.ref_name }} ▲</button>"
        </div>
    """

def get_iframe(src):
    onload = "this.before((this.contentDocument.body||this.contentDocument).children[0]);this.remove()"
    return f"""
        <!-- Taken from https://www.filamentgroup.com/lab/html-includes/#another-demo%3A-including-another-html-file -->"
        <iframe src="{src}" onload="{onload}" ></iframe>"
    """

def get_index():
    """build index.html with available documentation versions
    """
    template_fname = File("_templates/index.html")
    if template_fname.exists():
        with open(template_fname, mode='r') as template_file):
            template = template_fname.read()
    else:
        template = """
            <!doctype html>
            <html>
            <head>
              <title>a title</title>        
            </head>
            <body>
              {versions}
            </body>
            </html>
        """

    versions = f"""
      <div class="documentation-versions">
        {write_iframe("/includes/versions.html")}
      </div>
    """
    
    return template.format(**locals())
    
def blah():
    nist_pages = pathlib.Path("..") / "nist-pages_test"
    repo = git.Repo.clone_from("https://github.com/usnistgov/steppyngstounes.git", 
                               to_path=nist_pages, 
                               branch="nist-pages", single_branch=True)
    
# cd nist-pages
# 
# html="html"

    build = "../${{ inputs.docs-folder }}_build/html"
    branch = "${html}/${{ github.ref_name }}"
    
    # store built documents in directory named for current branch
    copy_docs(build, nist_pages / html / ${{ github.ref_name }}, repo)
    
    # store built documents in latest/
    # (but only do this for default branch of repo)
    if ${{ github.ref_name == github.event.repository.default_branch }}:
        copy_docs(build, nist_pages / html / "latest", repo)

    
    # jekyll conflicts with sphinx' underlined directories and files
    (nist_pages / ".nojekyll").touch()

    with open(nist_pages / "_includes" / "ntd2d_versions.html", mode='w') as version_file:
        version_file.write(get_versions(html, "${{ github.event.repository.name }}")

    with open(..., mode='w', as menu_file):
        menu_file.write(get_menu())

    with open(..., mode='w', as index_file):
        index_file.write(get_index())

if __name__ == "__main__":
    pass
