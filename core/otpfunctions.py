from vonage import Vonage, Auth
from vonage_sms import SmsMessage

def send_otp(phone_number, otp):
    auth     = Auth(api_key='fa0d5408', api_secret='VHZOPwnIq8eCVM6I')
    vonage   = Vonage(auth=auth)
    message  = SmsMessage(to=phone_number, from_='Vonage', text=f"Your OTP is: {otp}")
    response =vonage_client.sms.send(message)

    if response["messages"][0]["status"] == "0":
        return True  # OTP sent successfully
    else:
        return False  # OTP failed