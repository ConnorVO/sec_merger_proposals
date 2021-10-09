from bs4 import BeautifulSoup
from typing import List

from ..classes.Filing import Filing
from ..classes.PartialFiling import PartialFiling
from setup import SEC_RENDER_API


def _get_soup(url: str) -> BeautifulSoup:
    filing_html = SEC_RENDER_API.get_filing(url)
    soup: BeautifulSoup = BeautifulSoup(filing_html, 'lxml')
    return soup


def _get_all_text(soup: BeautifulSoup) -> str:
    stripped_strings = soup.stripped_strings
    combined_string = ' '.join(stripped_strings)

    return combined_string


def _does_have_two_tickers(all_text: str) -> bool:
    unique_tickers = []
    all_text_list = all_text.lower().split()

    for index, text in enumerate(all_text_list):
        stripped_text = text.strip('()')
        if stripped_text in ['nyse:', 'nasdaq:', 'amex:', 'nasdaq-cm:', 'nasdaq-sm:', 'nasdaq-gm:', 'nasdaqcm', 'nasdaqgm', 'nasdaqsm']:
            ticker = all_text_list[index+1].strip('(),.')
            if ticker not in unique_tickers:
                unique_tickers.append(ticker)

    if len(unique_tickers) >= 2:
        return True

    return False


def get_data_from_filing(filings: List[PartialFiling]) -> List[PartialFiling]:
    final_filings: List[PartialFiling] = []

    for filing in filings:
        soup = _get_soup(filing.url)
        all_text = _get_all_text(soup)
        does_have_two_tickers = _does_have_two_tickers(all_text)

        if not does_have_two_tickers:
            continue

        final_filings.append(filing)

        import pprint
        pprint.PrettyPrinter().pprint(f'{filing.ticker} | {filing.url} |  {does_have_two_tickers}')

    return final_filings
