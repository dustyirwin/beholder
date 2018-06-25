from beholder.keys import keys  # api keys
# from mws import Products as amazonProducts  # amazon api
from wapy.api import Wapy  # walmart api
from ebaysdk.finding import Connection as Finding  # ebay apis
from ebaysdk.shopping import Connection as Shopping
# from ebaysdk.trading import Connection as Trading
from inventory.models import ItemData  # item database
from search.models import SessionData  # session data
from bs4 import BeautifulSoup
import datetime
import requests
import re
import isodate
# import traceback


'''
BEHOLDER v0.3 written by Dustin Irwin 2018
'''


class Eye:

    def __init__(self):
        if SessionData.objects.filter(user='dusty').exists():
            self.session = SessionData.objects.get(user='dusty')
        else:
            self.session = SessionData(
                session_id='testing',
                user='dusty',
                data={'markets': [
                        {
                            'name': 'walmart',
                            'categories': [
                                {'name': 'Arts, Crafts & Sewing', 'id': '1334134'}, {'name': 'Auto & Tires', 'id': '91083'},
                                {'name': 'Baby', 'id': '5427'}, {'name': 'Beauty', 'id': '1085666'}, {'name': 'Books', 'id': '3920'},
                                {'name': 'Cell Phones', 'id': '1105910'}, {'name': 'Clothing', 'id': '5438'},
                                {'name': 'Electronics', 'id': '3944'}, {'name': 'Food', 'id': '976759'},
                                {'name': 'Gifts & Registry', 'id': '1094765'}, {'name': 'Health', 'id': '976760'},
                                {'name': 'Home', 'id': '4044'}, {'name': 'Home Improvement', 'id': '1072864'},
                                {'name': 'Household Essentials', 'id': '1115193'}, {'name': 'Industrial & Scientific', 'id': '6197502'},
                                {'name': 'Jewelry', 'id': '3891'}, {'name': 'Movies & TV Shows', 'id': '4096'},
                                {'name': 'Music on CD or Vinyl', 'id': '4104'}, {'name': 'Musical Instruments', 'id': '7796869'},
                                {'name': 'Office', 'id': '1229749'}, {'name': 'Party & Occasions', 'id': '2637'},
                                {'name': 'Patio & Garden', 'id': '5428'}, {'name': 'Personal Care', 'id': '1005862'},
                                {'name': 'Pets', 'id': '5440'}, {'name': 'Photo Center', 'id': '5426'},
                                {'name': 'Premium Beauty', 'id': '7924299'}, {'name': 'Seasonal', 'id': '1085632'},
                                {'name': 'Sports & Outdoors', 'id': '4125'}, {'name': 'Toys', 'id': '4171'},
                                {'name': 'Video Games', 'id': '2636'}, {'name': 'Walmart for Business', 'id': '6735581'},
                                {'name': 'Trending', 'id': 'specialQuery'}, ],
                            'search_filters': [
                                {'name': 'Best Sellers', 'value': False},
                                {'name': 'Clearance', 'value': False},
                                {'name': 'Special Buy', 'value': False},
                                {'name': 'Trending', 'value': False},
                                {'name': 'FreeShip', 'value': True}, ], },
                        {
                            'name': 'ebay',
                            'categories': [
                                {'name': 'Antiques', 'id': '20081'},{'name': 'Art', 'id': '550'},
                                {'name': 'Baby', 'id': '2984'},{'name': 'Books', 'id': '267'},
                                {'name': 'Business & Industrial', 'id': '12576'},{'name': 'Cell Phones & Accessories', 'id': '15032'},
                                {'name': 'Clothing,  Shoes & Accessories', 'id': '11450'},{'name': 'Coins & Paper Money', 'id': '11116'},
                                {'name': 'Collectibles', 'id': '1'},{'name': 'Camera & Photo', 'id': '625'},
                                {'name': 'Computers/Tablets & Networking', 'id': '58058'},{'name': 'Consumer Electronics', 'id': '293'},
                                {'name': 'Crafts', 'id': '14339'},{'name': 'Dolls & Bears', 'id': '237'},
                                {'name': 'DVDs & Movies', 'id': '11232'},{'name': 'Entertainment Memorabilia', 'id': '45100'},
                                {'name': 'Everything Else', 'id': '99'},{'name': 'Gift Cards & Coupons', 'id': '172008'},
                                {'name': 'Health & Beauty', 'id': '26395'},{'name': 'Home & Garden', 'id': '11700'},
                                {'name': 'Jewelry & Watches', 'id': '281'},{'name': 'Music', 'id': '11233'},
                                {'name': 'Musical Instruments & Gear', 'id': '619'},{'name': 'Pet Supplies', 'id': '1281'},{'name': 'Pottery & Glass', 'id': '870'},
                                {'name': 'Real Estate', 'id': '10542'},{'name': 'Specialty Services', 'id': '316'},{'name': 'Sporting Goods', 'id': '888'},
                                {'name': 'Sports Mem,  Cards & Fan Shop', 'id': '64482'},{'name': 'Stamps', 'id': '260'},
                                {'name': 'Tickets & Experiences', 'id': '1305'},{'name': 'Toys & Hobbies', 'id': '220'},
                                {'name': 'Travel', 'id': '3252'},{'name': 'Video Games & Consoles', 'id': '1249'}, ],
                            'search_filters': [
                                {'name': 'New', 'value': True},
                                {'name': 'BIN', 'value': True},
                                {'name': 'FreeShip', 'value': True},
                                {'name': 'InUS', 'value': True},
                                {'name': 'Hist', 'value': False}, ], },
                        {
                            'name': 'amazon',
                            'categories': [
                                {'name': 'Apparel', 'id': 'Apparel'},
                                {'name': 'Appliances', 'id': 'Appliances'},
                                {'name': 'ArtsAndCrafts', 'id': 'ArtsAndCrafts'},
                                {'name': 'Automotive', 'id': 'Automotive'},
                                {'name': 'Baby', 'id': 'Baby'},
                                {'name': 'Beauty', 'id': 'Beauty'},
                                {'name': 'Blended', 'id': 'Blended'},
                                {'name': 'Books', 'id': 'Books'},
                                {'name': 'Classical', 'id': 'Classical'},
                                {'name': 'Collectibles', 'id': 'Collectibles'},
                                {'name': 'DVD', 'id': 'DVD'},
                                {'name': 'DigitalMusic', 'id': 'DigitalMusic'},
                                {'name': 'Electronics', 'id': 'Electronics'},
                                {'name': 'Fashion', 'id': 'Fashion'},
                                {'name': 'FashionBaby', 'id': 'FashionBaby'},
                                {'name': 'FashionBoys', 'id': 'FashionBoys'},
                                {'name': 'FashionGirls', 'id': 'FashionGirls'},
                                {'name': 'FashionMen', 'id': 'FashionMen'},
                                {'name': 'FashionWomen', 'id': 'FashionWomen'},
                                {'name': 'GiftCards', 'id': 'GiftCards'},
                                {'name': 'GourmetFood', 'id': 'GourmetFood'},
                                {'name': 'Grocery', 'id': 'Grocery'},
                                {'name': 'Handmade', 'id': 'Handmade'},
                                {'name': 'HealthPersonalCare', 'id': 'HealthPersonalCare'},
                                {'name': 'HomeAndBusinessServices', 'id': 'HomeAndBusinessServices'},
                                {'name': 'HomeGarden', 'id': 'HomeGarden'},
                                {'name': 'Industrial', 'id': 'Industrial'},
                                {'name': 'Jewelry', 'id': 'Jewelry'},
                                {'name': 'KindleStore', 'id': 'KindleStore'},
                                {'name': 'Kitchen', 'id': 'Kitchen'},
                                {'name': 'LawnAndGarden', 'id': 'LawnAndGarden'},
                                {'name': 'Luggage', 'id': 'Luggage'},
                                {'name': 'MP3Downloads', 'id': 'MP3Downloads'},
                                {'name': 'Magazines', 'id': 'Magazines'},
                                {'name': 'Marketplace', 'id': 'Marketplace'},
                                {'name': 'Miscellaneous', 'id': 'Miscellaneous'},
                                {'name': 'MobileApps', 'id': 'MobileApps'},
                                {'name': 'Movies', 'id': 'Movies'},
                                {'name': 'Music', 'id': 'Music'},
                                {'name': 'MusicTracks', 'id': 'MusicTracks'},
                                {'name': 'MusicalInstruments', 'id': 'MusicalInstruments'},
                                {'name': 'OfficeProducts', 'id': 'OfficeProducts'},
                                {'name': 'OutdoorLiving', 'id': 'OutdoorLiving'},
                                {'name': 'PCHardware', 'id': 'PCHardware'},
                                {'name': 'Pantry', 'id': 'Pantry'},
                                {'name': 'PetSupplies', 'id': 'PetSupplies'},
                                {'name': 'Photo', 'id': 'Photo'},
                                {'name': 'Shoes', 'id': 'Shoes'},
                                {'name': 'Software', 'id': 'Software'},
                                {'name': 'SportingGoods', 'id': 'SportingGoods'},
                                {'name': 'Tools', 'id': 'Tools'},
                                {'name': 'Toys', 'id': 'Toys'},
                                {'name': 'UnboxVideo', 'id': 'UnboxVideo'},
                                {'name': 'VHS', 'id': 'VHS'},
                                {'name': 'Vehicles', 'id': 'Vehicles'},
                                {'name': 'Video', 'id': 'Video'},
                                {'name': 'VideoGames', 'id': 'VideoGames'},
                                {'name': 'Watches', 'id': 'Watches'},
                                {'name': 'Wine', 'id': 'Wine'},
                                {'name': 'Wireless', 'id': 'Wireless'},
                        {'name': 'WirelessAccessories', 'id': 'WirelessAccessories'}, ],
                            'search_filters': [
                                {'name': 'Prime', 'value': False},
                                {'name': 'Used', 'value': False}, ], }, ]}
            ).save()


