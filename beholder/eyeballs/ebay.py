import isodate
import datetime
import numpy
from ebaysdk.finding import Connection as findingConnection
from ebaysdk.shopping import Connection as shoppingConnection
from .amazon import amazonAPI
from beholder.keys.keys import ebay


class ebayAPI:
    def __init__(self):
        self.ebay = ebay()
        self.usedFilters = [{
            'name': 'Condition',
            'value': ['1000', '1500', '1750', '2000', '3000', '4000', '5000', '6000']
        }]
        self.UPCSalesDataFilters = [
            {'name': 'Condition', 'value': ['1000']},
            {'name': 'AvailableTo', 'value': 'US'},
        ]
        self.findingConnection = findingConnection(
            appid=self.ebay.key['production']['appid'], config_file=None,
        )
        self.shoppingConnection = shoppingConnection(
            appid=self.ebay.key['production']['appid'], config_file=None,
        )
        self.categories = [
            {'name':'All','code':''}, {'name':'Antiques','code':'20081'},
            {'name':'Art','code':'550'}, {'name':'Baby','code':'2984'},
            {'name':'Books','code':'267'}, {'name':'Business & Industrial','code':'12576'},
            {'name':'Camera & Photo','code':'625'}, {'name':'Cell Phones & Accessories','code':'11450'},
            {'name':'Clothing, Shoes & Accessories','code':'11450'},
            {'name':'Coins & Paper Money','code':'11116'}, {'name':'Collectibles','code':'1'},
            {'name':'Computers/Tablets & Networking','code':'58058'},
            {'name':'Consumer Electronics','code':'293'}, {'name':'Crafts','code':'14339'},
            {'name':'Dolls & Bears','code':'237'}, {'name':'DVDs & Movies','code':'11232'},
            {'name':'Entertainment Memorabilia','code':'45100'}, {'name':'Everything Else','code':'99'},
            {'name':'Gift Cards & Coupons','code':'172008'}, {'name':'Health & Beauty','code':'26395'},
            {'name':'Home & Garden','code':'11700'}, {'name':'Jewelry & Watches','code':'281'},
            {'name':'Music','code':'11233'}, {'name':'Musical Instruments & Gear','code':'619'},
            {'name':'Pet Supplies','code':'1281'}, {'name':'Pottery & Glass','code':'870'},
            {'name':'Real Estate','code':'10542'}, {'name':'Specialty Services','code':'316'},
            {'name':'Sporting Goods','code':'888'}, {'name':'Sports Mem, Cards & Fan Shop','code':'64482'},
            {'name':'Stamps','code':'260'}, {'name':'Tickets & Experiences','code':'1305'},
            {'name':'Toys & Hobbies','code':'220'},{'name':'Travel','code':'3252'},
            {'name':'Video Games & Consoles','code':'1249'},
        ]

    def getSalesDataForUPC(self, UPC, **kwargs):  # Todo! function under construction!
        ebayItem = self.findingConnection.execute(
            'findCompletedItems', {
            'productId': UPC,
            'itemFilter': self.UPCSalesDataFilters,
        })
        return ebayItem

    def getSalesData(self, walmartItems, **kwargs):
        soldItems = []
        for item in walmartItems:
            salesData = self.getSalesDataForUPC(item.upc)
            soldItems.append()
            prices = [ item.sale_price for item in soldItems ]
            salesData = {
            'lowPrice': min(prices),
            'meanPrice': mean(prices),
            'stdDev': numpy.std(prices),
            'sampleSize': len(soldItems),
            }
            item = {
                'data': item,
                'salesData': salesData,
            }
        #save item data to database
        return walmartItems

    def search(self, request, **kwargs):
        ebayItems = self.findingConnection.execute(
            'findItemsAdvanced', {
                'keywords': request.GET.get('keywords'),
                'categoryId': request.GET.get('ebayCatId'),
                'descriptionSearch': True,
                'sortOrder': 'EndTimeSoonest',
                'outputSelector': ['GalleryURL', 'ConditionHistogram'],
                'itemFilter': self.itemFilters,
                'paginationInput': {
                    'entriesPerPage': 25,
                    'pageNumber': request.GET.get('page')}
                }
        ).dict()

        if 'errorMessage' in ebayItems:
            print(str(ebayItems['errorMessage']))

        ebayItems['paginationOutput']['pageRange'] = []
        for i in range(int(ebayItems['paginationOutput']['totalPages'])):
            ebayItems['paginationOutput']['pageRange'].append(str(i+1))

        # print(str('FindingResult.paginationOutput.totalPages: ' + str(ebayItems['paginationOutput']['totalPages'])))
        # print(str('FindingResultItem: '+str(ebayItems['searchResult']['item'][0])))

        for i, item in enumerate(ebayItems['searchResult']['item']): #gathering description and shipping costs
            if ebayModel.objects.filter(itemId=item['itemId']).exists():
                _item = ebayModel.objects.get(itemId=item['itemId'])
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

        return ebayItems

    def price(self, request, **kwargs):
        totalSales, totalFBAFees, totalReferralFees = 0, 0, 0
        totalTTP, totalNet, totalWeight = 0, 0, 0
        totalFBAShipping, totalSellFees = 0, 5.0
        amazonItems = []

        if ebayModel.objects.filter(itemId=request.GET.get('itemId')).exists():
            ebayItem = ebayModel.objects.get(itemId=request.GET.get('itemId'))
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

            ebayItem = ebayModel(
                name=_data['name'],
                itemId=_data['ItemID'],
                data=_data,
            ).save()

            # print('New item '+ str(ebayModel.objects.get(itemId=request.GET.get('itemId')).name)+ ' added to the database.')
            ebayItem = ebayModel.objects.get(itemId=request.GET.get('itemId'))

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
                amazon = amazonAPI()
                amazon.scrape(request, amazonModel)
                amazon.fees(request, amazonModel)
                amazonItem = amazonModel.objects.get(ASIN=request.GET.get('ASIN'))

            ebayItem = ebayModel.objects.get(itemId=request.GET.get('itemId'))

            if not request.GET.get('ASIN') in ebayItem.data['ASINInfo'].keys():
                amazonItem.data['selected'] += 1
                ebayItem.data['ASINInfo'][request.GET.get('ASIN')] = {'qty': 1,
                                                              'amazonCatId': request.GET.get('amazonCatId'),
                                                              'title': amazonItem.name}
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

        ebayItem = ebayModel.objects.get(itemId=request.GET.get('itemId'))
        if ebayItem.data['ASINInfo'] != {}:
            for ASIN, info in ebayItem.data['ASINInfo'].items():
                _ = amazonModel.objects.get(ASIN=ASIN)
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
