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
    print(r.json())
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
        'payment': 'cvs',
        'cvs': '2'
    }

    # step3 -> step 4
    response = s.post('https://www.pokemoncenter-online.com/',
                      headers=headers_step3, params=params_step3, data=data_step3)

    soup = BeautifulSoup(response.text, 'html.parser')

    with open("step3.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    for cookie in response.cookies:
        s.cookies.set(cookie.name, cookie.value, domain=cookie.domain)

    print(str(response.status_code) + '  step3->step4')
    return response.status_code


def confirmation(v3_captcha):
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
        'ioBlackBox': '0400R9HVeoYv1gsNf94lis1ztl2f0eBwPuTXobqahih8hnVmMV0Uegdggpnwt3khnD2JYn6bo3wR2dDu2MJCSi12NBBoiZbfxP1Whlz5wlRFwWJi0FRulruXQQGCQaJkXU7G9DG/ZYNBQ5CZy8DWHTI6PKYR9FtpPsLf0LVQmADUFBlDgm50c6V/UpKetslI3IixYH1H5YVrp93GJ/KtOFGi8RKePA1UZdKAZDwic+y5/r+SkyAbziDM7k8xAXTS4l7D1erHMnjL6rgoFtmWiT5CtQQoy8fRBma0k8bxHmac52ZUgBbu4NCNc/UJiL5MGqvetG3HqlFCLvW/bzn4/zo2+02BsxVnnQs2zfDowfbw2uVrhMvWeZzwDOZsjHs3PiDdANQor3U91ow85h7zmVcUJNEAtEMdY2g2piIn/4g7jAnC1AevYOBPe8UvRkxkPz1xPGsqpmVl2tnAqvQx/6iBZjoPcOyOxFI2BKLsrHKFK5VCqyTK8LKzctT16TeM5diEHf7WUtiodkQPzf3Q6z+CNnsflDqqr32sdArZwIoMuyjN1/EvKVgGJuwRUFY7xdAiqlr028/3Pq/1J4XWqgJhTMFecIWWXvKVQEdu2XYvr46icoEUIBl9dJXAAYR3cfgvhxJRd5g6SXXqhrnrmN79BNESHGSyQb5EM6m8KZlmvCNExcn0gSd9G/hfflTR5XM9lcABhHdx+C/edkQFDysAsy0AH2WgO40osBx6w1tx0mMZz7HtmSQrKuHt39bvxE86eVaYJEF00M2dmwpFJMf4g4Cmb5UM/4vwDbpnZQL4a0uuVtPyWJ7NheZjVekMYG3JYXyFHBbsmyyzb0vSwWRA+eSMeWgCk0M8kgQVobtOy5kXbeVOAqXsCI9qpLt2ZL85ADPXWwUTnjUH20A9afihHFeovP7W+WpQCv10TaNx+XQgqHxyPWh5ihek/rBXsb8RgJnjRx+vsOoysA/IfO8HBxSm14l9HowIxpdhcydfoD/HpaMZB6qa7he8ghSnRXCYbgbm3tLvHs0o9ETsqFNXePej/eAatMgA+IWxppxSapZauODchk2WrH2LOmVQKLUdYeTcLtcejyCxPk2UkqDvdYEYDfmfBwBYRhc3f5urJ1aotlycMEBL1IzyVekwhI5/tPvXfQEg+KLRVsDNUznM+4IlRQO86SD0OIS7LH591kg7Q92FGKueu33EPopga4/ZM01CDD4rLIv4xPDcpR57NLB95ACgmnUHgChX76n40U18n9NGrU6qnseMYGIoyANRpBH2oITY/3Nu6f8tsMYXiQmV0jazVeFl5sdrzcINkHrBPdBaPIi5ACXz0f07yUmDyuM/37O95k44XxwMXkDk35Y/TtL0elc8rRS5aFgDWT2C+ZC/uhKlHrNbg1PUG+c6Toh1ixUl+hEWF+LPo0WlvBpjnvEcJP4gJuow/Y6swkyDn09MGPGkRbCdsLJ2psgBVSaircwUTU6bnW7Z1lHdnCeZNJ72Jz1Tlkc6bU/8d88s1yhEhfQSW9cHJ8AMQ6Irq0dBLp4BOsE='
    }

    response = requests.post('https://www.pokemoncenter-online.com/?main_page=checkout_process',
                             headers=headers_step4, params=params_step4, data=data_step4)

    soup = BeautifulSoup(response.text, 'html.parser')

    with open("step4.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    print("Confirmed order")
    return response.status_code


get_session()
captcha_id = start_captcha_task(sitekey, client_key)

while True:
    if get_solved_captcha(captcha_id["taskId"], client_key)['status'] == "processing":
        print("Captcha Empty, retrying")
        time.sleep(3)
    else:
        login(username, password, get_solved_captcha(
            captcha_id["taskId"], client_key)['solution']['gRecaptchaResponse'])
        break

addToCart(item_id)
goToStep3()
goToStep4()
captcha_v3_id = start_v3_task(v3_key, v3_source, client_key)["taskId"]

while True:
    if get_v3_response(captcha_v3_id, client_key)['status'] == "processing":
        print("Captcha v3 empty, retrying")
        time.sleep(3)
    else:
        confirmation(get_v3_response(captcha_v3_id, client_key))
        break
