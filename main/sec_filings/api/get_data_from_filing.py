from bs4 import BeautifulSoup
from typing import List
import re

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

def _does_pass_phrase_check(all_text: str) -> bool:
    stripped_text = re.sub('\n', ' ', all_text, flags=re.MULTILINE) # all_text.replace("\n", "")

    # previously announced acquisition, previously announced merger, previously announced transaction, loan agreement
    avoid_phrases = [
        'credit agreement', 
        'license agreement', 
        'special purpose acquisition corporation', 
        'special purpose acquisition corporation,', 
        'special-purpose acquisition corporation', 
        'special-purpose acquisition corporation,', 
        'special-purpose acquisition company', 
        'special-purpose acquisition company,', 
        'special purpose acquisition company', 
        'special purpose acquisition company,',
        'completed the closing of the previously announced acquisition',
        'condensed combined balance sheet',
        'completion of its acquisition',
        'blank check company',
        'blank check company,',
        'loan purchase agreement',
        'loan purchase agreement,',
        'successfully completed the merger',
        'completion of their merger',
        'the completion of our merger',
        'acquisition corp.',
        'acquisition corporation',
        'declared a dividend',
        'announced the completion',
        'completed the previously announced merger',
        'closed the acquisition',
        'corporate presentation',
        'audited',
        # 'consolidated statements of operations',
        # 'unaudited financial statements',
        # 'interim financial statements',
        # 'consolidated financial statements',
        # 'condensed balance sheets',
        # 'condensed statements of operations',
        # 'discussion and analysis of financial condition and results of operations',
        'spac ', # must have space so it doesn't match with words like "space"
    ]

    does_contain_avoid_phrase = [ele for ele in avoid_phrases if (ele in stripped_text.lower())]

    if does_contain_avoid_phrase:
        return False
    
    return True


def get_data_from_filing(filings: List[PartialFiling]) -> List[PartialFiling]:
    final_filings: List[PartialFiling] = []

    for filing in filings:
        soup = _get_soup(filing.url)
        all_text = _get_all_text(soup)
        does_have_two_tickers = _does_have_two_tickers(all_text)
        does_pass_phrase_check = _does_pass_phrase_check(all_text)

        import pprint
        pprint.PrettyPrinter().pprint(f'{filing.ticker} | {filing.url} |  {does_have_two_tickers}')

        # DON'T INCLUDE THIS BECAUSE A PRIVATE COMPANY COULD BE BUYING IT
        # if not does_have_two_tickers:
        #     continue

        if not does_pass_phrase_check:
            continue

        final_filings.append(filing)

    return final_filings
