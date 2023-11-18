#imports the requests used to make HTtP calls
import requests

#Imports the Session library that will allow us to create a session object for the purpose of sharing
from requests import Session

#Imports a json library called pretty print to print json more visually appealing "pretty"
from pprint import pprint as pretp

class CryptoClassAPI:

    #Class initialization function
    def __init__(self):

        #Sets the base URL of the api we are going to connect to
        self.apiurl = 'https://pro-api.coinmarketcap.com'

        #Defines a data structure to store the type of data we will accept as well as a variable to hold our key
        self.headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': '1517333c-4bfc-4553-8b98-7299e8b438e3',}

        #Creates a session object instance that we will use for our data exchange session with the API
        self.session = Session()

        #Defines the shared connection information we are going to retain accross the session
        self.session.headers.update(self.headers)

    def get_price(self,symbol):
        url = self.apiurl + '/v2/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url,params=parameters)
        data = r.json()['data']
        return data
    
    def get_all_listings(self,start,end):
        url = self.apiurl + '/v1/cryptocurrency/listings/latest'
    
if __name__ == "__main__":
    cryptoinstance = CryptoClassAPI()
    #print(cryptoinstance.get_price('BTC'))
    pretp(cryptoinstance.get_price("BTC"))

    pretp(cryptoinstance.get_all_listings("1","1000"))