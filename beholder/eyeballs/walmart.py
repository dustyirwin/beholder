from wapy.api import Wapy
from beholder.keys.keys import keys
import requests
import traceback


"""
Class methods for Walmart Stores API
"""

class walmartEye:
    def __init__(self):
        self.categories = []
        self.keys = keys()
        self.walmartAPIKey = self.keys.walmart["walmartAPIKey"]
        self.wapy = Wapy(self.walmartAPIKey)
        try:
            self.taximony = requests.get('http://api.walmartlabs.com/v1/taxonomy?apiKey='+self.walmartAPIKey).json()
            for category in self.taximony['categories']:
                self.categories.append({
                'id': category['id'],
                'name': category['name'],
                })
        except:
            print(traceback.format_exc()) #  output error to std



    def getBestSellers(self, **kwargs):
        return self.wapy.bestseller_products(int(kwargs['category']))

    def getClearance(self, **kwargs):
        return self.wapy.clearance_products(int(kwargs["category"]))

    def getSpecialBuy(self, **kwargs):
        return self.wapy.clearance_products(int(kwargs["category"]))

    def getTrending(self, **kwargs):
        return self.wapy.trending_products()

    def search(self, **kwargs):
        products = self.wapy.search(
            kwargs["keywords"],
            categoryId=int(kwargs["category"]),
            ResponseGroup="full",
            page=int(kwargs["page"]),
            sort="bestseller",
            numItems=25,
        )
        return products


"""
Scratchpad/Testing


walmart = walmartEye()

products = walmart.search(keywords="batman",category="5438",walmartPage="1")
products[0].sale_price
products[0].item_id
products[0].product_url
products[0].long_description
products[0].stock
products[0].available_online

ship = products[0].get_attribute("marketplace")


best_sellers_in_5438 = walmart.getBestSellers(category=5438,page=1)
clearance_in_5438 = walmart.getClearance(category="5438",page="1")
special_buy_in_5438 = walmart.getSpecialBuy(category="5438",page="1")
trending = walmart.getTrending()
trending[0].name
"""
