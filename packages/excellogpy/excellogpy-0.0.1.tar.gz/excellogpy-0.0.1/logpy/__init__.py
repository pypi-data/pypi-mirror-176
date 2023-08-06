__version__ = '0.0.1'

from .log import Log
from .entry import Entry

from pathlib import Path
from typing import Union
from datetime import datetime, timedelta

from openpyxl import load_workbook


DAYS = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7
}


def load_log(path: Union[Path, str]) -> Log:
    """
    Loading log from folder
    :param path: Union[Path, str]
    :return: Log
    """
    path = Path(path)
    log = Log(path.name)
    for year_dir in path.iterdir():
        year = int(year_dir.name)
        for week_dir in year_dir.iterdir():
            week = int(week_dir.name.split('.')[0][1:])
            work_book = load_workbook(week_dir, read_only=True, data_only=True)
            for day in DAYS.keys():
                date = datetime.fromisocalendar(year, week, DAYS[day])
                try: sheet = work_book[day]
                except KeyError: continue

                for row in sheet.iter_rows(3):
                    row = [cell.value for cell in row]
                    if not row[0]: break

                    start_time = {
                        'hours': row[0].hour,
                        'minutes': row[0].minute
                    }

                    if row[1].hour == 0:
                        end_time = {
                            'days': 1
                        }
                    else:
                        end_time = {
                            'hours': row[1].hour,
                            'minutes': row[1].minute
                        }

                    row[0] = date + timedelta(**start_time)
                    row[1] = date + timedelta(**end_time)

                    log.add_entry(Entry(*row))

            work_book.close()

    return log
