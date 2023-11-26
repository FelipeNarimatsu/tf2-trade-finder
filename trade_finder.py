#Developed by Felipe Narimatsu Presti
#Trade finder program
    #hard coded items name of STN trade database
    #search items data using requests for retrieve STN HTML
    #use requests to retrieve backpack.tf HTML 

import sys, os
import requests

#only key price = 'x keys'
def convert_only_key_price_to_ref(price_string, key_price):
    price_keys = float(price_string.split(' key',1)[0])
    price_ref = price_keys*float(key_price)
    return price_ref

#mixed price = 'x keys, x ref'
def convert_mixed_price_to_ref(price_string, key_price):
    price_ref = price_string.split(', ',1)[1]
    price_ref = float(price_ref.split(' ',1)[0])
    price_keys = float(price_string.split(' key',1)[0])
    price_ref = price_ref + price_keys*float(key_price)
    return price_ref

def switch_item_type(item_name):
    if('Strange Part' in item_name):
        return 'Strange Part'
    if('Strange' in item_name):
        return 'Strange'
    if('Non-Craftable' in item_name):
        return 'Non-Craftable'
    return 'Unique'

def generate_backpack_url(item_name):

    item_type = switch_item_type(item_name)
    
    item_name = item_name.replace(' ', '%20')
    item_name = item_name.replace(':','%3A')
    item_name = item_name.replace('!','%21')
    item_name = item_name.replace("'",'%27')
    item_name = item_name.replace('#','%23')
    if(item_type == 'Non-Craftable'):
        item_name = item_name.replace('Non-Craftable%20', '')
        item_name = "https://backpack.tf/stats/" + 'Unique' + '/' + item_name + "/Tradable/Non-Craftable"

    if(item_type == 'Strange'):
        item_name = item_name.replace('Strange%20', '')
        item_name = "https://backpack.tf/stats/" + 'Strange' + '/' + item_name + "/Tradable/Craftable"

    if(item_type == 'Strange Part'):
        item_name = "https://backpack.tf/stats/Unique/"+ item_name + "/Tradable/Craftable"

    if(item_type == 'Unique'):
        item_name = "https://backpack.tf/stats/" + 'Unique' + '/' + item_name + "/Tradable/Craftable"

    return str(item_name)

def generate_stn_url(item_name):
    item_name = item_name.replace(' ','+')
    item_name = item_name.replace(':','%3A')
    item_name = item_name.replace('!','%21')
    item_name = item_name.replace("'",'%27')
    item_name = item_name.replace('#','%23')
    item_name = "https://stntrading.eu/item/tf2/" + item_name
    return str(item_name)

def main():
    os.remove('urls.txt') 
    headers_stn = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0', 
            'Cookie': 'browser=1; cf_clearance=NpZ2Ch1l4ZKvgjy_jUocQMoJKJ2MDm.6Dq9IEnA9pEw-1700840657-0-1-3064c7fa.4656b0ce.6ed7f5ef-0.2.1700840657; stn_hash=27fe4c2326ee8d55d464b932b9d92d39; browser=1; __cflb=0H28vBBkjWkeFGpkqAzJEXRDzPd1g8Mfybprxb71Bk9'}

    headers_backpack = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0', 
            'Cookie': 'user-id=6i5byn3m71b4cd3hjog8;'}

    f1 = open('items_names.txt', 'r')  
    f2 = open('urls.txt', 'a+')
    item_names_list = f1.readlines()

    #retrieve key infomation backpack.tf HTML
    url_backpack_key = 'https://backpack.tf/stats/Unique/Mann%20Co.%20Supply%20Crate%20Key/Tradable/Craftable'
    k = requests.get(url_backpack_key, headers=headers_backpack)
    html_backpack_key = k.text
    key_price = html_backpack_key.split('<div class="value">',1)[1]
    key_price = key_price.split('â€',1)[0]
    key_price = key_price.replace('\n','')
    key_price = key_price.replace(' ','')

    for line in item_names_list:
        #generate URLs and remove \n from the end
        url_stn = generate_stn_url(line).replace('\n','')
        url_backpack = generate_backpack_url(line).replace('\n','')

        #log all searched urls
        f2.write("STN: " + url_stn + '\t' + "TF2BP: " + url_backpack + '\n')

        #need to remove \n char from the url before request
        #retrieve stn HTML
        r = requests.get(url_stn, headers=headers_stn)
        full_html_stn = r.text
        #retrieve backpack.tf HTML
        b = requests.get(url_backpack, headers=headers_backpack)
        full_html_backpack = b.text

        #remove text before item name and after item name on stn HTML to retrieve sell price
        sell_price_string = full_html_stn.split('Buy it for:</p><p class="mb-0" style="font-size: 18px;"><b>',1)[1]
        sell_price_string = sell_price_string.split('</b></p><p class="text-success"><b>',1)[0]
        
        #remove text before item name and after item name on backpack HTML to retrieve buy price
        if("<span>Latest Forum Threads</span>" not in full_html_backpack):
            try:
                buy_price_string = full_html_backpack.split('<h4>Buy Orders</h4>',1)[1]
                buy_price_string = buy_price_string.split('Suggestions',1)[0]
            except IndexError:
                #create buy_price_string that dont pass on next check
                buy_price_string = 'No listings found.'
                print("Index Error <h4>")
            if('No listings found.' not in buy_price_string):
                buy_price_string = buy_price_string.split('data-listing_price="',1)[1]
                buy_price_string = buy_price_string.split('" data-equipped="',1)[0]
            else:
                buy_price_string = ''
        else:
            buy_price_string = ''

        #filter out of stock items
        if("<b>0</b> in Stock" not in full_html_stn):
            #print(sell_price_string)
            #print(buy_price_string)
            #convert sell price to only ref
            if(sell_price_string != ''):
                if('key' not in sell_price_string):
                    #print('already ref sell')
                    sell_price_ref = float(sell_price_string.split('ref',1)[0])
                    
                elif('keys,' in sell_price_string or 'key,' in sell_price_string):
                    #print('mixed sell')
                    sell_price_ref = convert_mixed_price_to_ref(sell_price_string, key_price)
                    
                else:
                    #print('only key sell')
                    sell_price_ref = convert_only_key_price_to_ref(sell_price_string, key_price)
                    
            else:
                sell_price_ref = 0

            #convert buy price to only ref
            if(buy_price_string != ''):
                if('key' not in buy_price_string):
                    #print('already ref buy')
                    buy_price_ref = float(buy_price_string.split('ref',1)[0])
                    #conversion_type = 'already ref'
                elif('keys,' in buy_price_string or 'key,' in buy_price_string):
                    #print('mixed buy')
                    buy_price_ref = convert_mixed_price_to_ref(buy_price_string, key_price)
                    #conversion_type = 'mixed'
                else:
                    #print('already ref buy')
                    buy_price_ref = convert_only_key_price_to_ref(buy_price_string, key_price)
                    #conversion_type = 'only key'
            else:
                buy_price_ref = 0

            #calculate estimated profit in ref
            if(buy_price_ref > sell_price_ref):
                profit = buy_price_ref - sell_price_ref
            else:
                profit = 0
            

            #print('Item name: ' + line.replace('\n','') + '\t' + 'sell: ' + sell_price_string + '\t' + 'Buy: ' + buy_price_string + '\t' + 'Profit: ' + str(profit) + ' ' + conversion_type)
            print('Profit: ' + str(profit) + ' Item name: ' + line.replace('\n','') + '\t' + 'sell: ' + str(sell_price_ref) + '\t' + 'Buy: ' + str(buy_price_ref) + '\t')


#end main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
