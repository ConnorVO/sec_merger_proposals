import smtplib, ssl

from typing import List

from main.sec_filings.classes.PartialFiling import PartialFiling
from setup import EMAIL_PASSWORD

def _get_filing_info(filings: List[PartialFiling]) -> List[object]:
    filing_url_obj = {}
    for filing in filings:
        if filing.url not in filing_url_obj:
            filing_url_obj[filing.url] = {
                'url': filing.url,
                'ticker1': filing.ticker,
                'ticker2': ''
            }
        else:
            filing_url_obj[filing.url]['ticker2'] = filing.ticker
    
    return filing_url_obj

def _get_message_string_from_filing_obj(filing_obj) -> str:
    msg_str: str = ''''''

    for key in filing_obj:
        obj = filing_obj[key]
        ticker1 = obj['ticker1']
        ticker2 = obj['ticker2']
        url = obj['url']
        # tickers_str = f'{ticker1} and {ticker2}' if ticker2 else f'{ticker1} and N/A'
        tickers_str = f'{ticker1}'

        msg_str += f'{tickers_str} -> {url}\n'
    
    return msg_str


def send(filings: List[PartialFiling], date_string: str, is_test: bool = False):

    filing_obj = _get_filing_info(filings)
    msg_str = _get_message_string_from_filing_obj(filing_obj)

    port = 465  # For SSL
    password = EMAIL_PASSWORD

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Email participants
    sender_email = "connorv.dev@gmail.com"
    receiver_emails = ["logan.mcdirmit@gmail.com", "connor.vanooyen@gmail.com"] if not is_test else ["connor.vanooyen@gmail.com"]

    # Message
    message = f'To: {",".join(receiver_emails)}\nSubject: Mergers for {date_string}\n\n{msg_str}'

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("connorv.dev@gmail.com", password)
        server.sendmail(sender_email, receiver_emails, message)