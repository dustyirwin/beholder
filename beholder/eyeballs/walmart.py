from requests import request

class walmartAPI:
    def __init__(self):
        self.apiKey = 'njpxezmectwhkmwyve6d2fnm'

    def getItemInfo(self, request):
        UPC_URL = 'http://api.walmartlabs.com/v1/items?apiKey='+self.apiKey+'a'+request.GET.get('UPC')
        resp = request.GET.get('GET', UPC_URL)
        print(str(resp))
        return resp

    def searchWalmart(self, request):
        query_URL = ''
        return {}