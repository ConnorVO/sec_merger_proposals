from typing import List

from .api.get_ex991_from_sec import get_ex991
from .api.get_data_from_filing import get_data_from_filing
from .classes.PartialFiling import PartialFiling


def get_filings_between_dates(start_date: str, end_date: str) -> List[PartialFiling]:
    filings: List[PartialFiling] = get_ex991(start_date, end_date, [])
    final_filings: List[PartialFiling] = get_data_from_filing(filings)

    return final_filings
