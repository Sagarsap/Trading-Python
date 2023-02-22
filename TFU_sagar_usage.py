
# importing the requests library
import requests
import time

def getLTP(Instrument):
    url = "http://localhost:4000/ltp?instrument=" + Instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data

def main():
    while True:
        k = getLTP('NSE:SBIN')
        print(" K = "  ,k)
        time.sleep(1)
        k = getLTP('NSE:RELIANCE')
        print(" K = "  ,k)

main()