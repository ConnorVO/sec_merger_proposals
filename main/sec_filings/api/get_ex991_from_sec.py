from typing import List
from main.sec_filings.classes.PartialFiling import PartialFiling

from setup import SEC_FULL_TEXT_SEARCH_API


def get_ex991(start_date_string: str, end_date_string: str, unique_filings: List[PartialFiling], page: int = 1) -> List[PartialFiling]:
    '''
    Get all EX 99.1 acquisition filings
    '''

    _unique_filings = unique_filings

    query = {
        "query": '"definitive agreement" merger "exhibit 99.1" -isda',
        "formTypes": ['8-K'],
        "startDate": start_date_string,
        "endDate": end_date_string,
        "page": page
    }

    # for some reason this will sometimes fail with a JSONDecoder error and I think its sec-api problem
    try:
        data = SEC_FULL_TEXT_SEARCH_API.get_filings(query)
    except:
        print('Error with Full Text API')
        return get_ex991(start_date_string, end_date_string, unique_filings, page)

    filings = data['filings']

    for filing in filings:
        is_991 = True

        import pprint
        pprint.PrettyPrinter().pprint(filing)

        if filing['type'] != 'EX-99.1':
            is_991 = False

        partial_filing = PartialFiling(filing['ticker'], filing['accessionNo'], filing['cik'], filing['filingUrl'], filing['filedAt'], filing['companyNameLong'], filing['description'], is_991)

        _unique_filings.append(partial_filing)

        # import pprint
        # pprint.PrettyPrinter().pprint(vars(partial_filing))

    if not filings:
        return _unique_filings

    # each page returns up to 100 filings  ->https://sec-api.io/docs/full-text-search-api/request-parameters
    if len(filings) >= 100:
        return get_ex991(start_date_string, end_date_string, _unique_filings, page=page+1)

    return _unique_filings
