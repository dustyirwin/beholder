"Class methods for Target Stores API"

from beholder.keys.keys import target

class targetAPI:
    def __init__(self):
        self.target = target()
        self.apiKey = self.target.key['targetAPIKey']
        self.categories = ['All']

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
