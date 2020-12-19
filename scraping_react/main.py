from os import scandir
from typing import Optional, Union
from gazpacho import get, Soup
import logging
from autoscraper import AutoScraper

logging.basicConfig(level=logging.DEBUG)
logger: logging.Logger = logging.getLogger()

ENDPOINT = 'https://reactjs.org'
SAMPLE_PAGE = '/docs/getting-started.html'
WANTED_LIST = [
    'React is a JavaScript library for building user interfaces. Learn what React is all about on our homepage or in the tutorial.']


scraper = AutoScraper()


def main():
    urls = get_documents_url()
    logger.info(f'Get {len(urls)} urls.')
    scraper.build(f'{ENDPOINT}{SAMPLE_PAGE}', WANTED_LIST)
    sample_url = urls[10]
    logger.debug(sample_url)
    result: list[str] = scraper.get_result_similar(
        sample_url, contain_sibling_leaves=True)
    logger.debug(result)


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
