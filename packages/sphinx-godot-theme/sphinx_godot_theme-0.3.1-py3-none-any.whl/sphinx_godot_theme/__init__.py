"""Standalone sphinx theme based on the official Godot documentation theme."""
__version__ = "0.3.1"
__version_info__ = tuple((int(num) if num.isdigit() else num for num in __version__.replace("-", ".", 1).split(".")))

from pathlib import Path

_file_path = Path(__file__).parent
templates_path = [str(_file_path / Path("templates"))]
source_encoding = "utf-8-sig"
html_static_path = [str(_file_path / Path("static"))]
html_extra_path = [str(_file_path / Path("robots.txt"))]
html_css_files = [str(_file_path / Path("static") / Path("css") / Path("custom.css"))]
html_js_files = [str(_file_path / Path("static") / Path("js") / Path("custom.js"))]

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
