"Class methods for Walmart Stores API"
from wapy.api import Wapy
from beholder.keys.keys import walmart


class walmartAPI:
    def __init__(self):
        self.walmart = walmart()
        self.apiKey = self.walmart.key["walmartAPIKey"]
        self.wapy = Wapy(self.apiKey)
        self.categories = []

    def getBestSellers(self, request, walmartModel):
        walmartItems = self.wapy.bestseller_products(request.GET.get("walmartCatId"))
        for i, item in enumerate(walmartItems):

            if walmartModel.objects.filter(ASIN=item['ASIN']).exists():
                amazonItems['Item'][i] = amazonModel.objects.get(ASIN=item['ASIN'])
            else:
                amazonItems['Item'][i]['data'] = item
        return products

    def getClearance(self, request, walmartModel):
        return self.wapy.clearance_products(request.GET.get("walmartCatId"))

    def getSpecialBuy(self, request, walmartModel):
        return self.wapy.clearance_products(request.GET.get("walmartCatId"))

    def getTrending(self, walmartModel):
        return self.wapy.trending_products()

    def search(self, request, walmartModel):
        products = wapy.search(
            request.GET.get("keywords"),
            numItems=25,
            categoryId=request.GET.get("walmartCatId"),
            page=request.GET.get("page"),
            sort=request.GET.get("walmartSearchSort")
            )
        return products

w = walmartAPI()

p = w.getTrending()
p[0].name
p[0].images
p[0].upc
p[0].item_id


product = wapy.product_lookup('21853453')
