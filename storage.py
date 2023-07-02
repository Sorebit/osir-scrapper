from contextlib import contextmanager
import csv
from dataclasses import dataclass
import pathlib

from model import GroupData

class Storage:
    async def save(self, data):
        raise NotImplementedError()


class CsvStorage(Storage):
    """One line per entry or maybe an read-or-append-only csv list?"""
    def __init__(self, filename):
        self.path = pathlib.Path(filename)
        self.delimiter = ','
        self.quotechar = '"'
        self.touch()

    def touch(self):
        if self.path.exists():
            return
        with self.get_writer(mode='w') as w:
            w.writerow(row := ['Datetime', 'Group', 'People'])
            print('[x]', 'Column names', row)

    async def save(self, data: list[GroupData]):
        with self.get_writer(mode='a') as w:
            for group_data in data:
                w.writerow(row := [group_data.dt, group_data.group, group_data.people])
                print('[x]', row)

    @contextmanager
    def get_writer(self, mode):
        with open(self.path, mode=mode) as out_file:
            writer = csv.writer(out_file, delimiter=self.delimiter, quotechar=self.quotechar)
            yield writer
