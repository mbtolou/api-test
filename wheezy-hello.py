from wheezy.http import HTTPResponse, WSGIApplication
from wheezy.routing import url
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bottstrap_defaults, path_routing_middleware_factory

class WelcomeHandler(BaseHandler):
    def get(self):
        response = HTTPResponse()
        response.write('hello world')
        return response

urls = [
        url('', WelcomeHandler, name='default')
]

options = {}
app = WSGIApplication(
        middleware=[
            bootstrap_defaults(url_mapping=urls),
            path_routing_middleware_factory
        ],
        options=options
)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=8000)
