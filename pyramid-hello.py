from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response

def hello(request):
    return Response('hello world')

with Configurator() as config:
    config.add_route('hello', '/')
    config.add_view(hello, route_name='hello')
    app = config.make_wsgi_app()
    #print(app)
    #serve(app, host='127.0.0.1', port=8000)
