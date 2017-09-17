from routes import *

class chart(tornado.web.RequestHandler):
        def get(self):
            self.render("chart.html")