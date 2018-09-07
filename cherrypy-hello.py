import cherrypy

class Root(object):
    @cherrypy.expose
    def index(self):
        return "hello world"

cherrypy.config.update({
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 8000,
    'engine.autoreload.on': False,
    'environment': 'embedded'
})

app = cherrypy.tree.mount(Root())
cherrypy.server.unsubscribe()
cherrypy.engine.signals.subscribe()
cherrypy.engine.start()

#app = cherrypy.quickstart(HelloWorld())
