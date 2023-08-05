from requests import api
import socketio
import json
import requests
import time
from datetime import datetime
from hashlib import sha256

class SocketEventIsec(socketio.ClientNamespace):
    def __init__(self, namespace, isec_instance):
        super().__init__(namespace)
        self.isec = isec_instance
        self.hostname = 'https://uatstreams.icicidirect.com'
        self.sio = socketio.Client()

    def connect(self):
        auth = {"user": self.isec.user_id, "token": self.isec.session_key}
        self.sio.connect(self.hostname, auth=auth)

    def on_disconnect(self):
        pass
    
    def on_message(self, data):
        data = self.isec.parse_data(data)
        self.isec.on_ticks(data)
    
    def watch(self, data):
        print("watching stock")
        print(data)
        self.sio.emit('join', data)
        self.sio.on('stock',self.on_message)
    
    def unwatch(self, data):
        print("unsubscribed:"+str(data))
        self.sio.emit("leave", data)
        
class IsecConnect():

    def __init__(self, api_key): #needed for hashing json data
        self.user_id = None
        self.api_key = api_key
        self.session_key = None
        self.secret_key = None    
        self.sio_handler = None
        self.on_ticks = None
                 
    def ws_connect(self):
        if not self.sio_handler:
            self.sio_handler = SocketEventIsec("/", self)
            self.sio_handler.connect()
                 
    def subscribe_stock(self, stock_names):
        if self.sio_handler:
            self.sio_handler.watch(stock_names)
    
    def unsubscribe_stock(self, stock_names):
        if self.sio_handler:
            self.sio_handler.unwatch(stock_names)
        # raise SioHandlerNot
    
    def parse_market_depth(self, data, exchange):
        depth=[]
        for lis in data:
            dict = {}
            if exchange=='1':
                dict["BestBuyRate-1"] = lis[0]
                dict["BestBuyQty-1"] = lis[1]
                dict["BestSellRate-1"] = lis[2]
                dict["BestSellQty-1"] = lis[3]
                depth.append(dict)
            else:
                dict["BestBuyRate-1"] = lis[0]
                dict["BestBuyQty-1"] = lis[1]
                dict["BuyNoOfOrders-1"] = lis[2]
                dict["BuyFlag-1"] = lis[3]
                dict["BestSellRate-1"] = lis[4]
                dict["BestSellQty-1"] = lis[5]
                dict["SellNoOfOrders-1"] = lis[6]
                dict["SellFlag-1"] = lis[7]
                depth.append(dict)
        return depth

    def parse_data(self, data):
        exchange = str.split(data[0],'!')[0].split('.')[0]
        data_type = str.split(data[0],'!')[0].split('.')[1]
        if data_type == '1':
            data_dict = {
                "symbol": data[0],
                "open": data[1],
                "last": data[2],
                "high": data[3],
                "low": data[4],
                "change": data[5],
                "bPrice": data[6],
                "bQty": data[7],
                "sPrice": data[8],
                "sQty": data[9],
                "ltq": data[10],
                "avgPrice": data[11],
                "ttq": data[12],
                "totalBuyQt": data[13],
                "totalSellQ": data[14],
                "ttv": data[15],
                "trend": data[16],
                "lowerCktLm": data[17],
                "upperCktLm": data[18],
                "ltt": datetime.fromtimestamp(data[19]).strftime('%c'),
                "quotes": "Quotes Data"
            }
        else:
            data_dict = {
                "symbol": data[0],
                "time": datetime.fromtimestamp(data[1]).strftime('%c'),
                "depth" : self.parse_market_depth(data[2],exchange),
                "quotes": "Market Depth"
            }
        if exchange =='4':
            data_dict['exchange'] = 'NSE Equity'
        elif exchange == '1':
            data_dict['exchange'] = 'BSE'
        elif exchange == '13':
            data_dict['exchange'] = 'NSE Currency'
        return data_dict

    def api_util(self, json_data,url,api_name):
        current_date = datetime.now()
        current_timestamp = current_date.strftime("%d-%b-%Y %H:%M:%S")
        
        hashedWord = sha256((current_timestamp+json.dumps(json_data)+self.secret_key).encode("utf-8")).hexdigest()
        req_body = {
            "AppKey": self.api_key,
            "time_stamp" : current_timestamp,
            "JSONPostData" : json.dumps(json_data),
            "Checksum" : hashedWord
        }
        result = requests.post(url = url, data = json.dumps(req_body) , headers={"Content-Type": "application/json"})
        try:
            self.session_key = result.json()['Success']['session_token']
            self.user_id = result.json()['Success']['idirect_userid']
        except:
            print("Could not authenticate credentials. Please check token and keys")
    
    def generate_session(self, api_secret, session_token):
        self.session_key = session_token
        self.secret_key = api_secret
        url = "http://103.87.40.246/customer/customerdetails"
        json_data = {
                # "UserID" : self.user_id,
                "API_Session" : self.session_key,
                "AppKey": self.api_key
        }
        self.api_util(json_data,url,'cust_details')
    