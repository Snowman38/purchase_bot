import requests
import time
from bs4 import BeautifulSoup

v3_key = "6LfDcPoUAAAAAM5gneG6VuVeJQLfDpErocIh4fwD"
v3_source = "https://www.pokemoncenter-online.com/?main_page=checkout_confirmation"

sitekey = "6LcwhoEUAAAAAIPQCm9zx-S7Ai9VBfu28bxIFBw5"
client_key = "08fa3a631937eae924d92a1de6ae01cd"

username = "nunu18858@gmail.com"
password = "1278Okamoto"
item_id = "4521329314112"

s = requests.Session()


def get_session():
    headers = {
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Connection': 'keep-alive',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
    }

    response = requests.get(
        'https://www.pokemoncenter-online.com/?main_page=shopping_cart', headers=headers)

    for cookie in response.cookies:
        s.cookies.set(cookie.name, cookie.value, domain=cookie.domain)


def start_captcha_task(sitekey, client_key):

    data = {
        "clientKey": client_key,
        "task": {
            "type": "NoCaptchaTaskProxyless",
            "websiteURL": "https://www.pokemoncenter-online.com",
            "websiteKey": sitekey
        }
    }

    print("Getting Captcha")
    r = requests.post("https://api.capmonster.cloud/createTask", json=data)

    return r.json()


def get_solved_captcha(task_id, client_key):
    data = {
        "clientKey": client_key,
        "taskId": task_id
    }

    r = requests.post("https://api.capmonster.cloud/getTaskResult", json=data)
    return r.json()


def start_v3_task(v3_key, v3_source, client_key):
    data = {
        "clientKey": client_key,
        "task": {
            "type": "RecaptchaV3TaskProxyless",
            "websiteURL": v3_source,
            "websiteKey": v3_key,
            "minScore": 0.7,
        }
    }

    r = requests.post("https://api.capmonster.cloud/createTask", json=data)
    return r.json()


def get_v3_response(task_id, client_key):
    data = {
        "clientKey": client_key,
        "taskId": task_id,
    }

    r = requests.post("https://api.capmonster.cloud/getTaskResult", json=data)
    print("Recieved v3 response")
    return r.json()


