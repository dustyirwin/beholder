from beholder.eyeballs import Walmart, Ebay
from beholder.keys import keys

kz = keys.keys
wally = Walmart()
wally.categories
amazony = AmazonAPI(
    keys.keys['amazon']["production"]["AMAZON_ACCESS_KEY"],
    keys.keys['amazon']["production"]["AMAZON_SECRET_KEY"],
    keys.keys['amazon']["production"]["AMAZON_ASSOC_TAG"],)
ebay = Ebay()
shoppy = Shopping(appid=kz['ebay']['production']['appid'], config_file=None)

params = {
    "keywords": "iphone 7",
    "walmartCatId": "1105910",
    "ResponseGroup": "base",
    "page": 1,
    "sort": "bestseller",
    "numItems": 25, }

walitems = wally.search(**params)
walitems[0].category_node
walitems[0].category_path
walitems[0].images[0]
walitems[0].medium_image
walitems[0].num_reviews
itemz = ebay.search(
    keywords="cell phone",
    ebayCatId=15032)
itemz[0]
itm = itemz[0]
imgs[0][0]


a = '1'
b = ''

True if a == b == "" else False
