import bottle

@bottle.get('/')
def hello():
    return 'hello world'

app = bottle.default_app()
