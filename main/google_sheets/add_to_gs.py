import pygsheets
from typing import List

from ..sec_filings.classes.PartialFiling import PartialFiling


def add_to_gs(filings: List[PartialFiling]):
    gs = pygsheets.authorize(
        service_file='./main/google_sheets/sec-merger-filings-58dd32f36d4c.json')
    sheet = gs.open_by_key(
        '1MxJc8aJtjzoDgo_T_Bsi7LduMw2FYaTPQgo6hIr5nSg').worksheet('title', 'Main')

    sheet_list = []

    for filing in filings:
        filing_list = [filing.filed_at, filing.ticker, filing.cik, filing.url, filing.description]
        sheet_list.append(filing_list)

    sheet.append_table(sheet_list[::-1])
