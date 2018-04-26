
"""Class methods for Alibaba marketplace"""


class alibaba:

    def __init__(self):
        self.msg = "New class for Alibaba wholesale marketplace!"

    def search(self, request, AlibabaDB):  # methods for querying products
        query_URL = ''
        # method for producing RESTful GET request for product information.
        self.request = request
        self.AlibabaDB = AlibabaDB

    def price(self, request, AlibabaDB):  # methods for calculating potential profit
        query_URL = ''
        self.request = request
        self.AlibabaDB = AlibabaDB
