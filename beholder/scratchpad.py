from beholder.keys import keys
import requests
from ebaysdk.finding import Connection as Finding
import datetime

kz = keys.keys
FindingAPI = Finding(appid=keys.keys['ebay']['production']['appid'], config_file=None)

pages = range(1,6)
kwargs = {'keywords': 'Samsung Galaxy 6S'}
prices = []

search_params = {
    'keywords': kwargs['keywords'],
    'descriptionSearch': True,
    'sortOrder': 'BestMatch',
    'outputSelector': ['AspectHistogram', 'CategoryHistogram'],
    'itemFilter': [
        {'name': 'SoldItemsOnly', 'value': True},
        {'name': 'ListingType', 'value': 'AuctionWithBIN'},
        {'name': 'Condition', 'value': ['New']},
        {'name': 'LocatedIn', 'value': 'US'}, ],
    'paginationInput': {
        'entriesPerPage': 25,
        'pageNumber': 2, }}
response = FindingAPI.execute('findCompletedItems', search_params).dict()
len(response['searchResult']['item'])
response['searchResult']['item'][0]


for page in pages:

    search_params = {
        'keywords': kwargs['keywords'],
        'descriptionSearch': True,
        'sortOrder': 'BestMatch',
        'outputSelector': ['GalleryURL', 'ConditionHistogram'],
        'itemFilter': [
            {'name': 'SoldItemsOnly', 'value': True},
            {'name': 'ListingType', 'value': 'AuctionWithBIN'},
            {'name': 'Condition', 'value': ['New']},
            {'name': 'LocatedIn', 'value': 'US'}, ],
        'paginationInput': {
            'entriesPerPage': 25,
            'pageNumber': page, }}

    response = FindingAPI.execute('findCompletedItems', search_params).dict()
    if 'errorMessage' in response:
        print(response['errorMessage'])
    print(response['searchResult'].keys())
    print("Found "+response['searchResult']['_count']+" prices.")

    items = response['searchResult']['item']

    for item in items:

        _prices = {
            'name': item['title'],
            'item_id': item['itemId'],
            'market': 'ebay',
            'thumbnail_image': item['galleryURL'] if item.get('galleryURL') else None,
            'product_url': item['viewItemURL'],
            'sold_for': item['sellingStatus']['currentPrice']['value'],
            'shipping_cost': item['shippingInfo']['shippingServiceCost']['value'] if item.get('shippingServiceCost') else None,
            'sold_date': item['listingInfo']['endTime'] if 'listingInfo' in item else None,
            'sold_zip': item['postalCode'] if item.get('postalCode') else None,
            'time_stamp': datetime.datetime.now().__str__(), }

        prices.append(_prices)

    if int(response['searchResult']['_count']) < 25:
        break


for price in prices:
    print(price['item_id'], ": $", price['sold_for'], " : ", price['time_stamp'])

a ={}

a['b']['c'] = 123

for i in range(1,5):
    print(i)
amazony = AmazonAPI(
    keys.keys['amazon']["production"]["AMAZON_ACCESS_KEY"],
    keys.keys['amazon']["production"]["AMAZON_SECRET_KEY"],
    keys.keys['amazon']["production"]["AMAZON_ASSOC_TAG"],)





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

import requests
taxonomy = requests.get(
    'http://api.walmartlabs.com/v1/taxonomy?apiKey='
    + keys.keys['walmart']['apiKey']).json()

taxonomy

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
