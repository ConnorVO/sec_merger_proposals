from ..api.get_991_url import get_991_url


class PartialFiling:
    def __init__(self, ticker: str, accession_number: str, cik: str, url: str, filed_at: str, company_name: str, description: str, is991: bool):
        self.ticker = ticker
        self.accession_number = accession_number
        self.cik = cik
        self.filed_at = filed_at
        self.company_name = company_name
        self.description = description

        if not is991:
            self.url = get_991_url(url)
        else:
            self.url = url
