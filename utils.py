from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI(
            "5A3079737376386C6E42735864656C624E2F346B76763346696B5862514163664A634651535141396739493D"
        )
        params = {
            "sender": "",  # optional
            "receptor": phone_number,  # multiple mobile number, split by comma
            "message": code,
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
