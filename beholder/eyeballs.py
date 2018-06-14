from beholder.keys import keys  # api keys
from bottlenose import Amazon as AmazonAPI  # amazon api
from wapy.api import Wapy  # walmart api
from ebaysdk.finding import Connection as Finding  # ebay apis
from ebaysdk.shopping import Connection as Shopping
# from ebaysdk.trading import Connection as Trading
from inventory.models import ItemData  # item database
from bs4 import BeautifulSoup
import datetime
import json
import requests
import re
import isodate
import xmltodict
import pprint
# import traceback


'''
BEHOLDER v0.3 written by Dustin Irwin 2018
'''


class Eye:
    global eyeballs
    keys = keys.keys
    ItemData = ItemData

    def search(self, **kwargs):
        for key, value in kwargs.items():
            if 'CatId' in key:
                eyeballs[key[:-5]].getItems(**kwargs)

    def get_item(self, **kwargs):
        if ItemData.objects.filter(item_id=kwargs['item_id']).exists():
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(ItemData.objects.get(item_id=kwargs['item_id']).data)
            return ItemData.objects.get(item_id=kwargs['item_id'])
        else:
            item = eyeballs[kwargs['market']].getItem(**kwargs)
            item['market'] = kwargs['market']
            ItemData(
                name=item['name'],
                item_id=kwargs['item_id'],
                data=item,
            ).save()
            return ItemData.objects.get(item_id=kwargs['item_id'])

    def compare_item(self, **kwargs):
        _item = Eye.get_item(self, **kwargs)
        _item.data['market_prices'] = []

        for name, market in eyeballs.items():
            if name == kwargs['compare']:
                pass
            else:
                items = Eye.search(**kwargs)

                for item in items:

                    _item.data['market_prices'].append({
                        'name': item['name'],
                        'sale_price': item['sale_price'],
                        'item_id': item['item_id'],
                        'market': name,
                        'time_stamp': datetime.datetime.now().__str__()})

        _item.save()

        print('found market prices: ', item.data['market_prices'])


