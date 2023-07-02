import csv
import pathlib

from model import GroupData


class GroupDataStorage():
    """One line per entry or maybe an read-or-append-only csv list?"""
    def __init__(self, filename):
        self.path = pathlib.Path(filename)
        self.delimiter = ','
        self.quotechar = '"'
        
    async def save(self, data: list[GroupData]):
        with open(self.path, mode='a') as out_file:
            writer = csv.writer(out_file, delimiter=self.delimiter, quotechar=self.quotechar)
            for group_data in data:
                row = [group_data.time, group_data.group, group_data.people]
                writer.writerow(row)
                print('[x]', row)
