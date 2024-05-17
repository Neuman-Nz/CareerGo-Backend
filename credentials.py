import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'F7tjViaANDkuMTjWhVlyzCvGUD2xve2Flx85gWh0lVuluG0x'
    consumer_secret = 'hlaRbD0OzTn4MSgSa0dRwCGDkV9sTOt4MAv234adC6KwBHIAfMHkE8ZyZH6c36AM'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    OffSetValue = '0'
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')



#App.py

# import requests
# from requests.auth import HTTPBasicAuth
# import json
# from credentials import MpesaAccessToken, LipanaMpesaPpassword

# # mpesa stk push 

# class LipaNaMpesa(Resource):
#     def get(self,id):
#         # Check if user is logged in
#         # if 'user_id' not in session:
#         #     return {'error': 'Unauthorized access'}, 401
        
#         access_token = MpesaAccessToken.validated_mpesa_access_token
#         api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#         headers = {"Authorization": "Bearer %s" % access_token}
        
    
#         # Retrieve user details
#         user = User.query.filter_by(id=id).first()
        

#         # Retrieve user's phone number
#         phone_number = user.phone_number
#         # Remove the '+' character
#         cleaned_phone_number = phone_number.replace("+", "")
#         # the below line of code fetched the number from frontend after submisiion of form
#         # phone_number = request.form.get("phone_no")
        
        
#         request_data = {
#             "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
#             "Password": LipanaMpesaPpassword.decode_password,
#             "Timestamp": LipanaMpesaPpassword.lipa_time,
#             "TransactionType": "CustomerPayBillOnline",
#             "Amount": 1000,
#             # use phone_no when fetched 
#             "PartyA":cleaned_phone_number,
#             "PartyB": LipanaMpesaPpassword.Business_short_code,
#             # use phone_no when fetched 
#             "PhoneNumber": cleaned_phone_number,
#             "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
#             "AccountReference": "CareerGo",
#             "TransactionDesc": "Testing stk push"
#         }

#         response = requests.post(api_url, json=request_data, headers=headers)
        
        
#         if response.status_code == 200:
#             return {'message': 'STK push initiated successfully'}, 200
#         else:
#             return {'error': 'Failed to initiate STK push'}, 500


#api.add_resource(LipaNaMpesa, '/users/<int:id>/lipa_na_mpesa')