import boto3
import json
import re

client = boto3.client('rekognition')

# Handle a few permutations of UPC codes
# including with/without spaces and when
# rekognition mistakes O for 0
# 
# 7 9452221012 1
# O 94522 21O121
# 112345678900
upc_re = re.compile(r'([0-9O]\s?[0-9O]{5}\s?[0-9O]{5}\s?[0-9O])')

def decode_barcode(barcodeImageBytes=None):
    if barcodeImageBytes:
        response = client.detect_text(
            Image={
                'Bytes': barcodeImageBytes
            }
        )
        print(json.dumps(response))
        if 'TextDetections' in response:
            for detection in response['TextDetections']:
                textType = detection['Type']
                detectedText = detection['DetectedText']
                if textType == 'LINE': # Don't consider words by themselves
                    parsed = parse_upc(detectedText)
                    if parsed:
                        return parsed
    return None

def parse_upc(text=None):
    match = upc_re.search(text)
    if match and match.group(0):
        # Normalize by removing spaces and replaces O's with 0's
        return match.group(0).replace(" ","").replace("O","0")
    return None
