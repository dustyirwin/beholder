from wapy.api import Wapy
from beholder.keys.keys import keys
import requests


"""
Class methods for Walmart Stores API
"""

class walmartEye:
    def __init__(self):
        self.keys = keys()
        self.walmartAPIKey = self.keys.walmart["walmartAPIKey"]
        self.wapy = Wapy(self.walmartAPIKey)
        self.taximony = requests.get('http://api.walmartlabs.com/v1/taxonomy?apiKey='+self.walmartAPIKey).json()
        self.categories = []

        for category in self.taximony['categories']:
            self.categories.append({
            'id': category['id'],
            'name': category['name'],
            })

    def getBestSellers(self, **kwargs):
        if bool(kwargs['walmartCatId']) == True:
            return self.wapy.bestseller_products(int(kwargs['walmartCatId']))
        else:
            return []

    def getClearance(self, **kwargs):
        if bool(kwargs['walmartCatId']) == True:
            return self.wapy.clearance_products(int(kwargs["walmartCatId"]))
        else:
            return []

    def getSpecialBuy(self, **kwargs):
        if bool(kwargs['walmartCatId']) == True:
            return self.wapy.clearance_products(int(kwargs["walmartCatId"]))
        else:
            return []

    def getTrending(self, **kwargs):
        return self.wapy.trending_products()

    def search(self, **kwargs):
        products = self.wapy.search(
            kwargs["keywords"],
            categoryId=int(kwargs["walmartCatId"]),
            ResponseGroup="full",
            page=int(kwargs["walmartPage"]),
            sort="bestseller",
            numItems=25,
        )
        return products


"""
Scratchpad


walmart = walmartEye()

products = walmart.search(keywords="batman",walmartCatId="5438",walmartPage="1")
products[0].sale_price
products[0].item_id
products[0].product_url
products[0].long_description
products[0].stock
products[0].available_online
ship = products[0].get_attribute("stock")

print(ship)

best_sellers_in_5438 = walmart.getBestSellers(walmartCatId=5438,page=1)
clearance_in_5438 = walmart.getClearance(walmartCatId="5438",page="1")
special_buy_in_5438 = walmart.getSpecialBuy(walmartCatId="5438",page="1")
trending = walmart.getTrending()
trending[0].name
"""
