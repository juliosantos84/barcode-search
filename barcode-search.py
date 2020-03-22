import google_custom_search
import json
import re

search = google_custom_search.GoogleCustomSearch()

class BarcodeResult():
    def __init__(self, sourceJson=None):
        """
            {
                "kind": "customsearch#result",
                "title": "UPC 813267020076 Lookup | Barcode Spider",
                "htmlTitle": "UPC <b>813267020076</b> Lookup | Barcode Spider",
                "link": "https://www.barcodespider.com/813267020076",
                "displayLink": "www.barcodespider.com",
                "snippet": "Jun 12, 2019 ... UPC code lookup by number 813267020076 associated with A2 Milk 2% \nReduced Fat Milk, 64 oz.",
                "htmlSnippet": "Jun 12, 2019 <b>...</b> UPC code lookup by number <b>813267020076</b> associated with A2 Milk 2% <br>\nReduced Fat Milk, 64 oz.",
                "cacheId": "7yo3jc-rIBQJ",
                "formattedUrl": "https://www.barcodespider.com/813267020076",
                "htmlFormattedUrl": "https://www.barcodespider.com/<b>813267020076</b>",
                "pagemap": {
                    "cse_thumbnail": [
                        {
                            "src": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzZw1WCLoeWs5tPasLTeTfNhngNHSRbqKng7SP8lBicSA6Gs0eoV1zPI5E",
                            "width": "220",
                            "height": "130"
                        }
                    ],
                    "metatags": [
                        {
                            "viewport": "width=device-width, initial-scale=1"
                        }
                    ],
                    "cse_image": [
                        {
                            "src": "https://images.barcodespider.com/upcbarcode/81326702007.png"
                        }
                    ]
                }
            }
        """
        if sourceJson:
            self._barcode_img_url = sourceJson['pagemap']['cse_thumbnail'][0]['src']
            self._product_description_raw = sourceJson['snippet']
            self._product_description = parse_description(sourceJson['snippet'])

    def __str__(self):
        return "[barcode_image_url: {},product_description: {}]".format(self._barcode_img_url,self._product_description)

def parse_description(raw_product_description=None):
    ANCHOR_TOKEN = "associated with "
    return raw_product_description[str.find(raw_product_description, ANCHOR_TOKEN) + len(ANCHOR_TOKEN):].replace("\n","")

def find(barcode=None):
    results = search.get_results(query=barcode)
    for result in results:
        # print (json.dumps(result))
        br = BarcodeResult(sourceJson=result)
        print(br)


find("813267020076")
