from beholder.keys import keys

kz = keys.keys
from ebaysdk.finding import Connection as Finding
FindingAPI = Finding(appid=keys.keys['ebay']['production']['appid'], config_file=None)

search_params = {
    'keywords': 'batman pajamas',
    #'categoryId': '15032',
    'descriptionSearch': True,
    'sortOrder': 'BestMatch',
    'outputSelector': ['GalleryURL', 'ConditionHistogram'],
    'itemFilter': [
        {'name': 'Condition', 'value': ['New']},
        {'name': 'ListingType', 'value': 'AuctionWithBIN'},
        {'name': 'FreeShippingOnly', 'value': True},
        {'name': 'LocatedIn', 'value': 'US'}, ],
    'paginationInput': {
        'entriesPerPage': 25,
        'pageNumber': 1, }}

items = FindingAPI.execute('findItemsAdvanced', search_params).dict()
items





amazony = AmazonAPI(
    keys.keys['amazon']["production"]["AMAZON_ACCESS_KEY"],
    keys.keys['amazon']["production"]["AMAZON_SECRET_KEY"],
    keys.keys['amazon']["production"]["AMAZON_ASSOC_TAG"],)







kwargs = {
    'compare': 'walmart',
    'keywords': 'Herbal Essences Totally Twisted Curl Boosting Hair Mousse with '
             'Mixed Berry Essences, 6.8 oz',
     'item_id': '10316678',
     }
kwargs['keywords'] = kwargs['keywords'].replace("'","")
kwargs['keywords']
item = ebay.get_item()
kwargs['keywords'] = item.data['name']

for market in eyeballs:
    print(market)
    if market in kwargs.values():
        pass
    else:
        prices[market] = []
        items = eyeballs[market].search(**kwargs)

        for item in items:

            prices[market].append({
                'salePrice': item['salePrice'],
                'item_id': item['item_id']})

            item.data['compared_prices'] = {
                'time_stamp': datetime.datetime.now().__str__(),
                'prices': prices, }








from wapy.api import Wapy
wally = Wapy(keys.keys['walmart']['apiKey'])
wally_item = wally.product_lookup('16932759')
wally_item.response_handler.payload


params = {
    "walmartCatId": "1105910",
    "ResponseGroup": "base",
    "page": 1,
    "sort": "bestseller",
    "numItems": 25, }

walitems = wally.search("iphone 7", **params)
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


a = '1'
b = ''

True if a == b == "" else False

a = {
    'a': 123,
    None if False else 'key': 'value',
    }

a
