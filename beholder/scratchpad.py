from beholder.keys import keys
import requests
import re

from ebaysdk.shopping import Connection as Shopping
from ebaysdk.trading import Connection as Trading
from datetime import datetime as dt
from bs4 import BeautifulSoup
from wapy.api import Wapy
kz = keys.keys


#dict merging with new data
d1 = {'k1': 12.0, 'k2': ((58.5, 'datetime'), (56.5, 'datetime')), 'k3': 24.5}
d2 = {'k1': 11.0, 'k2': 55.0, 'k3': 26.5}
ds = [d1, d2]
d = {}

for k in d1:
    if type(d1[k]) == tuple:
        if d1[k][-1][0] != d2[k]:
            d[k] = d1[k] + ((d2[k], dt.now().__str__()), )
    else:
        if d1[k] != d2[k]:  # records
            d[k] = ((d1[k], dt.now().__str__()),(d2[k], dt.now().__str__()), )

nu_dict = {**d1, **d}
nu_dict

k = []
type(k)

#################### ebay section  ###############################
from ebaysdk.finding import Connection as FindingConnection
from beholder.keys import keys
kz = keys.keys
Finding = FindingConnection(appid=kz['ebay']['production']['appid'], config_file=None)
kwargs={}
findItems_params = {
    #'categoryId': 139973,
    'descriptionSearch': True,
    'sortOrder': 'PricePlusShippingLowest',
    #'outputSelector': ['GalleryURL', 'ConditionHistogram', 'PictureURLLarge'],
    'itemFilter': [
        {'name': 'Condition', 'value': ['New', 'Used']},
        #{'name': 'SellingState', 'value': 'EndedWithSales'}
        #{'name': 'FreeShippingOnly', 'value': kwargs['FreeShippingOnly'] if 'FreeShippingOnly' in kwargs else True},
        #{'name': 'LocatedIn', 'value': kwargs['LocatedIn'] if 'LocatedIn' in kwargs else 'US'},
        ],
    'paginationInput': {
        'entriesPerPage': 99,
        'pageNumber': 1 if 'ebayPage' not in kwargs else int(kwargs['ebayPage']), }}
findItems_params['keywords'] = 'eco friendly dog food' #-3-2-deep+cover+gex-enter+the+gecko-long+box-long+case-longbox'
findItems_params

resp_FIA = Finding.execute('findItemsAdvanced', findItems_params)
resp_FCI = Finding.execute('findCompletedItems', findItems_params)


resp = resp_FCI.dict()['searchResult']['item']


sold_items = [item for item in resp if item['sellingStatus']['sellingState'] == 'EndedWithSales']
unsold_items = [item for item in resp if item['sellingStatus']['sellingState'] != 'EndedWithSales']

len(sold_items)
len(unsold_items)

sold_items

r['searchResult']['item'][0]['sellingStatus']['currentPrice']['value']


response.connection
response.content


objects = response['searchResult']['item']


try:
    myitem = {
        "Item": {
            "Title": "Harry Potter and the Philosopher's Stone",
            "Description": "This is the first book in the Harry Potter series. In excellent condition!",
            "PrimaryCategory": {"CategoryID": "377"},
            "StartPrice": "1.0",
            "CategoryMappingAllowed": "true",
            "Country": "US",
            "ConditionID": "3000",
            "Currency": "USD",
            "DispatchTimeMax": "3",
            "ListingDuration": "Days_7",
            "ListingType": "Chinese",
            "PaymentMethods": "PayPal",
            "PayPalEmailAddress": "tkeefdddder@gmail.com",
               "PictureDetails": {"PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007"},
            "PostalCode": "95125",
            "Quantity": "1",
            "ReturnPolicy": {
                "ReturnsAcceptedOption": "ReturnsAccepted",
                "RefundOption": "MoneyBack",
                "ReturnsWithinOption": "Days_30",
                "Description": "If you are not satisfied, return the book for refund.",
                "ShippingCostPaidByOption": "Buyer"
            },
            "ShippingDetails": {
                "ShippingType": "Flat",
                "ShippingServiceOptions": {
                    "ShippingServicePriority": "1",
                    "ShippingService": "USPSMedia",
                    "ShippingServiceCost": "2.50"
                }
            },
            "Site": "US"
        }
    }

Trading.execute('VerifyAddItem', myitem)


except ConnectionError as e:
print(e)
print(e.response.dict())
pass

############################# walmart section ########################################
wally = Wapy(keys.keys['walmart']['apiKey'])

async def search(self, **kwargs):

    try:  # try to get response objects from apis

        for market_name in kwargs['markets']:

            objects = await Eyes.findItems(**kwargs)  # get resp_objects from marketplace api call
            await Eye.update_objects(kwargs={'objects': objects})  # check db_objects against ItemData db, update as needed

            response = {  # record response data to session for django template context creation
                'object_ids': [obj['item_id'] for obj in kwargs['objects']],
                'page': str(kwargs['findItems_params']['page']),
                'category': str(kwargs['findItems_params']['categoryId']),
                'keywords': kwargs['keywords'], }

            session.data['market_data'][market_name] = {**session.data['market_data'][market_name], **response}
            await session.save()

            print(f"{str(len(response['object_ids']))} {market_name} objects added to session.")

    except Exception as e:
        print(f"error retrieving items on {market_name}!: {e}") # queries marketplace apis for objects. # queries marketplaces for objects

wally_item = wally.product_lookup('16932759')
wally_item.response_handler.payload

cat_items = wally.search("", **{"categoryId": "7796869_1097870_1680603"})
clearance_cat_items = wally.clearance_products([1680603])
cat_items = [item.response_handler.payload for item in cat_items]
len(cat_items)
cat_items[0]

# amazon section
kwargs = {
    'keywords': 'baby stroller',
    'page': '1', }
kwargs_url_string = ''

for key, value in kwargs.items():
    if key == 'keywords' or key == 'page':
        value = value.replace(' ', '+')
        kwargs_url_string += str(key + '=' + value + '&')



amazon_search_url = 'https://www.amazon.com/dp/B06XNYLY5R'
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


B06XNYLY5R

############################# scraper section ########################################
kwargs = {}
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}
kwargs['keywords'] = "party favor"
kwargs_url_string = ''
kwargs['page'] = kwargs['chewy_page'] if 'chewy_page' in kwargs else '1'

for key, value in kwargs.items():

    if key == 'keywords' or key == '_page':
        key = key.replace('keywords','query')
        value = value.replace(' ', '+')
        kwargs_url_string += str(key + '=' + value + '&')

search_url = 'https://www.chewy.com/s/?' + kwargs_url_string
search_url
response = requests.get(search_url, headers=headers)
soup = BeautifulSoup(response.content, 'lxml')
search_results = soup.find_all('article', 'cw-card')
objects = []
chewy_url
for elem in search_results:

    obj = {
        'item_id': elem.find('div', class_='ga-eec__id').string,
        'market': 'chewy',
        'prices': {},
        'notes': {},
        'product_url': chewy_url + elem.find('a')['href'],
        'medium_image': 'https:'+ elem.find('img')['src'],
        'images': ['https:'+ elem.find('img')['src']],
        'name': elem.find('div', class_='ga-eec__name').string.replace('"', '\"'),
        'stock': 'Available? Check availablility by id?',
        'sale_price': elem.find('div', class_='ga-eec__price').string,
        'customer_rating': elem.find('p', class_='rating').find('img')['src'][-7:-4].replace('_','.')+' / 5.0',
        'customer_rating_count': elem.find('p', class_='rating').find('span').string,
        }

    objects.append(obj)

objects[0]