class Walmart(Eye):
    def __init__(self):
        self.WalmartAPI = Wapy(keys.keys['walmart']['apiKey'])
        self.taxonomy = requests.get(
            'http://api.walmartlabs.com/v1/taxonomy?apiKey='
            + keys.keys['walmart']['apiKey']).json()
        self.categories = [
            {'name': category['name'], 'id': category[
                'id']} for category in self.taxonomy['categories']]
        self.paths = {}
        self.market = {
            'name': 'walmart',
            'categories': self.categories,
            'query_options': [
                {'name': 'FreeShippingOnly', 'value': True}, ],
            }
        print('Walmart API initialized. Found ' + str(len(self.categories))
              + ' categories.')

    def getItems(self, **kwargs):
        search_params = {
            'ResponseGroup': 'full',
            'page': 1 if 'walmartPage' not in kwargs else int(kwargs['walmartPage']),
            'sort': 'bestseller',
            'numItems': 25,
            'categoryId' if 'walmartCatId' in kwargs else None: kwargs['walmartCatId'] if 'walmartCatId' in kwargs else None, }
        items = self.WalmartAPI.search(kwargs['keywords'], **search_params)
        print(str(len(items)) + ' items found on Walmart.')
        self.market['items'] = items
        self.market['walmartPage'] = search_params['page']
        self.market['walmartCatId'] = kwargs['walmartCatId']
        return items

    def getItem(self, **kwargs):
        return self.WalmartAPI.product_lookup(kwargs['item_id']).response_handler.payload

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
        self.taxonomy = ''
        self.categories = [
            {'name': 'Antiques', 'id': '20081'},
            {'name': 'Art', 'id': '550'},
            {'name': 'Baby', 'id': '2984'},
            {'name': 'Books', 'id': '267'},
            {'name': 'Business & Industrial', 'id': '12576'},
            {'name': 'Cell Phones & Accessories', 'id': '15032'},
            {'name': 'Clothing,  Shoes & Accessories', 'id': '11450'},
            {'name': 'Coins & Paper Money', 'id': '11116'},
            {'name': 'Collectibles', 'id': '1'},
            {'name': 'Camera & Photo', 'id': '625'},
            {'name': 'Computers/Tablets & Networking', 'id': '58058'},
            {'name': 'Consumer Electronics', 'id': '293'},
            {'name': 'Crafts', 'id': '14339'},
            {'name': 'Dolls & Bears', 'id': '237'},
            {'name': 'DVDs & Movies', 'id': '11232'},
            {'name': 'Entertainment Memorabilia', 'id': '45100'},
            {'name': 'Everything Else', 'id': '99'},
            {'name': 'Gift Cards & Coupons', 'id': '172008'},
            {'name': 'Health & Beauty', 'id': '26395'},
            {'name': 'Home & Garden', 'id': '11700'},
            {'name': 'Jewelry & Watches', 'id': '281'},
            {'name': 'Music', 'id': '11233'},
            {'name': 'Musical Instruments & Gear', 'id': '619'},
            {'name': 'Pet Supplies', 'id': '1281'},
            {'name': 'Pottery & Glass', 'id': '870'},
            {'name': 'Real Estate', 'id': '10542'},
            {'name': 'Specialty Services', 'id': '316'},
            {'name': 'Sporting Goods', 'id': '888'},
            {'name': 'Sports Mem,  Cards & Fan Shop', 'id': '64482'},
            {'name': 'Stamps', 'id': '260'},
            {'name': 'Tickets & Experiences', 'id': '1305'},
            {'name': 'Toys & Hobbies', 'id': '220'},
            {'name': 'Travel', 'id': '3252'},
            {'name': 'Video Games & Consoles', 'id': '1249'}, ]
        self.market = {
            'name': 'ebay',
            'categories': self.categories,
            'query_options': [
                {'name': 'NewOnly', 'value': True},
                {'name': 'BINOnly', 'value': True}, ], }
        print('eBay API initialized. Found ' + str(len(self.categories)) + ' categories.')

    def getItems(self, **kwargs):
        search_params = {
            'keywords' if 'keywords' in kwargs else None: kwargs['keywords'] if 'keywords' in kwargs else None,
            'categoryId' if 'ebayCatId' in kwargs else None: kwargs['ebayCatId'] if 'ebayCatId' in kwargs else None,
            'descriptionSearch': True,
            'sortOrder': 'BestMatch',
            'outputSelector': ['GalleryURL', 'ConditionHistogram', 'PictureURLLarge'],
            'itemFilter': [
                {'name': 'Condition', 'value': ['New']},
                {'name': 'ListingType', 'value': 'AuctionWithBIN'},
                {'name': 'FreeShippingOnly', 'value': True},
                {'name': 'LocatedIn', 'value': 'US'}, ],
            'paginationInput': {
                'entriesPerPage': 25,
                'pageNumber': 1 if 'ebayPage' not in kwargs else int(kwargs['ebayPage']), }}
        items = self.FindingAPI.execute(
            'findItemsAdvanced', search_params).dict()['searchResult']['item']

        for i, item in enumerate(items):
            paths = {
                'item_id': item['itemId'],
                'name': item['title'],
                'time_left': isodate.parse_duration(item['sellingStatus']['timeLeft']).__str__(),
                'sale_price': item['listingInfo']['buyItNowPrice']['value'],
                'product_url': item['viewItemURL'],
                'medium_image': item['galleryURL'],
                'images': [item['pictureURLLarge']],
                'stock': item['sellingStatus']['sellingState'],
                'category_node': item['primaryCategory']['categoryId'],
                'category_path': item['primaryCategory']['categoryName'], }
            items[i] = {**item, **paths}

        self.market['items'] = items

        print(str(len(items)) + ' items found on eBay.', )

    def getItem(self, **kwargs):
        item = self.ShoppingAPI.execute(
            'GetSingleItem', {
                'itemID': kwargs['item_id'],
                'includeSelector': 'TextDescription', }).dict()['Item']
        paths = {
            'name': item['Title'],
            'item_id': item['ItemID'],
            'salePrice': item['ConvertedBuyItNowPrice']['value'],
            'longDescription': item['Description'],
            'images': item['PictureURL'], }
        item = {**item, **paths}

        return item

    def price(self, **kwargs):
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
        self.AmazonAPI = AmazonAPI(
            keys.keys['amazon']['production']['AMAZON_ACCESS_KEY'],
            keys.keys['amazon']['production']['AMAZON_SECRET_KEY'],
            keys.keys['amazon']['production']['AMAZON_ASSOC_TAG'], )
        self.taxonomy = sorted([
            'Wine', 'Wireless', 'ArtsAndCrafts', 'Miscellaneous',
            'Electronics', 'Jewelry', 'MobileApps', 'Photo', 'Shoes',
            'KindleStore', 'Automotive', 'Vehicles', 'Pantry',
            'MusicalInstruments', 'DigitalMusic', 'GiftCards', 'FashionBaby',
            'FashionGirls', 'GourmetFood', 'HomeGarden', 'MusicTracks',
            'UnboxVideo', 'FashionWomen', 'VideoGames', 'FashionMen',
            'Kitchen', 'Video', 'Software', 'Beauty', 'Grocery',
            'FashionBoys', 'Industrial', 'PetSupplies', 'OfficeProducts',
            'Magazines', 'Watches', 'Luggage', 'OutdoorLiving', 'Toys',
            'SportingGoods', 'PCHardware', 'Movies', 'Books', 'Collectibles',
            'Handmade', 'VHS', 'MP3Downloads', 'HomeAndBusinessServices',
            'Fashion', 'Tools', 'Baby', 'Apparel', 'Marketplace', 'DVD',
            'Appliances', 'Music', 'LawnAndGarden', 'WirelessAccessories',
            'Blended', 'HealthPersonalCare', 'Classical'])
        self.categories = [
            {'name': category, 'id': category} for category in self.taxonomy]
        self.market = {
            'name': 'amazon',
            'categories': self.categories,
            'query_options': [
                {'name': 'NewOnly', 'value': False}],
            }
        print('Amazon API initialized. Found ' + str(
            len(self.categories)) + ' categories.')

    def search(self, **kwargs):
        items = self.AmazonAPI.search(
            Keywords=kwargs['keywords'],
            SearchIndex=kwargs['amazonCatId'],
            ResponseGroup='Medium, EditorialReview',
            ItemPage=kwargs['amazonPage'],
        )
        xmltodict.parse(items['ItemSearchResponse']['Items'])
        self.items = json.loads(json.dumps(items))

        #  check if item in database
        '''
        for item in items:

            if kwargs['ItemData'].data['item_id'] == item['ASIN']:
                items[item] = kwargs['ItemData']['amazon'].objects.get(
                    item_id=item['item_id']
                )
            else:
                item[item]['medium_image'] = 'mediumImagePath'
                item[item]['price'] = 'pricePath'
                item[item]['description'] = 'descriptionPath'
                item[item]['upc'] = 'upcPath'
                item[item]['name'] = 'namePath'
                item[item]['rating'] = 'ratingPath'
                item[item]['availability'] = 'availabilityPath'
        '''
        return items

    def scrapePrimePrice(self, **kwargs):
        priceList = []

        primeURL = 'https://www.amazon.com/gp/offer-listing/' + kwargs.get(
            'item_id') + '/ref=olp_f_primeEligible?ie=UTF8&f_primeEligible'
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

        if kwargs['ItemData']['amazon'].objects.filter(
                item_id=kwargs.get('item_id')).exists():
            item = kwargs['ItemData']['amazon'].objects.get(
                item_id=kwargs.get('item_id'))
        else:
            _data = self.amazon.ItemLookup(
                ItemId=kwargs.get('item_id'),
                ResponseGroup='Medium, EditorialReview')
            _data = xmltodict.parse(_data)
            _data = json.loads(json.dumps(_data))[
                'ItemLookupResponse']['Items']['Item']
            _data = {**_data, **{
                'name': _data['ItemAttributes']['Title'],
                'keywords': kwargs.get('keywords'),
                'itemType': '',
                'priced': False,
                'purchased': False,
                'created': datetime.datetime.now().__str__(),
                'lastModified': datetime.datetime.now().__str__(),
                'selected': 0,
                'financial': {
                    'historical': [],
                    'current': {
                        'primePrices': {
                            'lowPrime': 0.0,
                            'avgPrime': 0.0,
                            },
                        'listPrice': 0.0,
                        'FBAFee': 0.0,
                        'refFee': 0.0,
                        'TTP': 2,
                        'qty': 1,
                        'shipping': 1.0,
                        'net': 1.0,
                        'Weight': 1.0,
                        'datetimeStamp': datetime.datetime.now().replace(
                            microsecond=0).__str__(),
                        }, }
                    }}

            item = kwargs['ItemData']['amazon'](
                name=_data['name'],
                data=_data,
                item_id=kwargs.get('item_id')
            ).save()

        if len(priceList) > 0:
            item = kwargs['ItemData']['amazon'].objects.get(
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

    def calculateFBAFees(self, **kwargs):
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
            self.msg = 'New class for Alibaba wholesale marketplace!'
            self.categories = ['stuff']

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


#  instantiate market objects into eyeballs dict
eyeballs = {
    'walmart': Walmart(),
    'ebay': Ebay(),
    # 'amazon': Amazon(),
    # 'bestbuy': BestBuy(),
    # 'target': Target(),
    }
