
"""Class methods for Alibaba marketplace"""



class alibabaAPI:
    def __init__(self):
        self.msg = "New class for Alibaba wholesale marketplace!"
        self.categories = ['stuff']

    def search(self, request, AlibabaDB):  # methods for querying products
        query_URL = "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId="+ request.GET.get("catId") +"&SearchText="+request.get.GET("keywords")
        self.request = request
        self.AlibabaDB = AlibabaDB

    def price(self, request, AlibabaDB):  # methods for calculating potential profit
        query_URL = ''
        self.request = request
        self.AlibabaDB = AlibabaDB
