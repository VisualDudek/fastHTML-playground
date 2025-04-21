# type: ignore
# ruff: noqa
from fasthtml.common import *

hdrs = (
    MarkdownJS(),
    HighlightJS(langs=["python", "javascript", "html", "css"]),
)

app, rt = fast_app(
    debug=True,
    hdrs=hdrs,
)


@rt("/")
def get():
    return Titled("FastHTML", P("Let's do this!"), A(href="/hello")("Go to Hello page"))


@rt("/hello")
def get():
    return Titled("Hello, world!")


@rt("/name/{name}")
def get(name: str):
    return Titled(f"Hello {name.title()}")


content = """
Here are some _markdown_ elements.

- This is a list item
- This is another list item
- And this is a third list item

**Fenced code blocks work here.**
"""


@rt("/markdown")
def get(req):
    return Titled("Markdown rendering example", Div(content, cls="marked"))


code_example = """
import datetime
import time

for i in range(10):
    print(f"{datetime.datetime.now()}")
    time.sleep(1)
"""


@rt("/code")
def get(req):
    return Titled(
        "Markdown rendering example",
        Div(
            # The code example needs to be surrounded by
            # Pre & Code elements
            Pre(Code(code_example))
        ),
    )


serve()
