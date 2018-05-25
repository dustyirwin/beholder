"Class methods for Walmart Stores API"
from wapy.api import Wapy
from beholder.keys.keys import walmart


class walmartAPI:
    def __init__(self):
        self.walmart = walmart()
        self.apiKey = self.walmart.key["walmartAPIKey"]
        self.wapy = Wapy(self.apiKey)
        self.categories = {'name':'Apparel','code':'5438'}

    def getBestSellers(self, request, walmartModel):
        walmartItems = self.wapy.bestseller_products(int(request.GET.get("walmartCatId")))
        for i, item in enumerate(walmartItems):

            if walmartModel.objects.filter(itemId=item.item_id).exists():
                walmartItems[i] = walmartModel.objects.get(itemId=item['itemId'])

        return walmartItems

    def getClearance(self, request, walmartModel):
        return self.wapy.clearance_products(int(request.GET.get("walmartCatId")))

    def getSpecialBuy(self, request, walmartModel):
        return self.wapy.clearance_products(int(request.GET.get("walmartCatId")))

    def getTrending(self, walmartModel):

        return self.wapy.trending_products()

    def search(self, request, walmartModel):
        products = wapy.search(
            request.GET.get("keywords"),
            numItems=25,
            categoryId=int(request.GET.get("walmartCatId")),
            page=request.GET.get("page"),
            sort=request.GET.get("walmartSearchSort")
            )
        return products

w = walmart()

wapy = Wapy(w.key["walmartAPIKey"])
product = wapy.product_lookup('21853453')
product.available_online
product.name
product.upc
product.sale_price
product.msrp
product.stock
product.item_id
product.short_description
