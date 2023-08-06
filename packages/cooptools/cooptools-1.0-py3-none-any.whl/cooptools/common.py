import math
import uuid
from typing import List, Union, Tuple, Iterable, Callable
import itertools
import datetime
from .typevalidation import date_tryParse

def flattened_list_of_lists(list_of_lists: List[List], unique: bool = False) -> List:
    flat = list(itertools.chain.from_iterable(list_of_lists))

    if unique:
        flat = list(set(flat))

    return flat

def all_indxs_in_lst(lst: List, value) -> List[int]:
    idxs = []
    idx = -1
    while True:
        try:
            idx = lst.index(value, idx + 1)
            idxs.append(idx)
        except ValueError as e:
            break
    return idxs

def next_perfect_square_rt(n: int) -> int:
    int_root_n = int(math.sqrt(n))
    if int_root_n == n:
        return n
    return int_root_n + 1

def last_day_of_month(any_day: datetime.date):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month_first_day = (any_day.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month_first_day - datetime.timedelta(days=1)


def month_range(start_date, end_date) -> List[datetime.date]:
    if end_date < start_date:
        raise ValueError(f"invalid date range {start_date}->{end_date}")



    date1 = date_tryParse(start_date).replace(day=1)
    date2 = last_day_of_month(date_tryParse(end_date))

    months = []
    while date1 < date2:
        month = date1.month
        year = date1.year
        months.append(last_day_of_month(date1))
        next_month = month + 1 if month != 12 else 1
        next_year = year + 1 if next_month == 1 else year
        date1 = date1.replace(month=next_month, year=next_year)

    return months

def try_resolve_guid(id: str) -> Union[str, uuid.UUID]:

    try:
        return uuid.UUID(id)
    except:
        return id

def split_strip(txt: str):
    return [x.strip() for x in txt.split(',')]

def duplicates_in_list(lst: Iterable) -> List:
    res = list(set([ele for ele in lst
                    if list(lst).count(ele) > 1]))
    return res


def verify(verify_func: Callable, msg: str, msg_sub: str):
    if msg_sub is not None:
        msg += f"\n\t{msg_sub}"

    if not verify_func():
        raise ValueError(msg)

def verify_unique(lst: Iterable, error_msg: str = None):
    dups = duplicates_in_list(lst)

    tst = lambda: len(dups) == 0
    msg = f"All the values are not unique. Dups: {dups}"
    verify(tst, msg, error_msg)

def verify_len_match(iterable1, iterable2, error_msg: str = None):
    msg = f"{iterable1} and {iterable2} do not have the same length ({len(iterable1)} vs {len(iterable2)})"

    tst = lambda: len(iterable1) == len(iterable2)
    verify(tst, msg, error_msg)


def verify_len(iterable, length: int, error_msg: str = None):
    msg = f"{iterable} does not have len {length} ({len(iterable)})"

    tst = lambda: len(iterable) == length
    verify(tst, msg, error_msg)

def degree_to_rads(degrees: float) -> float:
    return degrees * math.pi / 180

def rads_to_degrees(rads: float) -> float:
    return rads * 180 / math.pi


if __name__ == "__main__":
    from pprint import pprint

    pprint(month_range('1/1/21', '8/9/22'))