from bs4 import BeautifulSoup

from setup import SEC_RENDER_API


def _get_soup(url: str) -> BeautifulSoup:
    filing_html = SEC_RENDER_API.get_filing(url)
    soup: BeautifulSoup = BeautifulSoup(filing_html, 'lxml')
    return soup


def _get_url(soup: BeautifulSoup) -> str:
    links = soup.find_all('a')
    for link in links:
        href = link.get('href') if link.get('href') else None
        if href is None:
            continue
        if 'ex991' in href.lower() or 'ex-991' in href.lower() or 'ex99-1' in href.lower() or 'ex-99-1' in href.lower():
            return href

    print("No ex99-1 links")
    return None


def get_991_url(url_8k: str):
    soup = _get_soup(url_8k)
    url = _get_url(soup)

    if url is None:
        return url_8k

    return url
