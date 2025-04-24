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
    copy_script = Script(
        """
        function copyToClipboardAndNotify(text) {
            navigator.clipboard.writeText(text).then(() => {
                console.log('Copied to clipboard:', text);
                showToast('Text copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        }

        function showToast(message) {
            const toast = document.createElement('div');
            toast.innerText = message;
            toast.style.position = 'fixed';
            toast.style.bottom = '20px';
            toast.style.right = '20px';
            toast.style.backgroundColor = '#333';
            toast.style.color = '#fff';
            toast.style.padding = '10px 20px';
            toast.style.borderRadius = '5px';
            toast.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.3)';
            toast.style.zIndex = '1000';
            document.body.appendChild(toast);

            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transition = 'opacity 0.5s';
                setTimeout(() => toast.remove(), 500);
            }, 2000);
        }
        """
    )
    return Titled(
        "FastHTML",
        copy_script,
        P("Let's do this!", onclick="copyToClipboardAndNotify(this.innerText)"),
        A(href="/hello")("Go to Hello page"),
        Div(
            P("Hello", onclick="copyToClipboardAndNotify(this.innerText)"),
            hx_get="/change",
        ),
        Div(P("Hello")),
    )


@rt("/change")
def get():
    return P("Nice to be here!")


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
    return Titled("Markdown rendering example", Div(Pre(Code(content))))


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
