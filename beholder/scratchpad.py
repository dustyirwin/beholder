from beholder.keys import keys
import requests
import re
from ebaysdk.finding import Connection as Finding
import datetime
from bs4 import BeautifulSoup
from wapy.api import Wapy
kz = keys.keys


# ebay section
kwargs = {
    'keywords': 'baby stroller',
    'page': '1', }
FindingAPI = Finding(appid=keys.keys['ebay']['production']['appid'], config_file=None)
hist_search_params = {
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
findItemsAdvanced_params = {
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
response = FindingAPI.execute('findCompletedItems', hist_search_params).dict()
response = FindingAPI.execute('findItemsAdvanced', findItemsAdvanced_params).dict()
response
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
wally = Wapy(keys.keys['walmart']['apiKey'])
wally_item = wally.product_lookup('16932759')
wally_item.response_handler.payload


# amazon section
kwargs = {
    'keywords': 'baby stroller',
    'page': '1', }
kwargs_url_string = ''

for key, value in kwargs.items():
    if key == 'keywords' or key == 'page':
        value = value.replace(' ', '+')
        kwargs_url_string += str(key + '=' + value + '&')


amazon_search_url = 'https://www.amazon.com/dp/' + kwargs_url_string
response = requests.get(amazon_search_url, headers={
    'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
soup = BeautifulSoup(response.content, 'lxml')

results_ul = soup.find('ul', id='s-results-list-atf')

search_results = soup.find_all('li', class_='s-result-item')

search_results[3].find('i', class_='a-icon-prime')

search_results[3].find_all('i')[0]['class']

search_results[2].find(title=True) == None


type(name)
name
items = []

for i, elem in enumerate(search_results):

    if 'AdHolder' not in elem['class'] and elem.has_attr('data-asin') and elem.find(title=True) != None:

        item = {
            'item_id': elem['data-asin'],
            'product_url': elem.find('a')['href'],
            'medium_image': elem.find('img')['src'],
            'name': elem.find(title=True)['title'],
            'customer_rating': elem.find('span', {'class': ['a-icon-alt']}).get_text(), }
        try:
            item['sale_price'] = elem.find('span', class_='a-offscreen').get_text()[1:]
        except Exception:
            item['sale_price'] = elem.find('span', class_="a-size-base").get_text()[1:]

        items.append(item)

len(items)
items


B06XNYLY5R
