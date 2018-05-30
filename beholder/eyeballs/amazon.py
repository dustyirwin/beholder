from amazon.api import AmazonAPI
from beholder.keys.keys import keys
from bs4 import BeautifulSoup
import datetime
import requests
import re
import xmltodict
import json
import traceback

"""
Class methods for Amazon MWS Products API
"""


class amazonEye:
    def __init__(self):
        self.keys = keys()
        self.accessKey = self.keys.amazon["production"]["AMAZON_ACCESS_KEY"]
        self.secretKey = self.keys.amazon["production"]["AMAZON_SECRET_KEY"]
        self.assocTag = self.keys.amazon["production"]["AMAZON_ASSOC_TAG"]
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
        self.amazon = AmazonAPI(
            self.accessKey, self.secretKey, self.assocTag
        )

    def search(self, **kwargs):
        try:
            response = self.amazon.ItemSearch(
                Keywords=kwargs['keywords'],
                SearchIndex=kwargs['category'],
                ResponseGroup='Medium, EditorialReview',
                ItemPage=kwargs['page'],
            )
            items = xmltodict.parse(
                response)['ItemSearchResponse']['Items']['Item']
            items = json.loads(json.dumps(items))
        except Exception:
            print(traceback.format_exc())  # output error to std
            return []

        return items

    def save_object(self, MarketData, **kwargs):
        """ #  check if item in database
        for i, item in enumerate(items['Item']):

            if MarketData['amazon'].objects.filter(item_id=item["item_id"]).exists():
                items['Item'][i] = MarketData['amazon'].objects.get(
                    item_id=item["item_id"]
                )
            else:
                items['Item'][i]['data'] = item
        """
        return

    def scrape(self, MarketData, **kwargs):
        priceList = []

        primeURL = 'https://www.amazon.com/gp/offer-listing/' + kwargs.get("item_id") + '/ref=olp_f_primeEligible?ie=UTF8&f_primeEligible=true&f_used=true&f_usedAcceptable=true&f_usedGood=true&f_usedLikeNew=true&f_usedVeryGood=true'
        response = requests.get(primeURL, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content, 'lxml')
        priceColumn = soup.find_all('span', "a-size-large a-color-price olpOfferPrice a-text-bold")
        primeRE = r"\d+.\d+"

        for _ in priceColumn:
            price = re.search(primeRE, str(_))
            priceList.append(float(price.group(0).replace(',', '')))

        if MarketData['amazon'].objects.filter(item_id=kwargs.get("item_id")).exists():
            amazonItem = MarketData['amazon'].objects.get(item_id=kwargs.get("item_id"))
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

            item = MarketData['amazon'](
                name=_data['name'],
                data=_data,
                item_id=kwargs.get("item_id")
            ).save()

            # assert(MarketData['amazon'].objects.filter(item_id=kwargs.get("item_id")).exists())
            print('New item ' + str(MarketData['amazon'].objects.get(item_id=kwargs.get("item_id")).name) + ' added to the database.')

        if len(priceList) > 0:
            item = MarketData['amazon'].objects.get(item_id=kwargs.get("item_id"))
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

    def fees(self, MarketData, **kwargs):
        valueNames = ['qty', 'TTP', 'Weight', 'Length', 'Width', 'Height']
        values = {}
        item = MarketData['amazon'].objects.get(item_id=kwargs.get("item_id"))

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


"""
Scratchpad / Tests

amazon = amazonEye()
batman_products_in_VideoGames = amazon.search(
    keywords="batman",
    category="VideoGames",
    page="1")


batman_products_in_VideoGames.keys()
batman_products_in_VideoGames['Item'][0]['ItemAttributes']['UPC']
batman_products_in_VideoGames['Item'][0]['ItemAttributes']['Feature'][0]
batman_products_in_VideoGames['Item'][0]['MediumImage']['URL']
batman_products_in_VideoGames['Item'][0]['ImageSets']['ImageSet'][0]['LargeImage']['URL']
batman_products_in_VideoGames['Item'][0]['ImageSets']['ImageSet'][1]['LargeImage']['URL']
"""
