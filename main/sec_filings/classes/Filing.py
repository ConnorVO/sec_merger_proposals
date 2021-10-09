from main.intrinio.get_current_price_for_ticker import get_current_price_for_ticker

from .PartialFiling import PartialFiling


class Filing:
    def __init__(self, ticker_a: str, ticker_b: str, proposed_price: float, partial: PartialFiling):
        self.ticker = partial.ticker
        self.accession_number = partial.accession_number
        self.cik = partial.cik
        self.url = partial.cil
        self.filed_at = partial.filed_at
        self.company_name = partial.company_name
        self.description = partial.description
        self.ticker_a = ticker_a
        self.ticker_b = ticker_b
        self.proposed_price = proposed_price
        self.current_price = get_current_price_for_ticker(self.ticker)
