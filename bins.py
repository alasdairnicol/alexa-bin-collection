#!/usr/bin/env python
from __future__ import print_function
from datetime import date, timedelta

RECYCLING = 'recycling'
RUBBISH = 'rubbish'
GARDEN = 'garden'


class CollectionDate():
    def __init__(self, collection_date, collection_types):
        self.date = collection_date
        self.types = collection_types

    def __str__(self):
        return "{}: {}".format(self.date, ", ".join(self.types))

EXCEPTIONS = {
    date(2016, 12, 30): CollectionDate(date(2016, 12, 31), (RUBBISH,)),
    date(2017, 1, 6): CollectionDate(date(2017, 1, 7), (RECYCLING,)),
}


def create_collections():
    collections = []
    input_date = date(2016, 11, 4)
    collected = (RUBBISH,)
    not_collected = (RECYCLING, GARDEN)
    while input_date < date(2017, 11, 1):
        if input_date in EXCEPTIONS:
            collection = EXCEPTIONS[input_date]
        else:
            collection = CollectionDate(input_date, collected)
        collections.append(collection)
        collected, not_collected = not_collected, collected
        input_date += timedelta(days=7)

    return collections


def get_next_bin_collection(input_date=None):
    if input_date is None:
        input_date = date.today()
    collections = create_collections()

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
