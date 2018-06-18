from beholder.keys import keys
import requests
from ebaysdk.finding import Connection as Finding
import datetime

kz = keys.keys

# ebay section
FindingAPI = Finding(appid=keys.keys['ebay']['production']['appid'], config_file=None)
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


# walmart section
from wapy.api import Wapy
wally = Wapy(keys.keys['walmart']['apiKey'])
wally_item = wally.product_lookup('16932759')
wally_item.response_handler.payload




# amazon section
kwargs = {
    'keywords': 'lego batman',
    'page': '1', }

kwargs_url_string = ''

for key, value in kwargs.items():
    value = value.replace(' ', '%20')
    kwargs_url_string += str(key + '=' + value + '&')

kwargs_url_string

amazon_search_results_url = 'https://www.amazon.com/s/ref=sr_pg_'+ kwargs['page'] +'?&' + kwargs_url_string

response = requests.get(amazon_search_url, headers={
    'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})

page_data = response.__dict__
page_data
len(page_data)


next_page_url_ =
'''
<a title="Next Page" id="pagnNextLink" class="pagnNext" href="/s/ref=sr_pg_2?rh=n%3A2335752011%2Cn%
3A7072561011%2Ck%3Aiphone+6s&amp;page=2&amp;keywords=iphone+6s&amp;ie=UTF8&amp;qid=1529292428">
<span id="pagnNextString">Next Page</span><span class="srSprite pagnNextArrow"></span></a>
'''


# for loop over search results in

sales_price_element =


name_element =
'''
<a class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"
title="Apple iPhone 6S 16GB - GSM Unlocked - Rose Gold (Certified Refurbished)"
href="https://www.amazon.com/Apple-iPhone-6S-16GB-Refurbished/dp/B01J8PBEUM/ref=sr_1_1?s=
wireless&amp;ie=UTF8&amp;qid=1529292428&amp;sr=1-1&amp;keywords=iphone+6s"><h2 data-attribute=
"Apple iPhone 6S 16GB - GSM Unlocked - Rose Gold (Certified Refurbished)" data-max-rows="0"
class="a-size-medium s-inline  s-access-title  a-text-normal">Apple iPhone 6S 16GB -
GSM Unlocked - Rose Gold (Certified Refurbished)</h2></a>
'''

medium_image_element =
"""
<img src="https://images-na.ssl-images-amazon.com/images/I/41jUosGQiDL._AC_US218_.jpg"
srcset="https://images-na.ssl-images-amazon.com/images/I/41jUosGQiDL._AC_US218_.jpg 1x,
https://images-na.ssl-images-amazon.com/images/I/41jUosGQiDL._AC_US327_FMwebp_QL65_.jpg 1.5x,
https://images-na.ssl-images-amazon.com/images/I/41jUosGQiDL._AC_US436_FMwebp_QL65_.jpg 2x,
https://images-na.ssl-images-amazon.com/images/I/41jUosGQiDL._AC_US500_FMwebp_QL65_.jpg 2.2935x"
width="218" height="218" alt="Apple iPhone 6S 16GB - GSM Unlocked - Rose Gold (Certified Refurbished)"
class="s-access-image cfMarker" data-search-image-load="">
"""


for item in items:

    item[item]['medium_image'] = 'mediumImagePath'
    item[item]['price'] = 'pricePath'
    item[item]['description'] = 'descriptionPath'
    item[item]['upc'] = 'upcPath'
    item[item]['name'] = 'namePath'
    item[item]['rating'] = 'ratingPath'
    item[item]['availability'] = 'availabilityPath'
