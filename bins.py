#!/usr/bin/env python
from __future__ import print_function
from datetime import date, timedelta

RECYCLING = 'recycling'
RUBBISH = 'rubbish'
GARDEN = 'garden'


WEEKDAYS = {
    'MONDAY': 1,
    'TUESDAY': 2,
    'WEDNESDAY': 3,
    'THURSDAY': 4,
    'FRIDAY': 5,
    'SATURDAY': 6,
    'SUNDAY': 7,
}


class CollectionDate():
    def __init__(self, collection_date, collection_types):
        self.date = collection_date
        self.types = collection_types

    @staticmethod
    def _suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

    @property
    def friendly_date(self):
        if self.date == date.today():
            return "today"
        elif (self.date - date.today()).days == 1:
            return "tomorrow"
        else:
            weekday = self.date.strftime('%A')
            day = "%s%s" % (self.date.day, self._suffix(self.date.day))
            month = self.date.strftime('%B')
            return "on %s the %s of %s" % (weekday, day, month)

    def __str__(self):
        return "{}: {}".format(self.date, ", ".join(self.types))


EXCEPTIONS = {
    date(2016, 12, 26): CollectionDate(date(2016, 12, 27), (RUBBISH,)),
    date(2016, 12, 27): CollectionDate(date(2016, 12, 28), (RUBBISH,)),
    date(2016, 12, 28): CollectionDate(date(2016, 12, 29), (RUBBISH,)),
    date(2016, 12, 29): CollectionDate(date(2016, 12, 30), (RUBBISH,)),
    date(2016, 12, 30): CollectionDate(date(2016, 12, 31), (RUBBISH,)),
    date(2017, 1, 2): CollectionDate(date(2017, 1, 3), (RECYCLING,)),
    date(2017, 1, 3): CollectionDate(date(2017, 1, 4), (RECYCLING,)),
    date(2017, 1, 4): CollectionDate(date(2017, 1, 5), (RECYCLING,)),
    date(2017, 1, 5): CollectionDate(date(2017, 1, 6), (RECYCLING,)),
    date(2017, 1, 6): CollectionDate(date(2017, 1, 7), (RECYCLING,)),
}


def create_collections(regular_collection_day):
    collections = []
    input_date = date(2016, 10, 30)  # Last Sunday of October 2016
    input_date += timedelta(WEEKDAYS[regular_collection_day])

    collected = (RUBBISH,)
    not_collected = (RECYCLING, GARDEN)
    while input_date < date(2017, 12, 1):
        if input_date in EXCEPTIONS:
            collection = EXCEPTIONS[input_date]
        else:
            collection = CollectionDate(input_date, collected)
        collections.append(collection)
        collected, not_collected = not_collected, collected
        input_date += timedelta(days=7)

    return collections


def get_next_bin_collection(regular_collection_day, input_date=None):
    if input_date is None:
        input_date = date.today()
    collections = create_collections(regular_collection_day)

    for collection in collections:
        if collection.date >= input_date:
            return collection


if __name__ == '__main__':
    collections = create_collections()
    for c in collections:
        print(c)

    print()
    print(get_next_bin_collection(date(2016, 12, 30)))
    print(get_next_bin_collection(date(2016, 12, 31)))
    print(get_next_bin_collection(date(2017, 1, 1)))
    print(get_next_bin_collection(date(2017, 1, 6)))
    print(get_next_bin_collection(date(2017, 1, 7)))
    print(get_next_bin_collection(date(2017, 1, 8)))

    # print(get_bin_collection())
