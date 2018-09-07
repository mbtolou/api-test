import hug

@hug.get('/')
def hello():
    return 'hello world'

app = __hug_wsgi__
