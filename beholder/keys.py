# beholder API keys


class keys:
    keys = {
        "beholder": {'SECRET_KEY': 'd0nTb3haXxOrZ_&W@hs#r!pt$zBr4H!9!0'
        },
        'beholderdb': {
                'NAME': 'beholder',
                'USER': 'dusty',
                'PASSWORD': 'M@nd!1003',
        },
        'ebay': {
            'production': {
                'appid': 'DustinIr-beholder-PRD-8fb0c962d-d008560e',
                'devid': '77947dc3-ae74-4247-851d-3f4b9955879f',
                'certid': 'PRD-fb0c962d19b8-fcd7-4046-9ff4-f322',
            },
        },
        'amazon': {
            'production': {
                'AMAZON_ACCESS_KEY': 'AKIAIF3NND4VDTTX4T3A',
                'AMAZON_SECRET_KEY': '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',
                'AMAZON_ASSOC_TAG': '7315-1282-4662',
            },
            'sandbox': {
            },
        },
        'walmart': {
            'apiKey': 'c2j7tvmfr8abf42m5u4r5dpb'
        },
        'target': {
            'APIKey': 'blahblahblah'
        },
    }


k = keys()
k.keys['beholder']['SECRET_KEY']
