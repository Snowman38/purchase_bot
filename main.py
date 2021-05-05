from bs4 import BeautifulSoup
import sys
import time
import asyncio
import requests


sitekey = "6LcwhoEUAAAAAIPQCm9zx-S7Ai9VBfu28bxIFBw5"
client_key = "08fa3a631937eae924d92a1de6ae01cd"


s = requests.session()

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
    'Referer': 'https://www.pokemoncenter-online.com/?p_cd=4521329314112',
    'Accept-Language': 'ja,en;q=0.9,en-GB;q=0.8',
}

# add item to the cart
params = (
    ('method', 'add_cart'),
    ('j', '4521329314112'),
    ('qty', '1'),
)

response = s.get('https://www.pokemoncenter-online.com/?p_cd=4521329314112',
                 headers=headers, params=params)

print(str(response.status_code) + '  add to cart')


while True:
    if response.status_code != 200:  # unsuccess add to the cart .
        s.get('https://www.pokemoncenter-online.com/?p_cd=4521329314112',
              headers=headers, params=params),
        print('retry add-cart process')
    else:
        break


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
print(str(response.status_code) + '  step2->step3')


while True:
    if response.status_code != 200:  # unsuccess to step3 .
        response = s.post('https://www.pokemoncenter-online.com/',
                          headers=headers_step2, params=params_step2, data=data_step2)
        print('retry step 2')
    else:
        break


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
print(str(response.status_code) + '  step3->step4')

while True:
    if response.status_code != 200:  # unsuccess to step 4 .
        response = s.post('https://www.pokemoncenter-online.com/',
                          headers=headers_step3, params=params_step3, data=data_step3)
        print('retry step 3')
    else:
        break

# step4 Final confirmation


# print(response.cookies)
"""


def start_captcha_task(sitekey, client_key):

    data = {
        "clientKey": client_key,
        "task": {
            "type": "NoCaptchaTaskProxyless",
            "websiteURL": "https://www.pokemoncenter-online.com",
            "websiteKey": sitekey
        }
    }

    r = requests.post("https://api.capmonster.cloud/createTask", json=data)

    return r.json()


captcha_id = start_captcha_task(sitekey, client_key)


def get_solved_captcha(task_id, client_key):
    data = {
        "clientKey": client_key,
        "taskId": task_id
    }

    r = requests.post("https://api.capmonster.cloud/getTaskResult", json=data)

    return r.json()


print(get_solved_captcha(captcha_id["taskId"], client_key))
>>>>>> > e4b6d64ec1628e7d8a5d0abb8c68ed505f0fc0a1
