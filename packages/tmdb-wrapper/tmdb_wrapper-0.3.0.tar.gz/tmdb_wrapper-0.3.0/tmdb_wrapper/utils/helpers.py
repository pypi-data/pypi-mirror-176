import pickle
from datetime import datetime
from .constants import route


def read_pickle() -> dict:
    '''
    load pickle file
    '''
    with open(route, 'rb') as read:
        dct = pickle.load(read)

    return dct, compare_dates(dct['expires_at'])

def save_pickle(data: dict) -> pickle:
    '''
    save pickle file
    '''
    with open(route, 'wb') as write:
        pickle.dump(data, write)


def compare_dates(date_file: str) -> bool:
    '''
    Compare 2 dates, convert them to datetime format and return a boolean.

    date_file : str
        date that belongs to expire session id.
    '''
    date_file_to_date = datetime.strptime(date_file, "%Y-%m-%d %H:%M:%S UTC")
    today_to_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_to_date = datetime.strptime(today_to_str, "%Y-%m-%d %H:%M:%S")
    return date_file_to_date > today_to_date