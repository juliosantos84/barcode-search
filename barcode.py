import boto3
import json
import re

client = boto3.client('rekognition')

# 7 94522 21012 1
upc_re = re.compile(r'([0-9O]\s?[0-9O]{5}\s?[0-9O]{5}\s?[0-9O])')

def get_upc_code(imageBytes=None):
    if imageBytes:
        response = client.detect_text(
            Image={
                'Bytes': imageBytes
            }
        )
        # print (json.dumps(response))
        if 'TextDetections' in response:
            for detection in response['TextDetections']:
                textType = detection['Type']
                detectedText = detection['DetectedText']
                if textType == 'LINE': # Don't consider words by themselves
                    parsed = parse_barcode(detectedText)
                    if parsed:
                        return parsed
    return None

def parse_barcode(text=None):
    match = upc_re.search(text)
    if match and match.group(0):
        return match.group(0).replace(" ","")

def test_recognition(imageFileName=None):
    with open(imageFileName, mode='rb') as file:
        imageBytes = file.read()
        resp = get_upc_code(imageBytes)
        print(json.dumps(resp))

def test_barcode_re(text=None):
    bcode = parse_barcode(text)

# test_barcode_re("7 94522 21012 1")
test_recognition('/Users/julio/Development/barcode-search/IMG_1384.jpg')
test_recognition('/Users/julio/Development/barcode-search/IMG_1385.jpg')
test_recognition('/Users/julio/Development/barcode-search/IMG_1386.jpg')