class Walmart(Eye):

    def __init__(self):
        self.walmart = Wapy(keys.keys['walmart']['apiKey'])
        super().__init__()

    def findItems(self, **kwargs):
        findItems_params = {
            'ResponseGroup': 'full',
            'categoryId': kwargs['walmartCatId'] if bool(kwargs['walmartCatId']) else None,
            'page': int(kwargs['walmartPage']) if 'walmartPage' in kwargs else 1,
            'sort': 'bestseller',
            'numItems': 25}

        try:
            items = self.walmart.search(kwargs['keywords'], **findItems_params)
            items = [{
                    'item_id': item.item_id,
                    'name': item.name,
                    'sale_price': item.sale_price,
                    'upc': item.upc,
                    'description': item.short_description,
                    'stock': item.stock,
                    'medium_image': item.medium_image,
                    'images': item.images,
                    'customer_rating': item.customer_rating,
                    'model_number': item.model_number,
                    'category_node': item.category_node,
                    'category_path': item.category_path,
                    'brand_name': item.brand_name,
                    'product_url': item.product_url} for item in items]

        except Exception as e:
            print('Error retrieving items on walmart: ', e)
            items = []

        self.session.data['walmart'] = {
            'items': items,
            'page': findItems_params['page'],
            'category': findItems_params['categoryId']}

        self.session.save()

        print(str(len(self.session.data['walmart']['items'])) + ' items found on walmart.')

    def getItemDetails(self, item={}, **kwargs):
        return {**self.WalmartAPI.product_lookup(kwargs['item_id']).response_handler.payload, **item}

    def getBestSellers(self, **kwargs):
        return self.WalmartAPI.bestseller_products(int(kwargs['walmartCatId']))

    def getClearance(self, **kwargs):
        return self.WalmartAPI.clearance_products(int(kwargs['walmartCatId']))

    def getSpecialBuy(self, **kwargs):
        return self.WalmartAPI.special_buy_products(int(kwargs['walmartCatId']))

    def getTrending(self):
        return self.WalmartAPI.trending_products()


