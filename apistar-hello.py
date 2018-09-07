from apistar import App, Route

def hello():
    return 'hello world'

app = App(routes=[
    Route('/', method='GET', handler=hello)
])
