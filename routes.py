import tornado.ioloop
import tornado.web

from chart_api import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Stock Visualisation, ")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/chart", chart),
    ])

if __name__ == "__main__":
    app = make_app()
    print ('Listening on port: 8888')
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()