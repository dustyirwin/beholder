import pandas
from beholder.keys import keys
from beholder.eyeballs import Ebay
from beholder.eyeballs import Walmart


wally = Walmart()
ebay = Ebay()


walmartItems = []

wally.getClearance(walmartCatId="1105910")  # Straight-talk wireless: 1105910_1045119

wally.categories[0]
try:
    wally.getClearance(walmartCatId=wally.categories[0]['id'])
except Exception as e:
    print(e)
wally.keys['walmart']['apiKey']
