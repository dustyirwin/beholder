from django.shortcuts import render
from .models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs.eyeballs import Eye


def amazon(request):
    return render(request, 'pricing/amazon.html')


def searchAmazon(request):
    amazon = Eye.Amazon()
    amazonItems = amazon.search(request, Amazon)

    # if pricing an eBay item, insert ebayItem into context
    if request.GET.get('itemId'):
        ebayItem = Ebay.objects.get(itemId=request.GET.get('itemId'))
        return render(request, 'pricing/amazon.html', {
                'items': amazonItems,
                'ebayItem': ebayItem})
    else:
        return render(request, 'pricing/amazon.html', {'items': amazonItems})


def ebay(request):
    return render(request, 'pricing/ebay.html')


def searchEbay(request):
    ebay = Eye.Ebay()
    ebayItems = ebay.search(request, Ebay)

    return render(request, 'pricing/ebay.html', ebayItems)


def priceEbayItem(request):
    ebay = Eye.Ebay()
    context = ebay.price(request, Ebay, Amazon)
    return render(request, 'pricing/priceEbayItem.html', context)


def sourceItem(request):
    ebay = Eye.Ebay()
    amazon = Eye.Amazon()
    walmart = Eye.Walmart()
    amazonItem = amazon.scrape(request, Amazon)
    ebayItems = ebay.getUPC(request, )
    walMartItem = walmart.getItemInfo(request)
    context = {
        'amazonItem': amazonItem,
        'walMartItem': walMartItem,
        'ebayItems': ebayItems,
    }
    return render(request, 'pricing/sourceItem.html', context)
