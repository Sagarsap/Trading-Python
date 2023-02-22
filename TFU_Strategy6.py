#https://buildmedia.readthedocs.org/media/pdf/technical-analysis-library-in-python/latest/technical-analysis-library-in-python.pdf

from kiteconnect import KiteConnect

from datetime import datetime,timedelta
import pandas as pd
from pytz import timezone
import ta
import pandas as pd
import pandas_ta as pta
import requests


def rsi(close, window, fillna=False):
    rsi_indicator = ta.momentum.RSIIndicator(close, window, fillna)
    return rsi_indicator.rsi()

def ohlc(checkInstrument,timeframe):
    date=pd.to_datetime(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))
    while(str(date)[-2::]!='00'):
        date=pd.to_datetime(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))
    date=date+timedelta(minutes=timeframe)
    current=date
    date=date-timedelta(seconds=2)
    l=[]
    while(pd.to_datetime(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))<=date):
        x=getLTP(checkInstrument)
        if x!=-1:
            l.append(x)
    if l!=[]:
        opens=l[0]
        high=max(l)
        low=min(l)
        close=l[-1]
        return [current,opens,high,low,close]
    else:
        return [-1]


def getLTP(name):
    try:
        ltp = kc.ltp([name])[name]['last_price']
        return ltp

    except Exception as e:
        print(name , "Failed : {} ".format(e))


####################__INPUT__#####################

api_key = ""
access_token = ""
kc = KiteConnect(api_key=api_key)
kc.set_access_token(access_token)

checkInstrument = "NFO:NIFTY22DECFUT";

x = 1
close=[]
opens=[]
high=[]
low=[]
op=['rsi',7,3]
print(['datetime','open','high','low','close'])
st=0

while x == 1:
    data=ohlc(checkInstrument,1)
    print(data)
    if data[0]!=-1:
        opens.append(data[1])
        high.append(data[2])
        low.append(data[3])
        close.append(data[-1])
        if op!=[]:
            value=ta.momentum.RSIIndicator(pd.Series(close),op[1],False).rsi()
            value1=ta.momentum.RSIIndicator(pd.Series(close),op[2],False).rsi()

        if str(value)[0].isdigit()==True and str(value1)[0].isdigit()==True:
            data.extend([value,value1])
            if st==0 and value>40 and value1<20:
                print('rsi_14 > 40 and rsi_2 < 20')
                sl=(float(close[-1])*0.4)/100
                sl=float(close[-1])-sl
                st=1
                typ='BUY'

            elif st==0 and value<60 and value1>80:
                print('rsi_14 < 60 and rsi_2 > 80')
                sl=(float(close[-1])*0.4)/100
                sl=float(close[-1]) + sl
                st=1
                typ='SELL'
            elif st==1 and typ=='SELL':
                if high[-1]>=sl:
                    print('SL Hit')
                    st=0
                elif value>60 or value1<20:
                    print('rsi_14 > 60 and rsi_2 < 20')
                    st=0
            elif st==1 and typ=='BUY':
                if low[-1]<=sl:
                    print('SL Hit')
                    st=0
                elif value<40 or value1>80:
                    print('rsi_14 < 40 and rsi_2 > 80')
                    st=0
            elif pd.to_datetime(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')) > pd.to_datetime(str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'))+' 15:15:00'):
                print('End Of the Day')
                st=0
                break
            print(data)
