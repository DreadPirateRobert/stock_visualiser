from routes import *
import requests
import json

class stock(tornado.web.RequestHandler):
    def set_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
    
    def post(self):
        self.set_headers()
        stock_name = self.get_argument("stock_name")
        print "stock api called: " + str(stock_name)
        req = requests.Session()
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + str(stock_name) +'&interval=1min&apikey=PTJUBNEO2HLMPSQD'
        req = requests.get(url)
        req = json.loads(req.text)
        
        high_req = []
        for data in req["Time Series (1min)"]:
            tmp_req = []
            time = (int(data[:4])-1970)*365*24*60*60 + (int(data[5:7]))*30*24*60*60 + (int(data[8:10]))*24*60*60 + (int(data[11:13]))*60*60 + (int(data[14:16]))*60 + int(data[17:19])
            tmp_req.append(time)
            tmp_req.append(float(req["Time Series (1min)"][data]["1. open"]))
            tmp_req.append(float(req["Time Series (1min)"][data]["2. high"]))
            tmp_req.append(float(req["Time Series (1min)"][data]["3. low"]))
            tmp_req.append(float(req["Time Series (1min)"][data]["4. close"]))
            tmp_req.append(float(req["Time Series (1min)"][data]["5. volume"]))
            high_req.append(tmp_req)
#            for key,value in req["Time Series (1min)"][data]
        stock_mess = {'info': req["Meta Data"],'data':high_req}
        print stock_mess
        self.write(stock_mess)
        #self.render("chart.html")
            
class index(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")