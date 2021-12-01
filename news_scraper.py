import os
import requests
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import cloudscraper
from selenium import webdriver

#Reuters 
r = requests.get("https://www.reuters.com/markets")
soup = BeautifulSoup(r.content, 'lxml')
classes = ['Text__text___3eVx1j Text__white___2ncio9 Text__medium___1ocDap Text__heading_2___sUlNJP Heading__base___1dDlXY Heading__heading_2___3f_bIW Jumbotron__title___GICxhj',
 'Text__text___3eVx1j Text__dark-grey___AS2I_p Text__medium___1ocDap Text__heading_6___m3CqfX Heading__base___1dDlXY Heading__heading_6___1ON736 MediaStoryCard__heading___1K4tAO']

final_headlines = []
final_links= []
# Reuters 
for item in classes:
    news_cards = soup.find_all('span', class_= item)
    for news in news_cards:
        final_headlines.append(news.text.strip() +'.')

classes = ['MediaStoryCard__basic_hero___fSAEnM', 'MediaStoryCard__no_meta___3iQjxw', 'MediaStoryCard__hub___2ECKOi story-card']
for item in classes:
    headlines = soup.find_all('a', class_ = item)
    for link in headlines:
        final_links.append('reuters.com' + str(link['href']))


#CNBC
r = requests.get("https://www.cnbc.com/world/?region=world")
soup = BeautifulSoup(r.content, 'lxml')

finance_news = soup.find_all('a', class_= 'LatestNews-headline')
for fin in finance_news:
        final_headlines.append(fin.text.strip() +'.')
        final_links.append(fin['href'][12:])

#Coindesk
r = requests.get("https://coindesk.com/")
soup = BeautifulSoup(r.content, 'lxml')

crypto_headlines = []
crypto_links = []

crypto_news = soup.find_all('div', class_= 'live-wirestyles__Title-sc-1xrlfqv-3 iNnArA')
for idea in crypto_news:
    crypto_titles= idea.find_all('a', class_= 'Box-sc-1hpkeeg-0 hdfPqS')
    for bar in crypto_titles:
        if bar.text[:11] == 'Market Wrap':
            crypto_headlines.insert(0, bar.text.strip() + '.')
            crypto_links.insert(0, 'coindesk.com' + str(bar['href']))
        else:
            crypto_headlines.append(bar.text.strip() + '.')
            crypto_links.append('coindesk.com' + str(bar['href']))

#Prices and future index
url = 'https://www.coindesk.com/'
delay = 30

os.environ["PATH"] += os.pathsep + r'C:/SeleniumDrivers'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(delay)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
coins = soup.find_all('div', class_ = 'price-navigationstyles__PricingItemWrapper-sc-1okl49q-0')
prices = []
for coin in coins:
    if coin.a['href'] == "/price/bitcoin/" or coin.a['href'] == "/price/ethereum/":
        for element in coin.div:
            prices.append(element.text)


r = requests.get("https://www.marketwatch.com/investing/future/sp%20500%20futures")
soup = BeautifulSoup(r.content, 'lxml')

futures = soup.find_all('div', class_ = 'intraday__data')
for future in futures:
    future_index = future.find('bg-quote', class_ = 'value')
    future_change = future.find('span', class_ = 'change--percent--q')


# url = 'https://messari.io/'
# delay = 30

# os.environ["PATH"] += os.pathsep + r'C:/SeleniumDrivers'
# driver = webdriver.Chrome()
# driver.get(url)
# driver.implicitly_wait(delay)
# html = driver.page_source
# soup = BeautifulSoup(html, 'lxml')
# table = soup.select('table.MuiTable-root')
# for each in table:
#     prices = each.select('div', class_ = 'MuiBox-root')
#     for price in prices:
#         foo = price.find_all('span', class_ = 'jss233')
#         print(foo)

    # for price in prices:
    #     exact = price.select_one('span.MuiTypography-root')
    #     print(exact)





# CoinTelegraph
scraper = cloudscraper.create_scraper()
r = scraper.get('https://cointelegraph.com/')
soup = BeautifulSoup(r.content, 'lxml')

crypto_news = soup.find_all('li', class_= 'posts-listing__item')
for idea in crypto_news:
    news_check= idea.find('span', class_= 'post-card__badge')
    if news_check:
        if news_check.text.strip() == 'News' or news_check.text.strip() == 'Market News' or news_check.text.strip() == 'Breaking news':
            these_links = idea.find_all('a', class_ = 'post-card__title-link')
            these_titles = idea.find_all('span', class_ = 'post-card__title')
            for bar in these_titles:
                if bar.text != '':
                    crypto_headlines.append(bar.text.strip() + '.')
            for link in these_links:
                crypto_links.append('cointelegraph.com' + str(link['href']))

#The Block
r = requests.get("https://www.theblockcrypto.com/")
soup = BeautifulSoup(r.content, 'lxml')

block_links = soup.find_all('a', class_ = 'theme color-outer-space')
for each in block_links:
    crypto_headlines.append(each.text.strip() + '.')
    crypto_links.append('theblockcrypto.com' + str(each['href']))

current_time = datetime.now() + timedelta(minutes=10)

#ApeBoard
url = "https://apeboard.finance/protocols"
delay = 30

os.environ["PATH"] += os.pathsep + r'C:/SeleniumDrivers'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(delay)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

ape_board =  soup.find('h1')
protocol_count = ape_board.text[-4:-1]


with open(f'C:\\Users\\Asus\\Documents\\Treehouse\\news.txt', 'w', encoding='utf-8') as f:
    f.write('Morning News\n')
    f.write(f'{date.today().strftime("%B %d, %Y")}\n')
    f.write(f'Singapore Time: {current_time.strftime("%H:%M")} am\n\n')
    f.write(f'BTC: {prices[0]} ({prices[1]})\n')
    f.write(f'ETH: {prices[2]} ({prices[3]})\n')
    f.write(f'S&P500 Futures: ${future_index.text} ({future_change.text})\n')
    
    f.write('\nTraditional Finance\n')
    for i in range(len(final_headlines)):
        f.write(u'   \u2022')
        f.write(f'   {final_headlines[i]}\n')
        f.write(f'{final_links[i]}\n')

    f.write('\nCrypto\n')
    for i in range(len(crypto_headlines)):
        f.write(u'   \u2022')
        f.write(f'   {crypto_headlines[i]}\n')
        f.write(f'{crypto_links[i]}\n')
    
    f.write('\nDeal Flow\n')
    f.write('\nCompetitor Update\n')    
    competitors = [f'Apeboard (Protocol Count:{protocol_count})(-) https://apeboard.finance/protocols', 'DeBank', 'Step Finance', 'Zerion', 'CrocoFinance', 'Zapper', 'Tin Network', 'Yieldwatch']
    for i in competitors:
        f.write(u'   \u2022')
        f.write('\t' + i + '\n')
        f.write('\t'u'   \u2022')
        f.write('New protocols supported:'+ '\n')
        f.write('\t\t'u'   \u2022'' (())\n' * 3)
