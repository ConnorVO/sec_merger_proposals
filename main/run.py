import json
from datetime import datetime, timedelta

from .sec_filings import sec_filings
from .google_sheets.add_to_gs import add_to_gs
from .email.email import send


def get_filings_between_dates():
    '''
    python3 -c 'import main.run; main.run.get_filings_between_dates()'
    '''
    # get last ran date
    with open('./main/local_db.json', 'r') as f:
        data = json.load(f)
        prev_start_date_string: str = data['prev_date']

    start_date = datetime.strptime(prev_start_date_string, '%Y-%m-%d') + timedelta(days=1)
    start_date_string = start_date.strftime('%Y-%m-%d')
    print(f'Checking for SEC mergers on {start_date_string}')

    # uncomment these if you want to set the dates
    # start_date_string = '2021-09-01'
    # end_date_string = '2021-10-07'
    # final_filings = sec_filings.get_filings_between_dates(start_date_string, end_date_string)

    final_filings = sec_filings.get_filings_between_dates(start_date_string, start_date_string)
    if final_filings:
        add_to_gs(final_filings)
        send(final_filings, start_date_string)
    else:
        print("No Filings")

    # save updated date to db
    with open('./main/local_db.json', 'w', encoding='utf-8') as f:
        print(f'Writing dates ({start_date_string}) to file')
        json.dump({"prev_date": start_date_string}, f, ensure_ascii=False, indent=4)

def test_email():
    '''
    pipenv run python3 -c 'import main.run; main.run.test_email()'
    '''

    # EMAIL WON'T WORK PROPERLY WITH TWO DATES
    start_date_string = '2021-12-28'
    # end_date_string = '2021-12-0'
    final_filings = sec_filings.get_filings_between_dates(start_date_string, start_date_string)

    if final_filings:
        add_to_gs(final_filings)
        send(final_filings, start_date_string)
    else:
        print("No Filings")
