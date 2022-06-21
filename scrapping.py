import requests
import bs4
from fake_useragent import UserAgent
from progress.bar import IncrementalBar
import time


def request_html_data(url, urn=None):
    fake_ua = UserAgent()
    headers = {'User-Agent': str(fake_ua.chrome)}
    if urn is None:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url+urn, headers=headers)

    return response.text


def check_keywords(html_code, keywords, url):
    posts = ''
    soup = bs4.BeautifulSoup(html_code, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        text = article.text
        text_list = text.split()
        href = article.find(class_='tm-article-snippet__title-link').attrs['href'][1:]
        link_ = url + href
        for keyword in keywords:
            if keyword in text_list:
                bar.next()
                title = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2')
                title_text = title.find('span').text
                date_cont = article.find(class_='tm-article-snippet__datetime-published')
                date = date_cont.find('time').attrs['title'][0:10]
                posts += f'\n-------\n{date}\n{title_text}\n{link_}'
            else:
                bar.next()
                html_data = request_html_data(url, href)
                post_soup = bs4.BeautifulSoup(html_data, features='html.parser')
                post_text = soup.find(class_='article-formatted-body article-formatted-body '
                                             'article-formatted-body_version-2').text
                if keyword in post_text:
                    title = post_soup.find(class_='tm-article-snippet__title tm-article-snippet__title_h1')
                    title_text = title.find('span').text
                    date = post_soup.find(class_='tm-article-snippet__datetime-published').find('title')[0:10]
                    posts += f'\n-------\n{date}\n{title_text}\n{link_}'

    return posts


if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    URL = 'https://habr.com/ru/all/'
    html_data = request_html_data(URL)
    bar = IncrementalBar('Поиск статей')

    bar.start()
    posts_result = check_keywords(html_data, KEYWORDS, URL)
    bar.finish()
    print('Поиск статей завершён!')
    time.sleep(1)
    print(posts_result)
