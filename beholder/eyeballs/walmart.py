from wapy.api import Wapy
from beholder.keys.keys import walmart as walmartKeys

"Class methods for Walmart Stores API"

class walmartAPI:
    def __init__(self):
        self.walmartKeys = walmartKeys()
        self.apiKey = self.walmartKeys.key["walmartAPIKey"]
        self.wapy = Wapy(self.apiKey)
        self.categories = [
            {'name':'All','code':''}, {'name':'Arts, Crafts & Sewing','code':'1334134'},
            {'name':'Auto & Tires','code':'91083'}, {'name':'Baby','code':'5427'},
            {'name':'Beauty','code':'1085666'}, {'name':'Books','code':'3920'},
            {'name':'Cell Phones','code':'1105910'}, {'name':'Clothing','code':'5438'},
            {'name':'TVs','code':'3944_1060825'}, {'name':'Food','code':'976759'},
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

    def getBestSellers(self, **kwargs):
        return self.wapy.bestseller_products(int(kwargs["walmartCatId"]))

    def getClearance(self, **kwargs):
        return self.wapy.clearance_products(int(kwargs["walmartCatId"]))

    def getSpecialBuy(self, **kwargs):
        return self.wapy.clearance_products(int(kwargs["walmartCatId"]))

    def getTrending(self, **kwargs):
        return self.wapy.trending_products()

    def search(self, **kwargs):
        products = self.wapy.search(
            kwargs["keywords"],
            categoryId=int(kwargs["walmartCatId"]),
            page=int(kwargs['page']),
            #sort=kwargs['sort']),
            #numItems=25,
        )
        return products

"""
Scratchpad
"""

walmart = walmartAPI()
batman_products_in_5438 = walmart.search(keywords="batman",walmartCatId="5438",page="1")
best_sellers_in_5438 = walmart.getBestSellers(walmartCatId="5438",page="1")
clearance_in_5438 = walmart.getClearance(walmartCatId="5438",page="1")
special_buy_in_5438 = walmart.getSpecialBuy(walmartCatId="5438",page="1")
trending = walmart.getTrending()

trending[0].name
