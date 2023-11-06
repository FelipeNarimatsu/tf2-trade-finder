import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
#from requests_html import AsyncHTMLSessio 
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())

browser.get("https://stntrading.eu/tf2")

#rola a pagina até o final para carregar todo o conteudo

#browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#browser.execute_script("window.scrollTo(0, 1080)") 
SCROLL_PAUSE_TIME = 2
# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

#espera um tempo para carregar o conteudo
time.sleep(2)

#separa o html da pagina
html_source = browser.page_source

browser.close()

soup = BeautifulSoup(html_source, 'html.parser')

array = soup.find_all('span') #cada item usa quatro linhas de span para mostrar no site

#separa a quantia de itens na pagina
quantia_itens_site = len(array)/4

#varaiveis globais
dados = []
dados_acc = []
lista_precos = []
lista_precos_acc = []

#itera a quantia de itens na pagina
acc = 0

for i in range(int(quantia_itens_site)):

    #separa nome do item do html
    nome = str(array[acc]).split('<span class="item-name">',1)[1]
    nome = nome.split('</span>',1)[0]
    #print(nome)       #nome                 
    dados_acc.append(nome)

    #separa preco do item do html
    preco = str(array[acc+2]).split('<span class="item-price">',1)[1]
    preco = preco.split('</span>',1)[0]
    #print(preco)     #preco
    dados_acc.append(preco)

    #separa a quantia do item do html
    quantia = str(array[acc+3]).split('<span class="item-stock in-stock"><b>',1)[1]
    quantia = quantia.split('</b> in Stock</span>',1)[0]
    #print(quantia)     #quantia  
    dados_acc.append(quantia)

    #verifica qual a qualidade do item e insere na linha dos dados que irao para o array "dados"
    if("Strange" in str(array[acc])):
        dados_acc.append("Strange")
    else:
        if("Genuine" in str(array[acc])):
            dados_acc.append("Genuine")
        else:
            if("Vintage" in str(array[acc])):
                dados_acc.append("Vintage")   
            else:
                if("Non-Craftable" in str(array[acc])):
                    dados_acc.append("Non-Craftable")
                else:
                    dados_acc.append("Unique")

    if("Strange Part:" in str(array[acc])):
        dados_acc.pop()
        dados_acc.append("Strange Part")

    #insere os dados num array de armazenamento
    dados.append(dados_acc)

    #limpa o acumulador para proxima iteracao
    dados_acc = []

    #print('\n')
    
    #incrementa variavel para o index das linhas do html
    acc = acc + 4

print(dados)

#iteracao que joga os dados do array de armazenamento no tf2 backpack
for x in range(int(quantia_itens_site)):

    #se for um item unique
    if(dados[x][3] == "Unique"):
        html_pesquisa = "https://backpack.tf/stats/Unique/{}/Tradable/Craftable"
        nome_com_caractere_especial = str(dados[x][0]).replace(" ", "%20")              #troca os espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace(":", "%3A")   #troca : espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("!", "%21")   #troca ! por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("'", "%27")   #troca ' por o caractere especial
        html_pesquisa = html_pesquisa.format(nome_com_caractere_especial)

    #se for um item strange
    if(dados[x][3] == "Strange"):
        html_pesquisa = "https://backpack.tf/stats/Strange/{}/Tradable/Craftable"
        
        nome_com_caractere_especial = str(dados[x][0]).replace("Strange ", "")
        nome_com_caractere_especial = nome_com_caractere_especial.replace(" ", "%20")   #troca os espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace(":", "%3A")   #troca : espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("!", "%21")   #troca ! por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("'", "%27")   #troca ' por o caractere especial
        html_pesquisa = html_pesquisa.format(nome_com_caractere_especial)        

    #se for um item genuine
    if(dados[x][3] == "Genuine"):
        html_pesquisa = "https://backpack.tf/stats/Genuine/{}/Tradable/Craftable"
        
        nome_com_caractere_especial = str(dados[x][0]).replace("Genuine ", "")
        nome_com_caractere_especial = nome_com_caractere_especial.replace(" ", "%20")   #troca os espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace(":", "%3A")   #troca : espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("!", "%21")   #troca ! por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("'", "%27")   #troca ' por o caractere especial
        html_pesquisa = html_pesquisa.format(nome_com_caractere_especial) 

    #se for um item vintage
    if(dados[x][3] == "Vintage"):
        html_pesquisa = "https://backpack.tf/stats/Vintage/{}/Tradable/Craftable"
        
        nome_com_caractere_especial = str(dados[x][0]).replace("Vintage ", "")
        nome_com_caractere_especial = nome_com_caractere_especial.replace(" ", "%20")   #troca os espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace(":", "%3A")   #troca : espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("!", "%21")   #troca ! por o caractere especial]
        nome_com_caractere_especial = nome_com_caractere_especial.replace("'", "%27")   #troca ' por o caractere especial
        html_pesquisa = html_pesquisa.format(nome_com_caractere_especial) 

    #se for um item non-craftable
    if(dados[x][3] == "Non-Craftable"):
        html_pesquisa = "https://backpack.tf/stats/Unique/{}/Tradable/Non-Craftable"

        nome_com_caractere_especial = str(dados[x][0]).replace("Non-Craftable ", "")
        nome_com_caractere_especial = nome_com_caractere_especial.replace(" ", "%20")   #troca os espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace(":", "%3A")   #troca : espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("!", "%21")   #troca ! por o caractere especial]
        nome_com_caractere_especial = nome_com_caractere_especial.replace("'", "%27")   #troca ' por o caractere especial
        html_pesquisa = html_pesquisa.format(nome_com_caractere_especial) 

    #se for um item strange part
    if(dados[x][3] == "Strange Part"):
        html_pesquisa = "https://backpack.tf/stats/Unique/{}/Tradable/Craftable"

        nome_com_caractere_especial = str(dados[x][0])
        nome_com_caractere_especial = nome_com_caractere_especial.replace(" ", "%20")   #troca os espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace(":", "%3A")   #troca : espacos por o caractere especial
        nome_com_caractere_especial = nome_com_caractere_especial.replace("!", "%21")   #troca ! por o caractere especial]
        nome_com_caractere_especial = nome_com_caractere_especial.replace("'", "%27")   #troca ' por o caractere especial
        html_pesquisa = html_pesquisa.format(nome_com_caractere_especial) 


    print(html_pesquisa)
    #inicia a pesquisa do preco no tf2 backpack
    html_pesquisa = requests.get(html_pesquisa)
    html_pesquisa = html_pesquisa.text
    soup_pesquisa = BeautifulSoup(html_pesquisa, 'html.parser')      
    
    #pega todos os divs
    tags = {tag.name for tag in soup.find_all()}
    for tag in tags:
        for i in soup_pesquisa.find_all(tag):
            if(i.has_attr( "data-listing_intent" )):
                if(i["data-listing_intent"] == "buy"):
                    #print(i["data-listing_price"])
                    #lista_precos_acc.append(str(i["data-listing_price"]))
                    preco_pesquisa = str(i["data-listing_price"])
                    break
    lista_precos_acc.append(dados[x][0])
    lista_precos_acc.append(dados[x][1])
    lista_precos_acc.append(preco_pesquisa)
    lista_precos.append(lista_precos_acc)
    
    print(lista_precos_acc)
    lista_precos_acc = []            