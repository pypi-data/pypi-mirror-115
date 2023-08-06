html_favicon = "static/images/docs_logo.svg"
supported_languages = {
    "en": "SCCD (%s) documentation in English",
}
extensions = [
    "notfound.extension",
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "sphinx_search.extension",
    "sphinx_tabs.tabs",
    "sphinxext.opengraph",
]
sphinx_tabs_nowarn = True
templates_path = ["templates"]
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}
source_encoding = "utf-8-sig"
master_doc = "index"

env_tags = os.getenv("SPHINX_TAGS")
if env_tags is not None:
    for tag in env_tags.split(","):
        print("Adding Sphinx tag: %s" % tag.strip())
        tags.add(tag.strip())  # noqa: F821
language = os.getenv("READTHEDOCS_LANGUAGE", "en")
if language not in supported_languages.keys():
    print("Unknown language: " + language)
    print("Supported languages: " + ", ".join(supported_languages.keys()))
    print("The configured language is wrong. Falling back to 'en'.")
    language = "en"
todo_include_todos = False
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "logo_only": True,
    "collapse_navigation": False,
}
html_logo = "static/images/docs_logo.svg"
html_static_path = ["static"]
htmlhelp_basename = "sccddoc"
html_extra_path = ["robots.txt"]
html_css_files = ["css/custom.css"]
html_js_files = ["js/custom.js"]
on_rtd = os.environ.get("READTHEDOCS", None) == "True"
html_title = supported_languages[language] % version
html_context = {"conf_py_path": "/"}

notfound_context = {
    "title": "Page not found",
    "body": """
        <h1>Page not found</h1>
        <p>
            Sorry, we couldn't find that page. It may have been renamed or removed
            in the version of the documentation you're currently browsing.
        </p>
        <p>
            If you're currently browsing the
            <em>latest</em> version of the documentation, try browsing the
            <a href="/en/stable/"><em>stable</em> version of the documentation</a>.
        </p>
        <p>
            Alternatively, use the
            <a href="#" onclick="$('#rtd-search-form [name=\\'q\\']').focus()">Search docs</a>
            box on the left or <a href="/">go to the homepage</a>.
        </p>
    """,
}
