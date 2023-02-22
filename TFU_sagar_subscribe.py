from urllib import response
from kiteconnect import KiteTicker
from kiteconnect import KiteConnect
from pprint import pprint
import threading
from flask import Flask, request

##############################################
#                   INPUT's                  #
##############################################
apiKey = "i0ail80lvw85fpsn"
accessToken = "Zlp1hxT0aYX2mlsalwxtZsuDJxtdxn3f"

instrumentList = [
    "NSE:ABFRL",
    "NSE:ADANIENT",
    "NSE:ADANIPORTS",
    "NSE:AMARAJABAT",
    "NSE:ABB",
    #"NFO:NIFTY22DEC18000CE",
    "NSE:NIFTY 50"

]

##############################################
print("!! Started getltpDict.py !!")

app = Flask(__name__)

kc = KiteConnect(api_key=apiKey)
kc.set_access_token(accessToken)

tokenMapping = { }
ltpDict = { }

@app.route('/')
def hello_world():
	return 'Hello World'

@app.route('/ltp')
def getLtp():
    global ltpDict
    print(ltpDict)
    ltp = -1
    instrumet = request.args.get('instrument')
    try:
        ltp = ltpDict[instrumet]
    except Exception as e :
        print("EXCEPTION occured while getting ltpDict()")
        print(e)
    return str(ltp)



def getTokensList(instrumentList):
    global tokenMapping
    response = kc.ltp(instrumentList)
    tokensList = []
    for inst in instrumentList:
        token = response[inst]['instrument_token']
        tokensList.append(token)
        tokenMapping[token] = inst
    return tokensList

def on_ticks(ws, ticks):
    global ltpDict
    for tick in ticks:
        inst = tokenMapping[tick['instrument_token']]
        ltpDict[inst] = tick['last_price']
    print(ltpDict)

def on_connect(ws, response):
    global instrumentList
    tokensList = getTokensList(instrumentList)
    ws.subscribe(tokensList)
    ws.set_mode(ws.MODE_LTP,  tokensList)

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4000)

def main():
    print("Inside main()")
    t1 = threading.Thread(target=startServer)
    t1.start()
    
    kws = KiteTicker(apiKey , accessToken)
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.connect()
    t1.join()
    print("websocket started !!")

main()