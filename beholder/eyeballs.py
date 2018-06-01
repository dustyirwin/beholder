from beholder.keys import keys  # api keys
from amazon.api import AmazonAPI  # amazon api
from wapy.api import Wapy  # walmart api
from ebaysdk.finding import Connection as Finding  # ebay apis
# from ebaysdk.trading import Connection as Trading
# from ebaysdk.shopping import Connection as Shopping
from bs4 import BeautifulSoup
import datetime, isodate, json, requests, re, traceback, isodate


class Eye:
    def __init__(self):
        pass
    def searchCategory(self, ):
        self.items = "massaged response from Eye"
        return self.items

    def getItem(self, itemId):
        self.item = "massaged response from Eye"
        return self.item


class Walmart(Eye):
    def __init__(self):
        self.keys = keys()
        self.WalmartAPI = Wapy(self.keys.walmart['apiKey'])
        try:
            self.taxonomy = requests.get(
                'http://api.walmartlabs.com/v1/taxonomy?apiKey=' + self.keys.walmart['apiKey']
            ).json()

            self.categories = [{'id': category['id'], 'name': category['name']} for category in self.taxonomy['categories']]
            print("Walmart API initialized. Found " + str(len(self.categories)) + " categories.")

        except Exception:
            print("ERROR: "+traceback.format_exc())  # output error to std

    def search(self, **kwargs):
        items = self.WalmartAPI.search(
            kwargs["keywords"],
            categoryId=int(kwargs["category"]),
            ResponseGroup="base",
            page=int(kwargs["page"]),
            sort="bestseller",
            numItems=25,
        )
        return items

    def getBestSellers(self, **kwargs):
        return self.Walmart.bestseller_products(int(kwargs['category']))

    def getClearance(self, **kwargs):
        return self.Walmart.clearance_products(int(kwargs["category"]))

    def getSpecialBuy(self, **kwargs):
        return self.Walmart.clearance_products(int(kwargs["category"]))

    def getTrending(self, **kwargs):
        return self.Walmart.trending_products()


