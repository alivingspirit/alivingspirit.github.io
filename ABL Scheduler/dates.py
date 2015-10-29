import datetime
from datetime import date, timedelta

def get_dates(start_date, num_of_days, dates_to_skip = []):
    td = timedelta(weeks=1)
    next_date = start_date
    count = 0
    while count < num_of_days:
        if not next_date in dates_to_skip:
            yield next_date
            count += 1
        next_date = next_date + td

if __name__ == '__main__':
    d = get_dates( date(2015, 11, 8), 12, [date(2015, 12, 27)])
    print(*list(map(lambda x: x.strftime("%A %d. %B %Y"),d)), sep='\n')
