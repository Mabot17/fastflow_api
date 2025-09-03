# ============================================= Start Noted Send Wwhatsapp utils ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. send_whatsapp_api_personal >> kirim pribadi
# 2. send_whatsapp_api_group = kirim gorup internal
# 3. Token ini dari solo.wablas.com >> harus registrasi dahulu
# ============================================= END Noted Send Wwhatsapp utils ===================================
import requests

async def send_whatsapp_api_personal(phone: str, message: str):
    url = "https://solo.wablas.com/api/send-message"
    token = "xdYGXHX3Zt1c1nNnt2RUAwq0KuFR5CWXhYGGqUM24Vwur4HJiiPo3TmyVqRCVbCA"  # token dari wablas (Penyedia jasa api sms dan wa)
    headers = {"Authorization": token}
    data = {"phone": phone, "message": message}

    try:
        response = requests.post(url, headers=headers, data=data)
        print(response.text)
        return response.text
    except Exception as e:
        return str(e)

async def send_whatsapp_api_group(phone: str, message: str):
    url = "https://solo.wablas.com/api/send-message"
    token = "xdYGXHX3Zt1c1nNnt2RUAwq0KuFR5CWXhYGGqUM24Vwur4HJiiPo3TmyVqRCVbCA"  # token dari wablas (Penyedia jasa api sms dan wa)
    headers = {"Authorization": token}
    data = {"phone": phone, "message": message, "isGroup": "true"}

    try:
        response = requests.post(url, headers=headers, data=data)
        return response.text
    except Exception as e:
        return str(e)