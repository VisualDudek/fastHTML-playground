from fasthtml.common import *

app, rt = fast_app(debug=True)


@rt("/")
def get():
    return Titled("FastHTML", P("Let's do this!"))


serve()
