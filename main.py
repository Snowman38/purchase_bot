import requests
import time

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

params = (
    ('method', 'add_cart'),
    ('j', '4521329314112'),
    ('qty', '1'),
)

response = s.get('https://www.pokemoncenter-online.com/?p_cd=4521329314112',
                 headers=headers, params=params)

while true:
    if response.status != 200:
        s.get('https://www.pokemoncenter-online.com/?p_cd=4521329314112',
              headers=headers, params=params)
    else:

print(response.cookies)
