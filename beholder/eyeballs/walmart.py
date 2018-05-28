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
            page=int(kwargs['page']),
            sort="bestseller",
            numItems=25,
            start=25 * int(kwargs['page']) - 24,
        )
        return products


"""
Scratchpad


walmart = walmartEye()

batman_products_in_5438 = walmart.search(keywords="batman",walmartCatId="5438",page="1")
best_sellers_in_5438 = walmart.getBestSellers(walmartCatId=5438,page=1)
clearance_in_5438 = walmart.getClearance(walmartCatId="5438",page="1")
special_buy_in_5438 = walmart.getSpecialBuy(walmartCatId="5438",page="1")
trending = walmart.getTrending()
trending[0].name
"""
