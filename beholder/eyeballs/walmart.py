"Class methods for Walmart Stores API"
from wapy.api import Wapy
from beholder.keys.keys import walmart


class walmartAPI:
    def __init__(self):
        self.walmart = walmart()
        self.apiKey = self.walmart.key["walmartAPIKey"]
        self.wapy = Wapy(self.apiKey)
        self.categories = [
            {'name':'All','code':''}, {'name':'Arts, Crafts & Sewing','code':'1334134'},
            {'name':'Auto & Tires','code':'91083'}, {'name':'Baby','code':'5427'},
            {'name':'Beauty','code':'1085666'}, {'name':'Books','code':'3920'},
            {'name':'Cell Phones','code':'1105910'}, {'name':'Clothing','code':'5438'},
            {'name':'Electronics','code':'3944'}, {'name':'Food','code':'976759'},
            {'name':'Gifts & Registry','code':'1094765'}, {'name':'Health','code':'976760'},
            {'name':'Home','code':'4044'}, {'name':'Home Improvement','code':'1072864'},
            {'name':'Household Essentials','code':'1115193'}, {'name':'Industrial & Scientific','code':'6197502'},
            {'name':'Jewelry','code':'3891'}, {'name':'Movies & TV Shows','code':'4096'},
            {'name':'Music on CD or Vinyl','code':'4104'}, {'name':'Musical Instruments','code':'7796869'},
            {'name':'Office','code':'1229749'}, {'name':'Party & Occasions','code':'2637'},
            {'name':'Patio & Garden','code':'5428'}, {'name':'Personal Care','code':'1005862'},
            {'name':'Pets','code':'5440'}, {'name':'Photo Center','code':'5426'},
            {'name':'Premium Beauty','code':'792499'}, {'name':'Seasonal','code':'1085632'},
            {'name':'Sports & Outdoors','code':'4125'}, {'name':'Toys','code':'4171'},
            {'name':'Video Games','code':'2636'}, {'name':'Walmart for Business','code':'6735581'},
            ]

    def getBestSellers(self, request):
        return self.wapy.bestseller_products(int(request.GET.get("walmartCatId")))

    def getClearance(self, request):
        return self.wapy.clearance_products(int(request.GET.get("walmartCatId")))

    def getSpecialBuy(self, request):
        return self.wapy.clearance_products(int(request.GET.get("walmartCatId")))

    def getTrending(self):
        return self.wapy.trending_products()

    def search(self, request):
        products = self.wapy.search(
            request.GET.get("keywords"),
            numItems=25,
            categoryId=int(request.GET.get("walmartCatId")),
            page=1,
            #sort=request.GET.get("walmartSearchSort"),
            )
        return products


w = walmart()
wapy = Wapy(w.key["walmartAPIKey"])
product = wapy.product_lookup('21853453')
bestsellers = wapy.bestseller_products(3944)
bestsellers[0].name
bestsellers[0].sale_price
product.available_online
product.name
product.upc
product.sale_price
product.msrp
product.stock
product.item_id
product.short_description
'''
