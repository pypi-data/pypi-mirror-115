
# PYTHON ORANGE SMS GATE WAY

Orange provides API to send SMS to some countries around the world, but using the API may take you a few hours.


If you are a python developer, don't waste your time. Just use our package and save your time for other meaningful things.


## INSTALL

```sh
pip install python-orange-sms
```

## GET CREDENTIALS

1. Go to https://developer.orange.com/ and login or create a new account

2. Go to **my apps**

3. Select your app or create a new **app**

4. Get your  **Client ID**

5. Get your  **Authorization header**

6. Get your  **App Name**

## USAGE

```py
from python_orange_sms import utils
SENDER_NAME = 'Name of your app' # Name of your app in dev console
AUTH_TOKEN = 'Authorization header' # Authorization header from dev console
message = "The sms message you want to send to the recipient" # Your message
recipient_phone_number='243xxxxxxxxx' # a Receiver phone number
dev_phone_number='243xxxxxxxxx' # Sender (your phone number)
#recipient_phone_number and dev_phone_number are international phone numbers without + or leading zeros:  format regex('^[1-9][\d]{10,14}$')
sms = utils.SMS(AUTH_TOKEN = AUTH_TOKEN, )
res = sms.send_sms(message=message,
              dev_phone_number=dev_phone_number,       recipient_phone_number=recipient_phone_number)

print(res)

if res.status_code == 201:
    print('EVERYTHING RIGHT : ', res.text) # SMS sent
else:
    print('SAME THING WRONG : ', res.text) # OOPS
```
