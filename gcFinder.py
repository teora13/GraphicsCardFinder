import requests
from bs4 import BeautifulSoup
import time

# get info about your token and chatID from Telegram
def telegram_sendmsg(bot_message):
   bot_token = 'token'
   bot_chatID = 'chatID'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   return requests.get(send_text).json()

def finder():
# add url with filters
    newegg = ('https://www.newegg.ca/p/pl?N=100007708%20601357247%20601357250')
    html_text = requests.get(newegg).text
    soup = BeautifulSoup(html_text, 'html.parser')
# finds div with list of cards
    data = soup.findAll('div',attrs={'class':'list-wrap'})
    urllist = []
# goes through this list to find all links and append them to urllist
    for div in data:
        links = div.findAll('a', attrs={'class': 'item-title'})
        for card in links:
            urllist.append(card['href'])
# finds an availability message in every link
    for url in urllist:
        element_text = requests.get(url).text
        urlsoup = BeautifulSoup(element_text, 'html.parser')
        availability = urlsoup.find('div', attrs={'class': 'product-inventory'})
# sends message to telegram chat if the item in stock
        if availability.text.strip() != 'OUT OF STOCK.':
            telegram_sendmsg(url)
# goes to sleep for 2 mins and runs again
    time.sleep(120)
    finder()
finder()
