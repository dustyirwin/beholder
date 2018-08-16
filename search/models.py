from django.db import models
from django.contrib.postgres.fields import JSONField


class Query(models.Model):
    user = models.CharField(max_length=128)
    keywords = models.CharField(max_length=1028)
    market_name = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    filters = JSONField(default=dict)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"query on {self.market_names} in {self.categories} for '{self.keywords}'"

class Response(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    resp = JSONField(default=dict)

    def __str__(self):
        return f"response for {self.query}"


# MARKETPLACE QUERY DATA
ebay = {
    'name': 'ebay',
    'search_enabled': False,
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
        {'name': 'Hist', 'value': False}, ], }

walmart = {
    'name': 'walmart',
    'search_enabled': False,
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
        {'name': 'FreeShip', 'value': True}, ], }

amazon = {
    'name': 'amazon',
    'search_enabled': False,
    'categories': [
        {'name': 'Apparel', 'id': 'Apparel'},{'name': 'Appliances', 'id': 'Appliances'},
        {'name': 'ArtsAndCrafts', 'id': 'ArtsAndCrafts'},{'name': 'Automotive', 'id': 'Automotive'},
        {'name': 'Baby', 'id': 'Baby'},{'name': 'Beauty', 'id': 'Beauty'},
        {'name': 'Blended', 'id': 'Blended'},{'name': 'Books', 'id': 'Books'},
        {'name': 'Classical', 'id': 'Classical'},{'name': 'Collectibles', 'id': 'Collectibles'},
        {'name': 'DVD', 'id': 'DVD'},{'name': 'DigitalMusic', 'id': 'DigitalMusic'},
        {'name': 'Electronics', 'id': 'Electronics'},{'name': 'Fashion', 'id': 'Fashion'},
        {'name': 'FashionBaby', 'id': 'FashionBaby'},{'name': 'FashionBoys', 'id': 'FashionBoys'},
        {'name': 'FashionGirls', 'id': 'FashionGirls'},{'name': 'FashionMen', 'id': 'FashionMen'},
        {'name': 'FashionWomen', 'id': 'FashionWomen'},{'name': 'GiftCards', 'id': 'GiftCards'},
        {'name': 'GourmetFood', 'id': 'GourmetFood'},{'name': 'Grocery', 'id': 'Grocery'},
        {'name': 'Handmade', 'id': 'Handmade'},{'name': 'HealthPersonalCare', 'id': 'HealthPersonalCare'},
        {'name': 'HomeAndBusinessServices', 'id': 'HomeAndBusinessServices'},{'name': 'HomeGarden', 'id': 'HomeGarden'},
        {'name': 'Industrial', 'id': 'Industrial'},{'name': 'Jewelry', 'id': 'Jewelry'},
        {'name': 'KindleStore', 'id': 'KindleStore'},{'name': 'Kitchen', 'id': 'Kitchen'},
        {'name': 'LawnAndGarden', 'id': 'LawnAndGarden'},{'name': 'Luggage', 'id': 'Luggage'},
        {'name': 'MP3Downloads', 'id': 'MP3Downloads'},{'name': 'Magazines', 'id': 'Magazines'},
        {'name': 'Marketplace', 'id': 'Marketplace'},{'name': 'Miscellaneous', 'id': 'Miscellaneous'},
        {'name': 'MobileApps', 'id': 'MobileApps'},{'name': 'Movies', 'id': 'Movies'},
        {'name': 'Music', 'id': 'Music'},{'name': 'MusicTracks', 'id': 'MusicTracks'},
        {'name': 'MusicalInstruments', 'id': 'MusicalInstruments'},{'name': 'OfficeProducts', 'id': 'OfficeProducts'},
        {'name': 'OutdoorLiving', 'id': 'OutdoorLiving'},{'name': 'PCHardware', 'id': 'PCHardware'},
        {'name': 'Pantry', 'id': 'Pantry'},{'name': 'PetSupplies', 'id': 'PetSupplies'},
        {'name': 'Photo', 'id': 'Photo'},{'name': 'Shoes', 'id': 'Shoes'},
        {'name': 'Software', 'id': 'Software'},{'name': 'SportingGoods', 'id': 'SportingGoods'},
        {'name': 'Tools', 'id': 'Tools'},{'name': 'Toys', 'id': 'Toys'},
        {'name': 'UnboxVideo', 'id': 'UnboxVideo'},{'name': 'VHS', 'id': 'VHS'},
        {'name': 'Vehicles', 'id': 'Vehicles'},{'name': 'Video', 'id': 'Video'},
        {'name': 'VideoGames', 'id': 'VideoGames'},{'name': 'Watches', 'id': 'Watches'},
        {'name': 'Wine', 'id': 'Wine'},{'name': 'Wireless', 'id': 'Wireless'},
        {'name': 'WirelessAccessories', 'id': 'WirelessAccessories'}, ],
    'search_filters': [
        {'name': 'Prime', 'value': False},
        {'name': 'New', 'value': True}, ], }

chewy = {
    'name': 'chewy',
    'search_enabled': False,
    'search_filters': [],
    'categories': [], }
