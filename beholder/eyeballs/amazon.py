from django.shortcuts import Http404
from bs4 import BeautifulSoup
from beholder.keys.keys import amazon
import datetime
import bottlenose
import requests
import re
import xmltodict
import json


"""
Beholder API for amazon products.
"""


class amazonAPI:
    def __init__(self):
        self.mws = amazon()
        self.amazon = bottlenose.Amazon(
            self.mws.key['AWS_ACCESS_KEY'],
            self.mws.key['AWS_SECRET_ACCESS_KEY'],
            self.mws.key['AWS_ASSOCIATE_TAG'],
        )

    def search(self, request, amazonModel):
        if 'ASIN' in request.GET:
            amazon = amazonAPI()
            amazon.scrape(request, amazonModel)
            amazon.fees(request, amazonModel)
        resp = self.amazon.ItemSearch(
            Keywords=request.GET.get('keywords'),
            SearchIndex=request.GET.get('amazonCatId'),
            ResponseGroup='Medium,EditorialReview'
        )
        amazonItems = xmltodict.parse(resp)['ItemSearchResponse']['Items']
        amazonItems = json.loads(json.dumps(amazonItems))

        if 'Errors' in amazonItems['Request']:
            raise Http404(amazonItems['Request']['Errors']['Error']['Message'])

        for i, item in enumerate(amazonItems['Item']):

            if amazonModel.objects.filter(ASIN=item['ASIN']).exists():
                amazonItems['Item'][i] = amazonModel.objects.get(ASIN=item['ASIN'])
            else:
                amazonItems['Item'][i]['data'] = item

        return amazonItems['Item']

    def scrape(self, request, amazonModel):
        priceList = []

        primeURL = 'https://www.amazon.com/gp/offer-listing/' + request.GET.get('ASIN') + '/ref=olp_f_primeEligible?ie=UTF8&f_primeEligible=true&f_used=true&f_usedAcceptable=true&f_usedGood=true&f_usedLikeNew=true&f_usedVeryGood=true'
        response = requests.get(primeURL, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content, 'lxml')
        priceColumn = soup.find_all('span', "a-size-large a-color-price olpOfferPrice a-text-bold")
        primeRE = r"\d+.\d+"

        for _ in priceColumn:
            price = re.search(primeRE, str(_))
            priceList.append(float(price.group(0).replace(',', '')))

        if amazonModel.objects.filter(ASIN=request.GET.get('ASIN')).exists():
            amazonItem = amazonModel.objects.get(ASIN=request.GET.get('ASIN'))
        else:
            _data = self.amazon.ItemLookup(
                ItemId=request.GET.get('ASIN'),
                ResponseGroup='Medium, EditorialReview')
            _data = xmltodict.parse(_data)
            _data = json.loads(json.dumps(_data))['ItemLookupResponse']['Items']['Item']
            _data = {**_data, **{
                'name': _data['ItemAttributes']['Title'],
                'keywords': request.GET.get('keywords'),
                'type': '',
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

            amazonItem = amazonModel(
            name=_data['name'],
            data=_data,
            ASIN=request.GET.get('ASIN')
            ).save()

            # assert(amazonModel.objects.filter(ASIN=request.GET.get('ASIN')).exists())
            print('New item ' + str(amazonModel.objects.get(ASIN=request.GET.get('ASIN')).name) + ' added to the database.')

        if len(priceList) > 0:
            amazonItem = amazonModel.objects.get(ASIN=request.GET.get('ASIN'))
            amazonItem.data['financial']['historical'].append(amazonItem.data['financial']['current'])
            amazonItem.data['financial']['current']['primePrices'] = {
                'lowPrime': min(priceList),
                'avgPrime': round(sum(priceList) / len(priceList), 2),
                'highPrime': max(priceList)}
            amazonItem.data['financial']['current']['listPrice'] = min(priceList)
            amazonItem.data['financial']['current']['datetimeStamp'] = datetime.datetime.now().date().__str__()
            amazonItem.save()
            print('ASIN: ' + request.GET.get('ASIN') + ' scraped.')
        else:
            print('Failed to scrape ASIN: '+request.GET.get('ASIN'))

        return amazonItem

    def fees(self, request, amazonModel):
        valueNames = ['qty', 'TTP', 'Weight', 'Length', 'Width', 'Height']
        values = {}
        amazonItem = amazonModel.objects.get(ASIN=request.GET.get('ASIN'))

        if 'listPrice' not in request.GET:
            amazonItem.data['financial']['current']['listPrice'] = values[
                'listPrice'] = amazonItem.data['financial']['current']['primePrices']['lowPrime']
        else:
            amazonItem.data['financial']['current']['listPrice'] = values[
                'listPrice'] = float(request.GET.get('listPrice'))

        if 'itemType' not in request.GET:
            amazonItem.type = values['itemType'] = 'game'
        else:
            amazonItem.type = values['itemType'] = request.GET.get('itemType')

        amazonItem.save()

        for value in valueNames:
            if value in request.GET:
                amazonItem.data['financial']['current'][value] = request.GET.get(value)
                values[value] = request.GET.get(value)
            else:
                try:
                    values[value] = float(amazonItem.data['ItemAttributes']['ItemDimensions'][value]['#text']) / 100
                    amazonItem.data['financial']['current'][value] = values[value]
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
                'FBAFee': 3.96 + (0.39 * float(amazonItem.data['financial']['current']['Weight'])),
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
                amazonItem.data['financial']['current']['itemType'] = values['itemType']
                amazonItem.data['financial']['current']['varFee'] = 1.80
                amazonItem.data['financial']['current']['TTP'] = feeSchedules[itemType]['TTP']
                amazonItem.data['financial']['current']['refFee'] = round(feeSchedules[itemType]['refFee'])
                amazonItem.data['financial']['current']['FBAFee'] = round(feeSchedules[itemType]['FBAFee'], 2)
                amazonItem.data['financial']['current']['sellFee'] = round(feeSchedules[itemType]['refFee'] + 1.80, 2)
                amazonItem.data['financial']['current']['FBAShip'] = round(float(values['Weight']) * 0.35, 2)
                amazonItem.save()
                amazonItem.data['financial']['current']['net'] = values['net'] = round(
                                float(amazonItem.data['financial']['current']['listPrice']) \
                                 - amazonItem.data['financial']['current']['FBAFee'] \
                                 - amazonItem.data['financial']['current']['sellFee'] \
                                 - amazonItem.data['financial']['current']['FBAShip'], 2)
                amazonItem.data['financial']['current']['laborRate'] = round(values['net'] / (int(values['TTP']) / 60), 2)
                amazonItem.save()
                # print("amazonItem.data['financial']: " + str(amazonItem.data['financial']))

        return amazonItem


if __name__ == '__main__':
    amazon = amazonAPI()
    print('amazon = amazonAPI()\nmethods: search(request), scrape(request), fees(request)')
