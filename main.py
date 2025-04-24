# type: ignore
# ruff: noqa
from fasthtml.common import *
from dotenv import load_dotenv

load_dotenv()

debug_str = os.getenv("DEBUG", "false")
live_str = os.getenv("LIVE", "false")


def str_to_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes", "on")


DEBUG = str_to_bool(debug_str)
LIVE = str_to_bool(live_str)

print(f"{DEBUG=}\n{LIVE=}")


hdrs = (
    MarkdownJS(),
    HighlightJS(langs=["python", "javascript", "html", "css"]),
)

app, rt = fast_app(
    debug=DEBUG,
    live=LIVE,
    hdrs=hdrs,
)


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


# @rt("/")
# def get():
#     return Titled(
#         "FastHTML",
#         A(href="/grid")("Go to Grid page"),
#         copy_script,
#         P("Let's do this!", onclick="copyToClipboardAndNotify(this.innerText)"),
#         A(href="/hello")("Go to Hello page"),
#         Div(
#             P("Hello", onclick="copyToClipboardAndNotify(this.innerText)"),
#             hx_get="/change",
#         ),
#         Div(P("Hello")),
#     )


# @rt("/change")
# def get():
#     return P("Nice to be here!")


@rt("/")
def get():
    def prompt_card(promot: str):
        return Div(
            promot,
            onclick="copyToClipboardAndNotify(this.innerText)",
            cls="cell",
        )

    content = [
        prompt_card(
            "List the top 10 most popular repos on GitHub and summarize what they have in common."
        ),
        prompt_card(
            "Summarize the changes in the github/github-mcp-server repo since the v0.1.0 release"
        ),
        prompt_card(
            "Rate the open pull requests on the github/github-mcp-server repo based on how cool you think they are."
        ),
    ]
    return Titled(
        "Prompt Gallery",
        P("Hover over a prompt and click to copy it to your clipboard"),
        copy_script,
        Grid(
            *content,
            cls="grid",
        ),
        Style(
            """
            .grid {
                display: grid;
                # grid-template-columns: 1fr 1fr; /* Two columns */
                # grid-template-rows: auto auto; /* Two rows */
                grid-template-columns: 1fr; /* Single column */
                grid-template-rows: auto; /* Two rows */
                gap: 10px; /* Space between cells */
            }
            .cell {
                padding: 20px;
            #     background-color: #f0f0f0;
            #     border: 1px solid #ccc;
                text-align: center;
            }
            .cell:hover {
            #   background-color: #474646; /* Change background on hover */
                font-weight: bold; /* Change font to bold on hover */
            }
        """
        ),
    )


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


serve(
    #host="127.0.0.1"
)  # Need this bc js copy script wont run on not secure default 0.0.0.0 host
