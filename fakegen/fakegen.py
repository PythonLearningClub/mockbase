from csv import QUOTE_NONNUMERIC, writer
from datetime import datetime, timedelta
from random import sample, randint, triangular
from os import makedirs, path
from typing import List
from sys import argv
import logging


# Generate number of merchants between n and m + C (c << n)
# Enumerate merchants, remove C random merchants
# Generate number of filters for each merchant, use weighted list
# Split filters between order and shipping
# Enumerate filters: merchant_id*100+1(2 for shipping)+i(1..filter_count)
# Dates —2 years back from now on ~ 700 days
# For each day: for each filter: generate:
# total messages = successful + problematic (<15%; mtm + nbo + non_usd); orders (<= total)
# write to two files: date+merchant+filter+total+successful+problematics; date+merchant+filter+orders

def split(count: int, parts: int, primary_skew: float = 0):
    """
    Splits number into specified amount of parts
    Too slow
    :param count: number to split
    :param parts: number of parts to split to
    :param primary_skew: mean of triangular distribution (0..1)
    :return: list of parts
    """
    if not primary_skew:
        primary_skew = 0.5
    res = []
    primary = int(triangular(1, count, count*primary_skew))
    if parts == 2:
        return [primary, count-primary]
    res.append(primary)
    res.extend(split(count-primary, parts-1))
    return res


def write_batch(file: str, folder: str, lines: List) -> None:
    """
    Writes batch of lines as csv
    :param file: filename
    :param folder: folder to keep file in (must exist)
    :param lines: lines to write
    :return: None
    """
    with open(path.join(folder, file), 'a') as bfh:
        w = writer(bfh, quoting=QUOTE_NONNUMERIC)
        w.writerows(lines)


# Generating merchants list
if len(argv) > 1 and argv[1].lower() == 'debug':
    logging.basicConfig(level=logging.DEBUG)
    DEBUG_MLT = 10
    MERCHANT_MIN = 16*DEBUG_MLT
    MERCHANT_MAX = 20*DEBUG_MLT
    MERCHANT_SKIP_MIN = 2*DEBUG_MLT
    MERCHANT_SKIP_MAX = 6*DEBUG_MLT
    DATERANGE = 500
else:
    logging.basicConfig(level=logging.INFO)
    MERCHANT_MIN = 1600
    MERCHANT_MAX = 2000
    MERCHANT_SKIP_MIN = 20
    MERCHANT_SKIP_MAX = 60
    DATERANGE = 365*2
merchants_count = randint(MERCHANT_MIN, MERCHANT_MAX)
unused_merchants_count = randint(MERCHANT_SKIP_MIN, MERCHANT_SKIP_MAX)
merchant_ids = list(range(1, merchants_count))
merchant_ids = sorted(sample(merchant_ids, merchants_count-unused_merchants_count))
logging.debug('merchant count: %s, merchants skipped: %s, merchant ids: %s', merchants_count, unused_merchants_count,
              len(merchant_ids))
logging.info('%s merchant ids were generated', len(merchant_ids))

# Generating filters and messages
FILTER_MAX_COUNT = 20
FILTER_SKEW = 5
ORDER_SKEW = 0.8
DAILY_MSG_MAX = 5000
MSG_SKEW = 50
DAILY_MSG_MULTIPLIER = 10
MSG_MULTIPLIER_SKEW = 0.01
SUCCESS_SKEW = 1
WRITER_LIMIT = 10000

base_date = datetime.today()
insert_a = []
insert_b = []
lines_written = 0
makedirs('insert', exist_ok=True)
with open(path.join('insert', 'insert_a.csv'), 'w') as fh:
    fh.write('merchant_id, message_filter_id, sent_date, total_cnt, success_cnt, problematic_cnt, '
             'mtm_problematic_cnt, nbo_cnt, non_usd_count\n')
with open(path.join('insert', 'insert_b.csv'), 'w') as fh:
    fh.write('merchantid, filterid, orderdate, ordercount\n')
logging.debug('wrote headers')
for merchant in merchant_ids:
    filters = []
    filter_count = int(triangular(1, FILTER_MAX_COUNT, FILTER_SKEW))
    orders, shippings = split(filter_count, 2, 0.75)
    # filters.extend([merchant*10000+100+i for i in range(1, orders+1) if int(triangular(0, 10))])
    filters.extend([merchant*10000+100+i for i in range(1, orders+1)])
    if shippings:
        # filters.extend([merchant*10000+200+i for i in range(1, shippings+1) if int(triangular(0, 10))])
        filters.extend([merchant*10000+200+i for i in range(1, shippings+1)])
    # print(f'Processing merchant {merchant}/{merchants_count-unused_merchants_count}, total filter count: '
    #       f'{filter_count}; o: {orders}, s: {shippings}')
    logging.debug('Processing merchant %s, total filter count: %s; o: %s, s: %s', merchant, filter_count,
                  orders, shippings)
    for date in (base_date - timedelta(x) for x in range(DATERANGE)):
        for filter_id in filters:
            # messages = int(triangular(1, DAILY_MSG_MAX, MSG_SKEW)*triangular(1, DAILY_MSG_MULTIPLIER,
            #                                                                  MSG_MULTIPLIER_SKEW))
            messages = randint(10, DAILY_MSG_MAX)
            # successful_msg, mtm_problematic, nbo_problematic, non_usd = split(messages, 4, SUCCESS_SKEW)
            successful_msg = int(messages*0.95)
            mtm_problematic = int((messages - successful_msg)*0.75)
            nbo_problematic = int((messages - successful_msg - mtm_problematic)*0.5)
            non_usd = messages - successful_msg - mtm_problematic - nbo_problematic
            order_count = int(successful_msg*0.9)
            insert_a.append((merchant, filter_id, str(date.date()), messages, successful_msg, messages - successful_msg,
                             mtm_problematic, nbo_problematic, non_usd))
            insert_b.append((merchant, filter_id, str(date.date()), order_count))
            lines_written += 1
            if lines_written >= WRITER_LIMIT:
                logging.debug('Writing batch to csv')
                write_batch('insert_a.csv', 'insert', insert_a)
                write_batch('insert_b.csv', 'insert', insert_b)
                insert_a, insert_b = [], []
                lines_written = 0
