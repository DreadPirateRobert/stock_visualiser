from routes import *
import pymongo
from pymongo import MongoClient
import requests
import json
import MySQLdb


class stock(tornado.web.RequestHandler):
    def set_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        
    def mongo_write(self,req):
        connection = MongoClient("ds149954.mlab.com", 49954)
        db = connection['visualizer']
        db.authenticate('temp', 'temp123')
        #db.mynewcollection.insert({ "temp123" : "new_temp_inserter" })
        db.mynewcollection.insert({ req['Meta Data']['2. Symbol'] : json.dumps(req) })
        print "successfully written to MLab:"
        
        #Retreving data from MLab
        data = db.mynewcollection.find()
        for keys in data:
            print keys['_id']
    
    def sql_write(self,req):
        db = MySQLdb.connect("localhost","root","root","stock" )
        cursor = db.cursor()
        sql = "INSERT INTO `stock`.`stock_names` (`stock_name`, `user`) VALUES ('%s', '%s')" % (req['2. Symbol'],'temp')
        cursor.execute(sql)
        db.commit()
        db.close()
        print "Successfully written to sql: ",req['2. Symbol']
        
        
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
        
        #write to Mlab
        self.mongo_write(req)
        
        #write to sql
        self.sql_write(req['Meta Data'])
        
        self.write(stock_mess)
        #self.render("chart.html")
            
class index(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")