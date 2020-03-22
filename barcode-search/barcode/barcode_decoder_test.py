from barcode_decoder import decode_barcode, parse_upc
import json

def test_recognition(imageFileName=None):
    with open(imageFileName, mode='rb') as file:
        imageBytes = file.read()
        resp = decode_barcode(imageBytes)
        print(json.dumps(resp))

def test_barcode_re(text=None):
    bcode = parse_upc(text)
    print("barcode {}".format(bcode))
    
test_barcode_re("7 94522 21012 1")
test_barcode_re("7 94522 21O12 1")
test_barcode_re("794522210121")
# test_recognition('/Users/julio/Development/barcode-search/docs/IMG_1384.jpg')
# test_recognition('/Users/julio/Development/barcode-search/docs/IMG_1385.jpg')
test_recognition('/Users/julio/Development/barcode-search/docs/IMG_1386.jpg')