def login(username, password, captcha_key):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '^\\^',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.pokemoncenter-online.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.pokemoncenter-online.com/?main_page=login',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
    }

    params = (
        ('main_page', 'login'),
        ('action', 'process'),
    )

    data = {
        'login_address': username,
        'password': password,
        'g-recaptcha-response': captcha_key
    }

    r = s.post('https://www.pokemoncenter-online.com/?main_page=login&action=process',
               headers=headers, params=params, data=data)

    soup = BeautifulSoup(r.text, 'html.parser')
    with open("login.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))
    for cookie in r.cookies:
        s.cookies.set(cookie.name, cookie.value, domain=cookie.domain)

    print(r.cookies)

    return r.status_code


def addToCart(item_id):
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': 'application/json, text/javascript, /; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.pokemoncenter-online.com/?p_cd=' + item_id,
        'Accept-Language': 'ja,en;q=0.9,en-GB;q=0.8',
    }

    # add item to the cart
    params = (
        ('method', 'add_cart'),
        ('j', item_id),
        ('qty', '1'),
    )

    response = s.get('https://www.pokemoncenter-online.com/api/request.php?method=add_cart&j=' + item_id + '&qty=1',
                     headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open("addToCart.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    for cookie in response.cookies:
        s.cookies.set(cookie.name, cookie.value, domain=cookie.domain)

    print(str(response.status_code) + '  add to cart')

    return response.status_code


def goToStep3():
    headers_step2 = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.pokemoncenter-online.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.pokemoncenter-online.com/?main_page=checkout_shipping',
        'Accept-Language': 'ja,en;q=0.9,en-GB;q=0.8',
    }

    params_step2 = (
        ('main_page', 'checkout_shipping'),
    )

    data_step2 = {
        'action': 'process',
        'shipping_date_choice': '1',
        'hope_delivery_date': '',
        'hope_delivery_time_id': '0'
    }

    # step2 to step3
    response = s.post('https://www.pokemoncenter-online.com/',
                      headers=headers_step2, params=params_step2, data=data_step2)

    for cookie in response.cookies:
        s.cookies.set(cookie.name, cookie.value, domain=cookie.domain)

    soup = BeautifulSoup(response.text, 'html.parser')
    with open("step2.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    print(str(response.status_code) + '  step2->step3')
    return response.status_code


# step3 -> step 4
def goToStep4():
    headers_step3 = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.pokemoncenter-online.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.pokemoncenter-online.com/?main_page=checkout_payment',
        'Accept-Language': 'ja,en;q=0.9,en-GB;q=0.8',
    }

    params_step3 = (
        ('main_page', 'checkout_confirmation'),
    )

    data_step3 = {
        'action': 'process',
        'payment': 'cvs',  # selecting convenience store to make the process faster
        # select your payment shop(2=lowson 3=family mart 4=Daily-yamazaki 5= MINI STOP 6=セイコーマート)
        'cvs': '2'
    }

    response = s.post('https://www.pokemoncenter-online.com/',
                      headers=headers_step3, params=params_step3, data=data_step3)

    soup = BeautifulSoup(response.text, 'html.parser')

    with open("step3.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    for cookie in response.cookies:
        s.cookies.set(cookie.name, cookie.value, domain=cookie.domain)

    print(str(response.status_code) + '  step3->step4')
    return response.status_code


def conformation(v3_captcha):
    headers_step4 = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.pokemoncenter-online.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.pokemoncenter-online.com/?main_page=checkout_confirmation',
        'Accept-Language': 'ja',
    }

    params_step4 = (
        ('main_page', 'checkout_process'),
    )

    data_step4 = {
        'cc_token': '',
        'recaptchaResponse': v3_captcha['solution']['gRecaptchaResponse'],
        'agecheck': '1',
    }

    response = s.post('https://www.pokemoncenter-online.com/?main_page=checkout_process',
                      headers=headers_step4, params=params_step4, data=data_step4)

    soup = BeautifulSoup(response.text, 'html.parser')

    with open("step4.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    print("Confirmed order")
    return response.status_code


get_session()  # request to get the cookies
captcha_id = start_captcha_task(sitekey, client_key)  # get captcha on your login form

# login to the website
while True:
    if get_solved_captcha(captcha_id["taskId"], client_key)['status'] == "processing":  # solving captcha
        print("Captcha Empty, retrying")  # retry until sever send you the answer
        time.sleep(3)
    else:
        login(username, password, get_solved_captcha(
            captcha_id["taskId"], client_key)['solution']['gRecaptchaResponse'])  # login to the website
        break

# process of adding item to the cart
while True:
    if addToCart(item_id) != 200:  # if  fail to add-to-cart then try again
        print("fail to adding to the cart, retrying")
        time.sleep(2)
    else:
        break

# process of selecting delivery options
while True:
    if goToStep3() != 200:  # try send the request of the delivery options
        print("fail to send your delivery options, retrying")
        time.sleep(2)
    else:
        break


# process of selecting payment method
while True:
    if goToStep4() != 200:  # try send the request of the payment form
        print("fail to send your payment information, retrying")
        time.sleep(2)
    else:
        break

# getting captcha on the conformation page
captcha_v3_id = start_v3_task(v3_key, v3_source, client_key)["taskId"]

while True:   # try until sever solved the recaptcha
    if get_v3_response(captcha_v3_id, client_key)['status'] == "processing":
        print("Captcha v3 empty, retrying")
        time.sleep(3)
    else:
        break

# Conform your order
while True:
    if conformation(get_v3_response(captcha_v3_id, client_key)) != 200:
        print("sending confirmation failed, retrying")
        time.sleep(1)
    else:
        break
