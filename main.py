import requests


sitekey = "6LcwhoEUAAAAAIPQCm9zx-S7Ai9VBfu28bxIFBw5"
client_key = "08fa3a631937eae924d92a1de6ae01cd"

username = "nunu18858@gmail.com"
password = "1278Okamoto"
item_id = "4521329313641"

s = requests.session()


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


captcha_id = start_captcha_task(sitekey, client_key)


def get_solved_captcha(task_id, client_key):
    data = {
        "clientKey": client_key,
        "taskId": task_id
    }

    r = requests.post("https://api.capmonster.cloud/getTaskResult", json=data)
    ("Recieved Captcha.")
    return r.json()


print(get_solved_captcha(captcha_id["taskId"], client_key))


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

   # print(r.text)
    return r.status_code


# Login flow
while True:
    if login(username, password, get_solved_captcha(captcha_id["taskId"], client_key)) != 200:
        login(username, password, get_solved_captcha(
            captcha_id["taskId"], client_key))
        print("Could not log-in, retrying.")
    else:
        print("Successfully logged in")
        break


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

response = s.get('https://www.pokemoncenter-online.com/?p_cd=' + item_id,
                 headers=headers, params=params)

print(str(response.status_code) + '  add to cart')


while True:
    if response.status_code != 200:  # unsuccess add to cart .
        s.get('https://www.pokemoncenter-online.com/?p_cd=' + item_id,
              headers=headers, params=params),
        print('retry add-cart process')
    else:
       # print(response.text)
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
      #  print(response.text)
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
       # print(response.text)
        break

# step4 Final confirmation

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
    'recaptchaResponse': '03AGdBq27HuOR4sqWpXNp27zHs2RlT40ijYzsXfp-wsoqyujm9lmWCOvSGma-tpOWsg1LeTJD9KRVTljisOAF7bsG2Q17yIKHrL2moerbcL4j9q79Jv98PjVGpr_0NiUeoz70vMhehFRVt5ImsqioXwgSHBEs5YTdkEH5-5Ie5abEo-qSirbQpY5Ay1Tk_I30MBXZQz4JvP86AMvouymf0KsB2nbbsibLtpwWkz_cSNLudjtquZfcGe6tmHZr5sCVfWSka6t3fgHCdQ0Oga9EPAzv7RdocBUXOhMnI6KmC_g9C33QwA6sJkHagxdwCTBRsvAME_C6GzXsLRtnP5_5oqQP5XpXiZKYZNnrz_wUZlLrdazNMk3zxxDnY7zQUXHAxdpWqbO9BkzUdtZMO4mDgFukQC2BfqLJzg2VZ4ECYQ8-UcvkZ00k3YYMWsc1yTOuHCrUWwgTzngezr5AY5gQhOll29bYQXnVWqwQPTw_1iMfF0yMyic8Byu0',
    'agecheck': '1',
    # 'ioBlackBox': '0400R9HVeoYv1gsNf94lis1ztl2f0eBwPuTXobqahih8hnVmMV0Uegdggpnwt3khnD2JYn6bo3wR2dDu2MJCSi12NBBoiZbfxP1Whlz5wlRFwWJi0FRulruXQQGCQaJkXU7G9DG/ZYNBQ5CZy8DWHTI6PKYR9FtpPsLf0LVQmADUFBlDgm50c6V/UpKetslI3IixYH1H5YVrp93GJ/KtOFGi8RKePA1UZdKAZDwic+y5/r+SkyAbziDM7k8xAXTS4l7D1erHMnjL6rgoFtmWiT5CtQQoy8fRBma0k8bxHmac52ZUgBbu4NCNc/UJiL5MGqvetG3HqlFCLvW/bzn4/zo2+02BsxVnnQs2zfDowfbw2uVrhMvWeZzwDOZsjHs3PiDdANQor3U91ow85h7zmVcUJNEAtEMdY2g2piIn/4g7jAnC1AevYOBPe8UvRkxkPz1xPGsqpmVl2tnAqvQx/6iBZjoPcOyOxFI2BKLsrHKFK5VCqyTK8LKzctT16TeM5diEHf7WUtiodkQPzf3Q6z+CNnsflDqqr32sdArZwIoMuyjN1/EvKVgGJuwRUFY7xdAiqlr028/3Pq/1J4XWqgJhTMFecIWWXvKVQEdu2XYvr46icoEUIBl9dJXAAYR3cfgvhxJRd5g6SXXqhrnrmN79BNESHGSyQb5EM6m8KZlmvCNExcn0gSd9G/hfflTR5XM9lcABhHdx+C/edkQFDysAsy0AH2WgO40osBx6w1tx0mMZz7HtmSQrKuHt39bvxE86eVaYJEF00M2dmwpFJMf4g4Cmb5UM/4vwDbpnZQL4a0uuVtPyWJ7NheZjVekMYG3JYXyFHBbsmyyzb0vSwWRA+eSMeWgCk0M8kgQVobtOy5kXbeVOAqXsCI9qpLt2ZL85ADPXWwUTnjUH20A9afihHFeovP7W+WpQCv10TaNx+XQgqHxyPWh5ihek/rBXsb8RgJnjRx+vsOoysA/IfO8HBxSm14l9HowIxpdhcydfoD/HpaMZB6qa7he8ghSnRXCYbgbm3tLvHs0o9ETsqFNXePej/eAatMgA+IWxppxSapZauODchk2WrH2LOmVQKLUdYeTcLtcejyCxPk2UkqDvdYEYDfmfBwBYRhc3f5urJ1aotlycMEBL1IzyVekwhI5/tPvXfQEg+KLRVsDNUznM+4IlRQO86SD0OIS7LH591kg7Q92FGKueu33EPopga4/ZM01CDD4rLIv4xPDcpR57NLB95ACgmnUHgChX76n40U18n9NGrU6qnseMYGIoyANRpBH2oITY/3Nu6f8tsMYXiQmV0jazVeFl5sdrzcINkHrBPdBaPIi5ACXz0f07yUmDyuM/37O95k44XxwMXkDk35Y/TtL0elc8rRS5aFgDWT2C+ZC/uhKlHrNbg1PUG+c6Toh1ixUl+hEWF+LPo0WlvBpjnvEcJP4gJuow/Y6swkyDn09MGPGkRbCdsLJ2psgBVSaircwUTU6bnW7Z1lHdnCeZNJ72Jz1Tlkc6bU/8d88s1yhEhfQSW9cHJ8AMQ6Irq0dBLp4BOsE='
}

response = requests.post('https://www.pokemoncenter-online.com/?main_page=checkout_process',
                         headers=headers_step4, params=params_step4, data=data_step4)

if response.status_code == 200:  # unsuccess to step 4 .
    print('successfully purchase')

# print(response.cookies)
