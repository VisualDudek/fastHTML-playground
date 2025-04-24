# ruff: noqa
# type: ignore
# fmt: off

from fasthtml.common import *
from fasthtml import common as fh

# app, rt = fh.fast_app()

def render(todo):
    tid = f'todo-{todo.id}'
    toggle = A('Toggle', hx_get=f"/toggle/{todo.id}", target_id=tid)
    return Li(todo.title + ' ' + str(todo.id) + (' DONE ' if todo.done else ''), toggle, id=tid)

app, rt, todos, Todo = fast_app(
    db_file='todos.db', 
    live=True, 
    title=str, 
    done=bool,
    id=int,
    pk='id',
    render=render,
    )


@rt("/")
def get():
    nums = Ul(*[Li(num) for num in range(5)])
    # return Div(P("Hello World!"))
    # Idiomatic, chce strone z tytułem -> Titled()
    # todos.insert(Todo(title='First todo', done=False))
    # items = [Li(o) for o in todos()]
    return Titled("I am title", 
                Div(P("Hello World!")), 
                Div(nums, id='nums', hx_get="/change"), 
                # P(A("Link")),
                Div(Ul(*todos())),
                )
    # sprawdzaj kod źródłowy, jest tam dużo podpowiedzi

@rt("/change")
def get():
    return Div(P('Change is good'))


@rt("/toggle/{tid}")
def get(tid:int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo



serve()
