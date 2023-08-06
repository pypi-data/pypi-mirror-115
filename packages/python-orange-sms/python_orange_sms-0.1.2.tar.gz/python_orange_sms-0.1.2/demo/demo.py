import utils
SENDER_NAME = 'Name of your app'
AUTH_TOKEN = 'Basic Authorization_Header_From_Console'
message = "The sms message you want to send to the recipient"
recipient_phone_number='243xxxxxxxxx'
dev_phone_number='243xxxxxxxxx'
#recipient_phone_number and dev_phone_number are international phone numbers without + or leading zeros:  format regex('^[1-9][\d]{10,14}$')
sms = utils.SMS(AUTH_TOKEN = AUTH_TOKEN, )
res = sms.send_sms(message=message,
                   dev_phone_number=dev_phone_number,
                   recipient_phone_number=recipient_phone_number)

print(res)

if res.status_code == 201:
    print('EVERYTHING RIGHT : ', res.text)
else:
    print('SAME THING WRONG : ', res.text)
