# -----------------------------------------------------------------------------------#
# 1. Manual Login
# 2. Automatic Login using Selenium
# -----------------------------------------------------------------------------------#

# Import the required Libraries
from kiteconnect import KiteConnect
from pprint import pprint
import logging
from kiteconnect import KiteTicker
import pandas

#  Set your Account Details Here
api_key = "i0ail80lvw85fpsn"
secret_key = "6pz0z6jqas7dci9fm5bmf26wdgei27wr"
access_token = "Zlp1hxT0aYX2mlsalwxtZsuDJxtdxn3f" #NEED TO GENERATE EVERYDAY BY RUNNING THE FILE AND GOING TO LINK TO GET TEMP REQUEST TO MAKE IT FINAL ACCESS TOKEN#

#microsoft visual C++ installed.
#pip install KiteConnect
#pip install Twisted

#api_key = autoLoginClass.api_key()
#secret_key = autoLoginClass.secret_key()

kite = KiteConnect(api_key=api_key)

def manualLogin():
    global access_token, kite

    print(" Visit URL , Enter Details and get RequestToken :")
    login_url = "https://kite.trade/connect/login?api_key=" + api_key
    print(login_url)

    code = input("Enter RedirectURI token ")

    data = kite.generate_session(code, api_secret=secret_key)
    kite.set_access_token(data["access_token"])

    accessToken = data["access_token"]
    print("Access Token = ", accessToken)
    access_token = accessToken
    kite.set_access_token(access_token)


manualLogin()
