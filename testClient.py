from starlette.testclient import TestClient
from fasthtml.common import *


css = Style(":root {--pico-font-size:90%,--pico-font-family: Pacifico, cursive;}")
hdrs = (picolink, css)

# app, rt = fast_app(live=True, hdrs=hdrs)

app = FastHTML(hdrs=hdrs)
rt = app.route


@rt("/")
def get():
    return (Title("Hello world"), Main(H1("hello w"), P("testing"), cls="container"))


# client = TestClient(app)
# print(client.get("/").text)
# print(client.post("/").text)

serve()
