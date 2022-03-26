import bs4
import requests
from log_decorator import log_decorator_factory

LOG_FILE = 'log_file.txt'


@log_decorator_factory(LOG_FILE)
def find_keywords(keywords: set, text: str):
    for keyword in keywords:
        if text.find(keyword) != -1:
            return True
    return False


HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Cookie': 'hl=ru; fl=ru; visited_articles=349860',
           'Host': 'habr.com',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'none',
           'Sec-Fetch-User': '?1',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'
}

KEYWORDS = {'Дизайн', 'Фото', 'Web', 'Python'}
response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
response.raise_for_status()

text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')


for article_preview in articles:
    hubs = article_preview.find_all('a', class_='tm-article-snippet__hubs-item-link')
    hubs = set(hub.find('span').text for hub in hubs)
    title = article_preview.find('a', class_='tm-article-snippet__title-link')
    span_title = title.find('span').text
    time = article_preview.find('time')['title']
    href = title['href']
    url = 'https://habr.com' + href

    article_response = requests.get(url, headers=HEADERS)
    article_response.raise_for_status()
    article_text = article_response.text
    article_soup = bs4.BeautifulSoup(article_text, features='html.parser')
    formatted_body = article_soup.text
    if KEYWORDS & hubs or find_keywords(KEYWORDS, formatted_body):
        print(time, span_title, url)






