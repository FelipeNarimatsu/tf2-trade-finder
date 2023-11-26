import requests

f = open('test.txt', 'w')

headers_stn = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0', 
            'Cookie': 'browser=1; cf_clearance=Gggq3Ap6dPjjD3k_VKcT2fDo9pUCzD7Sck_wOVOnq70-1700880853-0-1-3064c7fa.4656b0ce.6ed7f5ef-0.2.1700880853; stn_hash=27fe4c2326ee8d55d464b932b9d92d39; trade_tf2_buy_items=Smissmas%202015%20Festive%20Gift; __cflb=0H28vBBkjWkeFGpkqAzJEXRDzPd1g8MfzJq3t4Z3kmT'}

url_stn = 'https://backpack.tf/stats/Unique/Mann%20Co.%20Supply%20Crate%20Series%20%2343/Tradable/Craftable'
r = requests.get(url_stn, headers=headers_stn)

full_html_stn = r.text
f.write(full_html_stn)

print(full_html_stn)