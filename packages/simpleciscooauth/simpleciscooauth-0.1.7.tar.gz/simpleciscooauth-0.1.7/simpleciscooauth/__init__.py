# -*- coding: utf-8 -*-

__author__ = "Jason Smith"
__credits__ = ["Jason Smith"]
__email__ = "jasons2@cisco.com"

"""
.env file must exist and be accessible.
Format:
clientId = 'yourclientID'
clientSecret = 'yourclientsecret'

Credentials can be obtained at http://apiconsole.cisco.com 
"""

import json
from datetime import datetime
from os import path
from decouple import config
import requests
from vslogging import vslogging

class SimpleCiscoOAuth:

    def __init__(self, tokenStorage=".token"):
        self.tokenStorage = tokenStorage
        self.token = ""
        self.clientId = config('clientId', default='')
        self.clientSecret = config('clientSecret', default='')
        self.rightnow = datetime.now()
        self.tokenInfo = {"tokenObtained" : self.rightnow, "token": self.token}
        self.tokenAge = 0
        self.l = vslogging('simpleciscooauth')

    def obtain_token(self):
        # this function checks to see if a token has been received in the last 60 mins
        # If it has, it loads it.  If not it runs post API request to odtain token and 
        # returns it to be used in other functions

        if not self.fileExists():
            self.l.debug(f".token file does not exist")
            self.generateToken()
            self.storeToken()
        else:
            self.l.debug(f".token file exists")
            self.readToken()
            self.calculateTokenAge()
            self.l.debug(f"Token age is {self.tokenAge}")

            if self.tokenAge  > 3600:
                self.generateToken()
                self.storeToken()
            else:
                self.l.debug("Assigning token from stored data")
                self.token = self.tokenInfo['token']

        return self.token
    
    def generateToken(self):
        """
        contact API, get token and store it in token
        """
        payload={}
        headers = {}

        self.l.debug(f"Generating new token")
        url = f"https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id={self.clientId}&client_secret={self.clientSecret}"
        
        response = requests.request("POST", url, headers=headers, data=payload)
        self.l.debug(f"requests status {response.status_code}")
        token_dict = json.loads(response.text)
        self.l.debug(f"token_dict -> {token_dict}")
        self.token = (token_dict['access_token'])
        self.l.debug(f"Successfully generated token")
        self.l.debug(f"token -> {self.token}")
    
    def storeToken(self):
        """
        Store the contents of tokenInfo in the file tokenStorage
        """
        self.l.debug(f"Storing token")
        self.tokenInfo = {"tokenObtained" : self.rightnow.strftime("%d-%m-%y:%H:%M:%S"), "token": self.token}
        self.l.debug(f"Writing {self.tokenInfo} to disk")
        with open(self.tokenStorage, "w") as outfile:
            json.dump(self.tokenInfo, outfile)
        self.l.debug(f"Successfully wrote to disk")

    def readToken(self):
        """
        Read contents of tokenStorage and put it in tokenInfo
        """
        self.l.debug(f"Reading token from Disk")
        with open (self.tokenStorage, "r") as f:
            self.tokenInfo = json.load(f)
        self.l.debug(f"Read {self.tokenInfo} from file.")

    def calculateTokenAge(self):
        """
        Calculate age of current token and store in tokenAge
        """
        self.l.debug(f"Calculating token age.")
        tokenLastReceived = datetime.strptime(self.tokenInfo['tokenObtained'], "%d-%m-%y:%H:%M:%S")
        self.l.debug(f"Token last received : {tokenLastReceived}")
        self.tokenAge = abs((self.rightnow - tokenLastReceived).total_seconds())
        self.l.debug(f"Token age computed as {self.tokenAge}")


    def fileExists(self) -> bool:
        return path.isfile(self.tokenStorage)