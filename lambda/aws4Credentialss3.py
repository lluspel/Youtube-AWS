import json

import sys, os, base64, datetime, hashlib, hmac 

access_key = 'ASIA6K3ULTTLMJ4UAI3I'
secret_key = 'PqOk48lov4dzEtJBTud7bEYfAoYUruMkLbRKFaNL'
securityToken= 'FwoGZXIvYXdzEH8aDP9xAt3uAEt8VLEgUSLOAc59uKYcJXTntfu4oXu6dndrw+crvxKrwfLyBHAV76r1XZDvP6GdraQP5Q4DLB2BMX1CrRCAJAN5FauAR9Kon+UOuuPUy5l8J/ODSqJsIPMIs5uPwhB6ivHp7KL33BJAh6yCoZ7iotokyl90Nkl4w2dUTAhSpOW5Rs0B2Y0tIJVnpMOI1BPcHolHuahs/2UawtJMhRwtOoubsdZEB+PcLik9auKFp7Bfo0CRB4SRpg7Y2sHhArBP+G4NTxcYQEUq9VM1hdb9ZiiQZzkf3QsvKOvryvUFMi2fBVX0bunsaCD1dM946r6BFeoeKKJvHJ3stWUGDSu0956AL//y2kPd+gz5DJ4='

bucket = "calculadora12"
bucketUrl = "http://calculadora12.s3.us-east-1.amazonaws.com/"
region = 'us-east-1'
service = 's3'

t = datetime.datetime.utcnow()
amzDate = t.strftime('%Y%m%dT%H%M%SZ')
dateStamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    
policy = """{"expiration": "2020-12-30T12:00:00.000Z",
"conditions": [
{"bucket": \"""" + bucket +"""\"},
["starts-with", "$key", ""],
{"acl": "public-read"},
{"success_action_redirect": \""""+ bucketUrl+"""success.html"},
    {"x-amz-credential": \""""+ access_key+"/"+dateStamp+"/"+region+"""/s3/aws4_request"},
    {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
    {"x-amz-date": \""""+amzDate+"""\" },
    {"x-amz-security-token": \"""" + securityToken +"""\"  }
  ]
}"""

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning




def lambda_handler(event, context):
    # TODO implement
    stringToSign= b""
    stringToSign=base64.b64encode(bytes((policy).encode("utf-8")))

    
    signing_key = getSignatureKey(secret_key, dateStamp, region, service)
    signature = hmac.new(signing_key, stringToSign, hashlib.sha256).hexdigest()
    
    #print(dateStamp)
    #print(signature)
    print(policy)
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({ 'stringSigned' :  signature , 'stringToSign' : stringToSign.decode('utf-8') , 'xAmzCredential' : access_key+"/"+dateStamp+"/"+region+ "/s3/aws4_request" , 'dateStamp' : dateStamp , 'amzDate' : amzDate , 'securityToken' : securityToken })
    }