class Ebay(Eye):

    def __init__(self):
        self.FindingAPI = Finding(appid=keys.keys['ebay']['production']['appid'], config_file=None)
        self.ShoppingAPI = Shopping(appid=keys.keys['ebay']['production']['appid'], config_file=None)
        super().__init__()

    def findItems(self, **kwargs):
        findItems_params = {
            'descriptionSearch': True,
            'sortOrder': 'BestMatch',
            'outputSelector': ['GalleryURL', 'ConditionHistogram', 'PictureURLLarge'],
            'itemFilter': [
                {'name': 'Condition', 'value': ['New']},
                {'name': 'ListingType', 'value': 'AuctionWithBIN'},
                {'name': 'FreeShippingOnly', 'value': True},
                {'name': 'LocatedIn', 'value': 'US'}, ],
            'paginationInput': {
                'entriesPerPage': 24,
                'pageNumber': 1 if 'ebayPage' not in kwargs else int(kwargs['ebayPage']), }}

        if bool(kwargs['keywords']):
            findItems_params['keywords'] = kwargs['keywords']

        if bool(kwargs['ebayCatId']):
            findItems_params['categoryId'] = kwargs['ebayCatId']

        try:
            items = self.FindingAPI.execute('findItemsAdvanced', findItems_params).dict()['searchResult']['item']
            items = [{
                'name': item['title'],
                'item_id': item['itemId'],
                'customer_rating': isodate.parse_duration(item['sellingStatus']['timeLeft']).__str__(),
                'sale_price': item['listingInfo']['buyItNowPrice']['value'] if item.get('buyItNowPrice') else item['sellingStatus']['currentPrice']['value'],
                'product_url': item['viewItemURL'],
                'medium_image': item['galleryURL'],
                'images': [item['pictureURLLarge'] if 'pictureURLLarge' in item else None],
                'stock': item['sellingStatus']['sellingState'],
                'category_node': item['primaryCategory']['categoryId'],
                'category_path': item['primaryCategory']['categoryName'], } for item in items]

        except Exception as e:
            print('Error getting items on eBay: ', e)
            items = []

        self.session.data['ebay'] = {
            'items': items,
            'page': findItems_params['paginationInput']['pageNumber'],
            'category': findItems_params['categoryId'] if 'categoryId' in findItems_params else None}

        self.session.save()

        print(str(len(self.session.data['ebay']['items'])) + ' items found on ebay.')

    def getItemDetails(self, item={}, **kwargs):
        return {**self.ShoppingAPI.execute(
            'GetSingleItem', {'itemID': kwargs['item_id']}).dict()['Item'], **item}

    def getPriceHistories(self, **kwargs):
        item = self.ItemData.objects.get(item_id=kwargs['get_prices'])
        item.data['prices']['query'] = kwargs['query']
        prices = []

        for page in range(1, 4):

            self.market['priceHistories_params'] = {
                'keywords': kwargs['keywords'] if kwargs.get('keywords') else 'happy tree friends',
                'descriptionSearch': True,
                'sortOrder': 'BestMatch',
                'outputSelector': ['CategoryHistogram', 'AspectHistogram', 'SellerInfo', ],
                'itemFilter': self.market['query_options'],
                'paginationInput': {
                    'entriesPerPage': 25,
                    'pageNumber': page, }}
            response = self.FindingAPI.execute('findCompletedItems', self.market['priceHistories_params']).dict()

            if response['ack'] == 'Success' and response['searchResult']['_count'] == '0':
                item.data['prices']['prices'] = []
                break

            else:
                items = response['searchResult']['item']

                for _item in items:

                    price = {
                        'name': item['title'],
                        'item_id': item['itemId'],
                        'small_image': item['galleryURL'],
                        'product_url': item['viewItemURL'],
                        'market': 'ebay',
                        'sold_for': item['listingInfo']['buyItNowPrice']['value'],
                        'shipping_cost': item['shippingInfo']['shippingServiceCost']['value'],
                        'sold_date': item['listingInfo']['endTime'],
                        'notes': [],
                        'prices': {}, }

                    prices.append(price)

                if int(response['searchResult']['_count']) < 25:
                    item.data['prices']['prices'] = prices
                    break

        item.data['prices']['count'] = len(item.data['prices']['prices'])
        item.save()

    def priceLot(self, **kwargs):
            totalSales = 0
            totalNet = 0
            totalFBAFees = 0
            totalReferralFees = 0
            totalTTP = 0
            totalWeight = 0
            totalFBAShipping = 0
            totalSellFees = 5.0
            amazonItems = []

            if kwargs['ebayModel'].objects.filter(
                    itemId=kwargs['itemId']).exists():
                ebayItem = kwargs['ebayModel'].objects.get(
                    itemId=kwargs['itemId'])
            else:
                _data = self.shoppingConnection.execute(
                    'GetSingleItem',
                    {'itemID': kwargs['itemId'],
                     'includeSelector': 'TextDescription, ShippingCosts'}
                ).dict()['Item']
                _data = {**_data, **{
                    'name': _data['Title'],
                    'TimeLeftStr': isodate.parse_duration(
                        _data['TimeLeft']).__str__(),
                    'keywords': kwargs['keywords'],
                    'financial': {
                        'current': {},
                        'historical': {}
                        },
                    'ASINInfo': {},
                    'priced': False,
                    'purchased': False,
                    'created': datetime.datetime.now().__str__(),
                    'lastModified': datetime.datetime.now().__str__(),
                    'selected': 0,
                }}

                ebayItem = kwargs['ebayModel'](
                    name=_data['name'],
                    itemId=_data['ItemID'],
                    data=_data,
                ).save()

                ebayItem = kwargs['ebayModel'].objects.get(
                    itemId=kwargs['itemId'])

            if 'currentPrice' in kwargs:
                ebayItem.data['ConvertedCurrentPrice'][
                    'value'] = kwargs['currentPrice']
                ebayItem.save()

            if 'ebayShipping' in kwargs:
                ebayItem.data['ShippingCostSummary'][
                    'ShippingServiceCost'] = {'value': float(
                        kwargs['ebayShipping'])}
                ebayShipping = float(kwargs['ebayShipping'])
                ebayItem.save()
            elif 'ShippingServiceCost' in ebayItem.data['ShippingCostSummary']:
                ebayShipping = float(ebayItem.data['ShippingCostSummary'][
                    'ShippingServiceCost']['value'])
            else:
                ebayShipping = 0.0

            if 'ASIN' in kwargs:
                if 'amazonCatId' in kwargs:
                    amazon = self.amazonAPI()
                    amazon.scrape(kwargs)
                    amazon.fees(kwargs)
                    amazonItem = kwargs['amazonModel'].objects.get(
                        ASIN=kwargs['ASIN'])

                ebayItem = kwargs['ebayModel'].objects.get(
                    itemId=kwargs['itemId'])

                if not kwargs['ASIN'] in ebayItem.data[
                        'ASINInfo'].keys():
                    amazonItem.data['selected'] += 1
                    ebayItem.data['ASINInfo'][kwargs['ASIN']] = {
                               'qty': 1,
                               'amazonCatId': kwargs['amazonCatId'],
                               'title': amazonItem.name
                               }
                if 'listPrice' in kwargs:
                    amazonItem.data['financial']['current'][
                        'listPrice'] = kwargs['listPrice']
                else:
                    if amazonItem.data[
                            'financial']['current']['listPrice'] == 0.0:
                        amazonItem.data['financial']['current'][
                            'listPrice'] = amazonItem.data['financial'][
                                'current']['primePrices']['lowPrime']
                if 'FBAFee' in kwargs:
                    amazonItem.data['financial']['current'][
                        'FBAFee'] = kwargs['FBAFee']
                if 'refFee' in kwargs:
                    amazonItem.data['financial']['current'][
                        'refFee'] = kwargs['refFee']
                if 'FBAShip' in kwargs:
                    amazonItem.data['financial']['current'][
                        'FBAShip'] = kwargs['FBAShip']
                if 'Weight' in kwargs:
                    amazonItem.data['financial']['current'][
                        'weight'] = float(kwargs['Weight'])
                if 'TTP' in kwargs:
                    amazonItem.data['financial']['current'][
                        'TTP'] = int(float(kwargs['TTP']))
                if 'qty' in kwargs:
                    ebayItem.data['ASINInfo'][kwargs['ASIN']][
                        'qty'] = kwargs['qty']
                    amazonItem.data['financial']['current'][
                        'qty'] = kwargs['qty']

                amazonItem.save()
                ebayItem.save()

            ebayItem = kwargs['ebayModel'].objects.get(
                itemId=kwargs['itemId'])
            if ebayItem.data['ASINInfo'] != {}:
                for ASIN, info in ebayItem.data['ASINInfo'].items():
                    _ = kwargs['amazonModel'].objects.get(ASIN=ASIN)
                    totalSales += float(_.data['financial']['current'][
                        'listPrice']) * int(info['qty'])
                    totalFBAFees += float(_.data['financial']['current'][
                        'FBAFee']) * int(info['qty'])
                    totalReferralFees += float(_.data['financial']['current'][
                        'refFee']) * int(info['qty'])
                    totalSellFees += float((_.data['financial']['current'][
                        'refFee']) + 1.80) * int(info['qty'])
                    totalTTP += float(_.data['financial']['current'][
                        'TTP']) * int(info['qty'])
                    totalFBAShipping += float(_.data['financial']['current'][
                        'FBAShip']) * int(info['qty'])
                    totalNet += float(_.data['financial']['current'][
                        'net']) * int(info['qty'])
                    totalWeight += float(_.data['financial']['current'][
                        'Weight']) * int(info['qty'])
                    amazonItems.append(_)

                ebayItem.data['financial']['current'] = {
                    'totalWeight': round(totalWeight, 2),
                    'totalSales': round(totalSales, 2),
                    'totalFBAFees': round(totalFBAFees, 2),
                    'totalReferralFees': round(totalReferralFees, 2),
                    'totalSellFees': round(totalSellFees, 2),
                    'totalTTP': round((totalTTP + 10), 2),
                    'totalFBAShipping': round(totalFBAShipping, 2),
                    'totalNet': round(totalNet - 5, 2),
                    'profit40': round(
                        totalNet - 5 - ((totalNet - 5) / 1.4 - ebayShipping)
                        - ebayShipping, 2),
                    'maxBid40': round((totalNet - 5) / 1.4 - ebayShipping, 2),
                    'maxBid100LR': round(
                        totalNet - 5 - 100*(totalTTP / 60) - ebayShipping, 2),
                    'laborRate40': round(
                        (totalNet - ((totalNet - 5) / 1.4 - ebayShipping) - 5
                         - ebayShipping) / ((totalTTP + 10) / 60), 2),
                }
                ebayItem.save()

            return {'ebayItem': ebayItem, 'amazonItems': amazonItems}


