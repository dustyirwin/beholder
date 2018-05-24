from django.shortcuts import render
from .models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs import amazon, ebay, walmart, alibaba


ebay = ebay.ebayAPI()
amazon = amazon.amazonAPI()
walmart = walmart.walmartAPI()
#alibaba = alibaba.alibabaAPI()

def query(request):
    context = {
    'amazonCategories': amazon.categories,
    }
    return render(request, 'sourcing/query.html', context)


def response(request):
    amazonItems = amazon.search(request, Amazon)
    ebayItems = ebay.search(request, Ebay)
    #walMartItem = walmart.getItemInfo(request)

    context = {
        'amazonItems': amazonItem,
        'walMartItems': walMartItem,
        'ebayItems': ebayItems,
    }
    return render(request, 'sourcing/response.html', context)
