from typing import List

from .api.get_ex991_from_sec import get_ex991
from .api.get_data_from_filing import get_data_from_filing
from .classes.PartialFiling import PartialFiling


def get_filings_between_dates(start_date: str, end_date: str) -> List[PartialFiling]:
    filings: List[PartialFiling] = get_ex991(start_date, end_date, [])
    final_filings: List[PartialFiling] = get_data_from_filing(filings)

    # remove duplicate companies
    # used_ciks = []
    # unique_filings = []
    # for filing in final_filings:
    #     if filing.cik not in used_ciks:
    #         used_ciks.append(filing.cik)
    #         unique_filings.append(filing)

    # return unique_filings

    return final_filings
