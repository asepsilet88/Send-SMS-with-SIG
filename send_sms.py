# update env_sample with your effective information
# change the file name of env_sample into .env

# install these libs below in advance
import nexmo
import time
import hashlib
import hmac
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
sig_secret = os.getenv("sig_secret")
from_oa = os.getenv("from_oa")
to_da = os.getenv("to_da")
text = 'Test Message'
timestamp = str('%.0f' % time.time())

client = nexmo.Client(key=api_key, signature_secret=sig_secret, 
signature_method='sha256')

message = ( '&api_key=' + api_key + '&from=' + from_oa + '&text=' + text +
'&timestamp=' + timestamp + '&to=' + to_da)
print('message: ' + message)

# the most valuable section, you are welcome
message = bytes(message, 'utf-8')
secret = bytes(sig_secret, 'utf-8')
signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
print('signature: ' + signature)

response = client.send_message({
    'from': from_oa,
    'to': to_da,
    'text': text,
    'timestamp': timestamp,
    'sig': signature
})

response = response['messages'][0]

if response['status'] == '0':
  print('Sent message', response['message-id'])
  print('Remaining balance is', response['remaining-balance'])
else:
  print('Error:', response['error-text'])
