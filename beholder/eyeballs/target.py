from beholder.keys import keys
import requests

"Class methods for Target Stores API"


class targetEye:
    def __init__(self):
        self.keys = keys()
        self.APIKey = self.keys.target['APIKey']
        self.target = "target api class..."
        self.categories = ['All']

    def getItemInfo(self, **kwargs):
        UPC_URL = 'http://api.target.com/upc...' + kwargs['UPC']
        resp = requests.get(UPC_URL)
        targetItem = resp
        return targetItem

    def search(self, **kwargs):
        searchURL = 'http://api.target.com/upc...'
        resp = requests.get(searchURL)
        targetItems = resp
        return targetItems

    def price(self, **kwargs):
        print("Do cool stuff yo!")


"""
Scratchpad / Testing
"""