class Ebay(Eye):
    def __init__(self):
        self.keys = keys()
        try:
            self.FindingAPI = Finding(appid=self.keys.ebay['production']['appid'], config_file=None)
            self.taxonomy = ''
            self.categories = [
                {'name': 'Antiques', 'code': '20081'},
                {'name': 'Art', 'code': '550'},
                {'name': 'Baby', 'code': '2984'},
                {'name': 'Books', 'code': '267'},
                {'name': 'Business & Industrial', 'code': '12576'},
                {'name': 'Cell Phones & Accessories', 'code': '15032'},
                {'name': 'Clothing,  Shoes & Accessories', 'code': '11450'},
                {'name': 'Coins & Paper Money', 'code': '11116'},
                {'name': 'Collectibles', 'code': '1'},
                {'name': 'Camera & Photo', 'code': '625'},
                {'name': 'Computers/Tablets & Networking', 'code': '58058'},
                {'name': 'Consumer Electronics', 'code': '293'},
                {'name': 'Crafts', 'code': '14339'},
                {'name': 'Dolls & Bears', 'code': '237'},
                {'name': 'DVDs & Movies', 'code': '11232'},
                {'name': 'Entertainment Memorabilia', 'code': '45100'},
                {'name': 'Everything Else', 'code': '99'},
                {'name': 'Gift Cards & Coupons', 'code': '172008'},
                {'name': 'Health & Beauty', 'code': '26395'},
                {'name': 'Home & Garden', 'code': '11700'},
                {'name': 'Jewelry & Watches', 'code': '281'},
                {'name': 'Music', 'code': '11233'},
                {'name': 'Musical Instruments & Gear', 'code': '619'},
                {'name': 'Pet Supplies', 'code': '1281'},
                {'name': 'Pottery & Glass', 'code': '870'},
                {'name': 'Real Estate', 'code': '10542'},
                {'name': 'Specialty Services', 'code': '316'},
                {'name': 'Sporting Goods', 'code': '888'},
                {'name': 'Sports Mem,  Cards & Fan Shop', 'code': '64482'},
                {'name': 'Stamps', 'code': '260'},
                {'name': 'Tickets & Experiences', 'code': '1305'},
                {'name': 'Toys & Hobbies', 'code': '220'},
                {'name': 'Travel', 'code': '3252'},
                {'name': 'Video Games & Consoles', 'code': '1249'},
            ]
            print("eBay API initialized. Found " + str(len(self.categories)) + " categories.")
        except Exception:
            print("ERROR: "+traceback.format_exc())  # output error to std

    def search(self, **kwargs):
        try:
            items = self.FindingAPI.execute(
                'findItemsAdvanced', {
                    'keywords': kwargs['keywords'],
                    'categoryId': [kwargs['category'], ],
                    'descriptionSearch': True,
                    'sortOrder': 'BestMatch',  # EndTimeSoonest
                    'outputSelector': ['GalleryURL', 'ConditionHistogram'],
                    'itemFilter': [
                        {'name': 'Condition', 'value': 'New'},
                        {'name': 'ListingType', 'value': 'AuctionWithBIN'},
                    ],
                    'paginationInput': {
                        'entriesPerPage': 25,
                        'pageNumber': kwargs["page"]
                        }
                    }
            ).dict()
        except Exception:
            print("ERROR: "+traceback.format_exc())  # output error to std

        if 'errorMessage' in items:
            print(str(items['errorMessage']))
            return {'error': items['errorMessage']}

            '''
            #gathering description and shipping costs
            for i, item in enumerate(ebayItems['searchResult']['item']):
                if kwargs['ebayModel'].objects.filter(itemId=item['itemId']).exists():
                    _item = kwargs['ebayModel'].objects.get(itemId=item['itemId'])
                    ebayItems['searchResult']['item'][i] = _item
                    # print('eBayItem found in db!')
                else:
                    _item = self.shoppingConnection.execute(
                        'GetSingleItem',
                        {'itemID': item['itemId'],
                         'includeSelector': 'TextDescription, ShippingCosts'}
                    ).dict()['Item']
                    _item['TimeLeftStr'] = isodate.parse_duration(_item['TimeLeft']).__str__()
                    ebayItems['searchResult']['item'][i] = {'data':_item}
            '''
            return items

        def price(self, request, **kwargs):

            totalSales = 0
            totalNet = 0
            totalFBAFees = 0,
            totalReferralFees = 0,
            totalTTP = 0,
            totalWeight = 0,
            totalFBAShipping = 0
            totalSellFees = 5.0
            amazonItems = []

            if kwargs['ebayModel'].objects.filter(itemId=request.GET.get('itemId')).exists():
                ebayItem = kwargs['ebayModel'].objects.get(itemId=request.GET.get('itemId'))
            else:
                _data = self.shoppingConnection.execute(
                    'GetSingleItem',
                    {'itemID': request.GET.get('itemId'),
                     'includeSelector': 'TextDescription, ShippingCosts'}
                ).dict()['Item']
                _data = {**_data, **{
                    'name': _data['Title'],
                    'TimeLeftStr': isodate.parse_duration(_data['TimeLeft']).__str__(),
                    'keywords': request.GET.get('keywords'),
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

                # print('New item '+ str(ebayModel.objects.get(itemId=request.GET.get('itemId')).name)+ ' added to the database.')
                ebayItem = kwargs['ebayModel'].objects.get(itemId=request.GET.get('itemId'))

            if 'currentPrice' in request.GET:
                ebayItem.data['ConvertedCurrentPrice']['value'] = request.GET.get('currentPrice')
                ebayItem.save()

            if 'ebayShipping' in request.GET:
                ebayItem.data['ShippingCostSummary']['ShippingServiceCost'] = {'value': float(request.GET.get('ebayShipping'))}
                ebayShipping = float(request.GET.get('ebayShipping'))
                ebayItem.save()
            elif 'ShippingServiceCost' in ebayItem.data['ShippingCostSummary']:
                ebayShipping = float(ebayItem.data['ShippingCostSummary']['ShippingServiceCost']['value'])
            else:
                ebayShipping = 0.0

            if 'ASIN' in request.GET:
                if 'amazonCatId' in request.GET:
                    amazon = amazonEye()
                    amazon.scrape(request, kwargs['amazonModel'])
                    amazon.fees(request, kwargs['amazonModel'])
                    amazonItem = kwargs['amazonModel'].objects.get(ASIN=request.GET.get('ASIN'))

                ebayItem = kwargs['ebayModel'].objects.get(itemId=request.GET.get('itemId'))

                if not request.GET.get('ASIN') in ebayItem.data['ASINInfo'].keys():
                    amazonItem.data['selected'] += 1
                    ebayItem.data['ASINInfo'][request.GET.get('ASIN')] = {
                               'qty': 1,
                               'amazonCatId': request.GET.get('amazonCatId'),
                               'title': amazonItem.name
                               }
                if 'listPrice' in request.GET:
                    amazonItem.data['financial']['current']['listPrice'] = request.GET.get('listPrice')
                else:
                    if amazonItem.data['financial']['current']['listPrice'] == 0.0:
                        amazonItem.data['financial']['current']['listPrice'] = amazonItem.data['financial']['current']['primePrices']['lowPrime']
                if 'FBAFee' in request.GET:
                    amazonItem.data['financial']['current']['FBAFee'] = request.GET.get('FBAFee')
                if 'refFee' in request.GET:
                    amazonItem.data['financial']['current']['refFee'] = request.GET.get('refFee')
                if 'FBAShip' in request.GET:
                    amazonItem.data['financial']['current']['FBAShip'] = request.GET.get('FBAShip')
                if 'Weight' in request.GET:
                    amazonItem.data['financial']['current']['weight'] = float(request.GET.get('Weight'))
                if 'TTP' in request.GET:
                    amazonItem.data['financial']['current']['TTP'] = int(float(request.GET.get('TTP')))
                if 'qty' in request.GET:
                    ebayItem.data['ASINInfo'][request.GET.get('ASIN')]['qty'] = request.GET.get('qty')
                    amazonItem.data['financial']['current']['qty'] = request.GET.get('qty')
                amazonItem.save()
                ebayItem.save()

            ebayItem = kwargs['ebayModel'].objects.get(itemId=request.GET.get('itemId'))
            if ebayItem.data['ASINInfo'] != {}:
                for ASIN, info in ebayItem.data['ASINInfo'].items():
                    _ = kwargs['amazonModel'].objects.get(ASIN=ASIN)
                    totalSales += float(_.data['financial']['current']['listPrice']) * int(info['qty'])
                    totalFBAFees += float(_.data['financial']['current']['FBAFee']) * int(info['qty'])
                    totalReferralFees += float(_.data['financial']['current']['refFee']) * int(info['qty'])
                    totalSellFees += float((_.data['financial']['current']['refFee']) + 1.80) * int(info['qty'])
                    totalTTP += float(_.data['financial']['current']['TTP']) * int(info['qty'])
                    totalFBAShipping += float(_.data['financial']['current']['FBAShip']) * int(info['qty'])
                    totalNet += float(_.data['financial']['current']['net']) * int(info['qty'])
                    totalWeight += float(_.data['financial']['current']['Weight']) * int(info['qty'])
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
                    'profit40': round(totalNet - 5 - ((totalNet - 5) / 1.4 - ebayShipping) - ebayShipping, 2),
                    'maxBid40': round((totalNet - 5) / 1.4 - ebayShipping, 2),
                    'maxBid100LR': round(totalNet - 5 - 100*(totalTTP / 60) - ebayShipping, 2),
                    'laborRate40': round((totalNet -((totalNet - 5) / 1.4 - ebayShipping) - 5 - ebayShipping) / ((totalTTP + 10) / 60), 2),
                }
                ebayItem.save()

            return {'ebayItem': ebayItem, 'amazonItems': amazonItems}


class Amazon(Eye):
    def __init__(self):
        self.keys = keys()
        try:
            self.Amazon = AmazonAPI(
                self.keys.amazon["production"]["AMAZON_ACCESS_KEY"],
                self.keys.amazon["production"]["AMAZON_SECRET_KEY"],
                self.keys.amazon["production"]["AMAZON_ASSOC_TAG"],)
            self.taxonomy = ""
            self.categories = [
                'All', 'Wine', 'Wireless', 'ArtsAndCrafts', 'Miscellaneous',
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
                'Blended', 'HealthPersonalCare', 'Classical'
                ]
            self.categories.sort(key=str.lower)
            print("Amazon API initialized. Found " + str(len(self.categories)) + " categories.")
        except Exception:
            print("ERROR: "+traceback.format_exc())  # output error to std

    def search(self, **kwargs):
        try:
            items = self.Amazon.search(
                Keywords=kwargs['keywords'],
                SearchIndex=kwargs['category'],
                ResponseGroup='Medium, EditorialReview',
                ItemPage=kwargs['page'],
            )
            xmltodict.parse(items)['ItemSearchResponse']['Items']
            items = json.loads(json.dumps(items))

        except Exception:
            print("ERROR: "+traceback.format_exc())  # output error to std

        #  check if item in database
        """
        for item in items:

            if kwargs['ItemData'].data['item_id'] == item["ASIN"]:
                items[item] = kwargs['ItemData']['amazon'].objects.get(
                    item_id=item["item_id"]
                )
            else:
                item[item]['medium_image'] = 'mediumImagePath'
                item[item]['price'] = 'pricePath'
                item[item]['description'] = 'descriptionPath'
                item[item]['upc'] = 'upcPath'
                item[item]['name'] = 'namePath'
                item[item]['rating'] = 'ratingPath'
                item[item]['availability'] = 'availabilityPath'
        """
        return items

    def scrapePrimePrice(self, **kwargs):
        priceList = []

        primeURL = 'https://www.amazon.com/gp/offer-listing/' + kwargs.get("item_id") + '/ref=olp_f_primeEligible?ie=UTF8&f_primeEligible=true&f_used=true&f_usedAcceptable=true&f_usedGood=true&f_usedLikeNew=true&f_usedVeryGood=true'
        response = requests.get(primeURL, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content, 'lxml')
        priceColumn = soup.find_all('span', "a-size-large a-color-price olpOfferPrice a-text-bold")
        primeRE = r"\d+.\d+"

        for _ in priceColumn:
            price = re.search(primeRE, str(_))
            priceList.append(float(price.group(0).replace(',', '')))

        if kwargs['ItemData']['amazon'].objects.filter(item_id=kwargs.get("item_id")).exists():
            item = kwargs['ItemData']['amazon'].objects.get(item_id=kwargs.get("item_id"))
        else:
            _data = self.amazon.ItemLookup(
                ItemId=kwargs.get("item_id"),
                ResponseGroup='Medium, EditorialReview')
            _data = xmltodict.parse(_data)
            _data = json.loads(json.dumps(_data))['ItemLookupResponse']['Items']['Item']
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
                        'datetimeStamp': datetime.datetime.now().replace(microsecond=0).__str__(),
                        }, }
                    }}

            item = kwargs['ItemData']['amazon'](
                name=_data['name'],
                data=_data,
                item_id=kwargs.get("item_id")
            ).save()

            # assert(kwargs['ItemData']['amazon'].objects.filter(item_id=kwargs.get("item_id")).exists())
            print('New item ' + str(kwargs['ItemData']['amazon'].objects.get(item_id=kwargs.get("item_id")).name) + ' added to the database.')

        if len(priceList) > 0:
            item = kwargs['ItemData']['amazon'].objects.get(item_id=kwargs.get("item_id"))
            item.data['financial']['historical'].append(item.data['financial']['current'])
            item.data['financial']['current']['primePrices'] = {
                'lowPrime': min(priceList),
                'avgPrime': round(sum(priceList) / len(priceList), 2),
                'highPrime': max(priceList)}
            item.data['financial']['current']['listPrice'] = min(priceList)
            item.data['financial']['current']['datetimeStamp'] = datetime.datetime.now().date().__str__()
            item.save()
            print('item_id: ' + kwargs.get("item_id") + ' scraped.')
        else:
            print('Failed to scrape item_id: '+kwargs.get("item_id"))

        return item

    def calculateFBAFees(self, **kwargs):
            valueNames = ['qty', 'TTP', 'Weight', 'Length', 'Width', 'Height']
            values = {}
            item = kwargs['ItemData']['amazon'].objects.get(item_id=kwargs.get("item_id"))

            if 'listPrice' not in kwargs:
                item.data['financial']['current']['listPrice'] = values[
                    'listPrice'] = item.data['financial']['current']['primePrices']['lowPrime']
            else:
                item.data['financial']['current']['listPrice'] = values[
                    'listPrice'] = float(kwargs.get('listPrice'))

            if 'itemType' not in kwargs:
                item.data['itemType'] = values['itemType'] = 'game'
            else:
                item.data['itemType'] = values['itemType'] = kwargs.get('itemType')

            item.save()

            for value in valueNames:
                if value in kwargs:
                    item.data['financial']['current'][value] = kwargs.get(value)
                    values[value] = kwargs.get(value)
                else:
                    try:
                        values[value] = float(item.data['ItemAttributes']['ItemDimensions'][value]['#text']) / 100
                        item.data['financial']['current'][value] = values[value]
                        print(str(value) + ' found. Value: ' + str(values[value]))
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
                    'FBAFee': 3.96 + (0.39 * float(item.data['financial']['current']['Weight'])),
                    'refFee': float(values['listPrice']) * 0.08,
                    'TTP': 10
                    },
                'accessory': {
                    'FBAFee': 2.99,
                    'refFee': float(values['listPrice']) * 0.15,
                    'TTP': 5},
                }

            for itemType in feeSchedules.keys():
                if values['itemType'] == itemType:
                    item.data['financial']['current']['itemType'] = values['itemType']
                    item.data['financial']['current']['varFee'] = 1.80
                    item.data['financial']['current']['TTP'] = feeSchedules[itemType]['TTP']
                    item.data['financial']['current']['refFee'] = round(feeSchedules[itemType]['refFee'])
                    item.data['financial']['current']['FBAFee'] = round(feeSchedules[itemType]['FBAFee'], 2)
                    item.data['financial']['current']['sellFee'] = round(feeSchedules[itemType]['refFee'] + 1.80, 2)
                    item.data['financial']['current']['FBAShip'] = round(float(values['Weight']) * 0.35, 2)
                    item.save()
                    item.data['financial']['current']['net'] = values['net'] = round(
                                    float(item.data['financial']['current']['listPrice']) \
                                     - item.data['financial']['current']['FBAFee'] \
                                     - item.data['financial']['current']['sellFee'] \
                                     - item.data['financial']['current']['FBAShip'], 2)
                    item.data['financial']['current']['laborRate'] = round(values['net'] / (int(values['TTP']) / 60), 2)
                    item.save()
                    # print("item.data['financial']: " + str(item.data['financial']))

            return item


class AlibabaEye(Eye):
        def __init__(self):
            self.msg = "New class for Alibaba wholesale marketplace!"
            self.categories = ['stuff']

        def customFunc():
            pass


class TargetEye(Eye):
        def __init__(self):
            self.keys = keys()
            self.APIKey = self.keys.target['APIKey']
            self.TargetAPI = "target api class..."
            self.categories = ['All']

        def customFunc():
            pass


"""
Testing
"""
wally = Walmart()


"""
Scratchpad

Amazon = AmazonAPI(
    keys.amazon["production"]["AMAZON_ACCESS_KEY"],
    keys.amazon["production"]["AMAZON_SECRET_KEY"],
    keys.amazon["production"]["AMAZON_ASSOC_TAG"],)
items = Amazon.search(
    Keywords="batman",
    SearchIndex="VideoGames",
    ResponseGroup='Medium, EditorialReview',
    ItemPage="1", )
"""