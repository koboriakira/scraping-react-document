from typing import Optional, Union
from gazpacho import get, Soup
import logging
from autoscraper import AutoScraper
import requests
import json

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger()

ENDPOINT = 'https://reactjs.org'
SAMPLE_PAGE = '/docs/getting-started.html'
WANTED_LIST = [
    'React is a JavaScript library for building user interfaces. Learn what React is all about on our homepage or in the tutorial.']

# CHECK_WORDS_API = 'https://check-word-bre4azfwrq-uc.a.run.app/analyse/'
CHECK_WORDS_API = 'http://localhost:8100/analyse/'

scraper = AutoScraper()


def main():
    urls = get_documents_url()
    logger.info(f'Get {len(urls)} urls.')
    scraper.build(f'{ENDPOINT}{SAMPLE_PAGE}', WANTED_LIST)
    ngsl_words: dict = {}
    not_ngsl_words: dict = {}
    for url in urls:
        logger.info(url)
        result: list[str] = scraper.get_result_similar(
            url, contain_sibling_leaves=True)
        words = get_words(text=" ".join(result))
        ngsl_words |= words[0]
        not_ngsl_words |= words[1]
    logger.info(ngsl_words)
    logger.info(not_ngsl_words)
    with open('./ngsl.json', mode='w') as f:
        json.dump(ngsl_words, f)
    with open('./not_ngsl.json', mode='w') as f:
        json.dump(not_ngsl_words, f)


def get_words(text: str) -> tuple[dict[str, int], dict[str, int]]:
    logger.info('get_words')
    response = requests.post(CHECK_WORDS_API, json={'text': text})
    logger.debug(response.status_code)
    response_json: dict = response.json()
    ngsl_words: dict = {}
    not_ngsl_words: dict = {}
    morphied_word_dict = response_json['morphied_word_dict']
    for ngsl_word in response_json['ngsl_word_list']:
        count = morphied_word_dict[ngsl_word] if ngsl_word in morphied_word_dict else 0
        if ngsl_word in ngsl_words:
            ngsl_words[ngsl_word] = ngsl_words[ngsl_word] + count
        else:
            ngsl_words[ngsl_word] = count
    for not_ngsl_word in response_json['not_ngsl_word_list']:
        count = response_json['morphied_word_dict'][not_ngsl_word]
        if not_ngsl_word in not_ngsl_words:
            not_ngsl_words[not_ngsl_word] = not_ngsl_words[not_ngsl_word] + count
        else:
            not_ngsl_words[not_ngsl_word] = count
    return (ngsl_words, not_ngsl_words)


def get_documents_url() -> list[str]:
    url = f'{ENDPOINT}{SAMPLE_PAGE}'
    soup: Soup = Soup(html=get(url))
    elements: list[Soup] = soup.find(tag='a', attrs={'class': 'css-19pur11'})
    return list(map(lambda e: ENDPOINT + e.attrs['href'], elements))


def get_next_url(soup: Soup) -> Optional[str]:
    try:
        element: Union[Soup, list[Soup]] = soup.find(
            tag='a', attrs={'class': 'css-1k1lek8'})
        logger.debug(element)
        if isinstance(element, Soup):
            return element.attrs['href']
        return element[1].attrs['href']
    except BaseException:
        return None


def cli():
    print("CLI")


if __name__ == '__main__':
    main()