class Amazon(Eye):

    def __init__(self):
        super().__init__()

    def findItems(self, **kwargs):
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}
        kwargs_url_string = ''
        kwargs['page'] = kwargs['amazonPage'] if 'amazonPage' in kwargs else '1'

        for key, value in kwargs.items():

            if key == 'keywords' or key == 'page':
                value = value.replace(' ', '+')
                kwargs_url_string += str(key + '=' + value + '&')

        amazon_search_url = 'https://www.amazon.com/s/?' + kwargs_url_string
        response = requests.get(amazon_search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        search_results = soup.find_all('li', class_='s-result-item')
        items = []

        for elem in search_results:

            if 'AdHolder' not in elem['class'] and elem.has_attr('data-asin') and elem.find(title=True) != None:

                item = {
                    'item_id': elem['data-asin'],
                    'product_url': elem.find('a')['href'],
                    'medium_image': elem.find('img')['src'],
                    'images': [elem.find('img')['src']],
                    'name': elem.find(title=True)['title'],
                    'stock': 'Prime' if elem.find('i', class_='a-icon-prime') else 'No Prime',
                    'customer_rating': elem.find('i', class_='a-icon-star').span.get_text() if elem.find('i', class_='a-icon-star') else None, }
                try:
                    item['sale_price'] = elem.find('span', class_='a-offscreen').get_text()[1:]
                except Exception:
                    try:
                        item['sale_price'] = elem.find('span', class_="a-size-base").get_text()[1:]
                    except Exception:
                        pass

                items.append(item)

        self.session.data['amazon'] = {
            'items': items,
            'page': kwargs['page'],
            'category': kwargs['amazonCatId'] if 'amazonCatId' in kwargs else None}

        self.session.save()

        print(str(len(self.session.data['amazon']['items'])) + ' items found on amazon.')

    def getItemDetails(self, item={}, **kwargs):
        amazon_search_url = 'https://www.amazon.com/dp/' + kwargs['item_id']
        response = requests.get(amazon_search_url, headers=self.market['headers'])
        soup = BeautifulSoup(response.content, 'lxml')
        _item = {
            'description': soup.find('ul', class_='a-spacing-none'), }
        item = {**item, **_item, **{

            'keywords': kwargs['keywords'], }}

        item = ItemData(
            item_id=item['item_id'],
            name=item['name'],
            data=item, ).save()

        return item

    def getPrimePrices(self, **kwargs):
        priceList = []

        primeURL = 'https://www.amazon.com/gp/offer-listing/'
        + kwargs['item_id']
        + '/ref=olp_f_primeEligible?ie=UTF8&f_primeEligible'
        + '=true&f_used=true&f_usedAcceptable=true&f_usedGood=true&f'
        + '_usedLikeNew=true&f_usedVeryGood=true'

        response = requests.get(primeURL, headers={
            'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/'
            + '537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content, 'lxml')
        priceColumn = soup.find_all(
            'span', 'a-size-large a-color-price olpOfferPrice a-text-bold')
        primeRE = r'\d+.\d+'

        for _ in priceColumn:
            price = re.search(primeRE, str(_))
            priceList.append(float(price.group(0).replace(',', '')))

        if len(priceList) > 0:
            item = ItemData.objects.get(
                item_id=kwargs.get('item_id'))
            item.data['financial']['historical'].append(
                item.data['financial']['current'])
            item.data['financial']['current']['primePrices'] = {
                'lowPrime': min(priceList),
                'avgPrime': round(sum(priceList) / len(priceList), 2),
                'highPrime': max(priceList)}
            item.data['financial']['current']['listPrice'] = min(priceList)
            item.data['financial']['current'][
                'datetimeStamp'] = datetime.datetime.now().date().__str__()
            item.save()
            print('item_id: ' + kwargs.get('item_id') + ' scraped.')
        else:
            print('Failed to scrape item_id: '+kwargs.get('item_id'))

        return item

    def calcFBAFees(self, **kwargs):
            valueNames = ['qty', 'TTP', 'Weight', 'Length', 'Width', 'Height']
            values = {}
            item = kwargs['ItemData']['amazon'].objects.get(
                item_id=kwargs.get('item_id'))

            if 'listPrice' not in kwargs:
                item.data['financial']['current']['listPrice'] = values[
                    'listPrice'] = item.data[
                        'financial']['current']['primePrices']['lowPrime']
            else:
                item.data['financial']['current']['listPrice'] = values[
                    'listPrice'] = float(kwargs.get('listPrice'))

            if 'itemType' not in kwargs:
                item.data['itemType'] = values['itemType'] = 'game'
            else:
                item.data['itemType'] = values['itemType'] = kwargs.get(
                    'itemType')

            item.save()

            for value in valueNames:
                if value in kwargs:
                    item.data['financial']['current'][value] = kwargs.get(
                        value)
                    values[value] = kwargs.get(value)
                else:
                    try:
                        values[value] = float(item.data['ItemAttributes'][
                            'ItemDimensions'][value]['#text']) / 100
                        item.data[
                            'financial']['current'][value] = values[value]
                        print(str(value) + ' found. Value: ' + str(
                            values[value]))
                    except Exception as e:
                        print(str(e) + ' not found. Using default value of 1.')
                        values[value] = 1.0

            feeSchedules = {
                'game': {
                    'FBAFee': 2.41,
                    'refFee': float(values['listPrice']) * 0.15,
                    'TTP': 2,
                    },
                'console': {
                    'FBAFee': 3.96 + (0.39 * float(item.data[
                        'financial']['current']['Weight'])),
                    'refFee': float(values['listPrice']) * 0.08,
                    'TTP': 10
                    },
                'accessory': {
                    'FBAFee': 2.99,
                    'refFee': float(values['listPrice']) * 0.15,
                    'TTP': 5}, }

            for itemType in feeSchedules.keys():
                if values['itemType'] == itemType:
                    item.data['financial']['current'][
                        'itemType'] = values['itemType']
                    item.data['financial']['current']['varFee'] = 1.80
                    item.data['financial']['current'][
                        'TTP'] = feeSchedules[itemType]['TTP']
                    item.data['financial']['current'][
                        'refFee'] = round(feeSchedules[itemType]['refFee'])
                    item.data['financial']['current'][
                        'FBAFee'] = round(feeSchedules[itemType]['FBAFee'], 2)
                    item.data['financial']['current'][
                        'sellFee'] = round(feeSchedules[itemType][
                            'refFee'] + 1.80, 2)
                    item.data['financial']['current'][
                        'FBAShip'] = round(float(values['Weight']) * 0.35, 2)
                    item.save()
                    item.data['financial']['current'][
                        'net'] = values['net'] = round(float(item.data[
                            'financial']['current']['listPrice'])
                                 - item.data['financial']['current']['FBAFee']
                                 - item.data['financial']['current']['sellFee']
                                 - item.data[
                                    'financial']['current']['FBAShip'], 2)
                    item.data['financial']['current']['laborRate'] = round(
                        values['net'] / (int(values['TTP']) / 60), 2)
                    item.save()

            return item


class BestBuy(Eye):
        def __init__(self):
            self.market = {
                'name': 'bestbuy',
                'BestBuyAPI': 'api_here',
                'categories': ['stuff'],
            }

        def customFunc():
            pass


class Target(Eye):
        def __init__(self):
            self.keys = keys()
            self.APIKey = self.keys.target['APIKey']
            self.TargetAPI = 'target api class...'
            self.categories = ['All']

        def customFunc():
            pass


# instantiate eyes into a dict
def eyeballs():
    return {
        'walmart': Walmart(),
        'ebay': Ebay(),
        'amazon': Amazon(), }
