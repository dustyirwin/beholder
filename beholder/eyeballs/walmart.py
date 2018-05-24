"Class methods for Walmart Stores API"

from beholder.keys.keys import walmart

class walmartAPI:
    def __init__(self):
        self.walmart = walmart()
        self.apiKey = self.walmart.key['apiKey']

    def getItemInfo(self, request):
        UPC_URL = 'http://api.walmartlabs.com/v1/items?apiKey='+self.apiKey+'a' + request.GET.get('UPC')
        resp = request.GET.get('GET', UPC_URL)
        print(str(resp))
        return resp

    def search(self, request):
        query_URL = ''
        return query_URL

    def price(self, request, WalmartDB):
        print("Do cool stuff yo!")
