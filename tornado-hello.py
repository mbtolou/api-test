import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')

app = tornado.web.Application([(r"/", MainHandler)])
