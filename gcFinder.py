import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import gc

def telegram_sendmsg(bot_message):
   bot_token = '1625063646:AAHRJj7eFbwOSSeIjLBozngQ7Z_4PMNGHrc'
   bot_chatID = '289450678'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   return requests.get(send_text).json()

def finder():
    newegg = ('https://www.newegg.ca/p/pl?N=100007708%20601357247%20601357250')
    html_text = requests.get(newegg).text
    soup = BeautifulSoup(html_text, 'html.parser')
    data = soup.findAll('div',attrs={'class':'list-wrap'})
    urllist = []
    for div in data:
        links = div.findAll('a', attrs={'class': 'item-title'})
        for card in links:
            urllist.append(card['href'])
    for url in urllist:
        element_text = requests.get(url).text
        urlsoup = BeautifulSoup(element_text, 'html.parser')
        availability = urlsoup.find('div', attrs={'class': 'product-inventory'})
        if availability.text.strip() != 'OUT OF STOCK.':
            telegram_sendmsg(url)
    # gc.collect()
    # print(datetime.now())
    time.sleep(120)
    finder()
finder()
