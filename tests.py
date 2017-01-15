from datetime import date

import pytest

from freezegun import freeze_time

from bins import get_next_bin_collection, CollectionDate, RECYCLING, RUBBISH, GARDEN


def test_no_input_date():
    collection = get_next_bin_collection("FRIDAY")
    assert isinstance(collection, CollectionDate)

    with freeze_time("2017-1-15"):
        collection = get_next_bin_collection("FRIDAY")
        assert collection.date == date(2017, 1, 20)
        assert collection.types == (RECYCLING, GARDEN)


@pytest.mark.parametrize("regular_collection_day,input_date,collection_date,collection_types", [
    ["MONDAY", date(2016, 11, 1), date(2016, 11, 7), (RECYCLING, GARDEN)],
    ["MONDAY", date(2016, 11, 7), date(2016, 11, 7), (RECYCLING, GARDEN)],
    ["MONDAY", date(2016, 11, 8), date(2016, 11, 14), (RUBBISH,)],
    ["MONDAY", date(2016, 11, 14), date(2016, 11, 14), (RUBBISH,)],
    ["MONDAY", date(2016, 11, 15), date(2016, 11, 21), (RECYCLING, GARDEN)],
    ["MONDAY", date(2017, 1, 9), date(2017, 1, 9), (RUBBISH,)],
    ["MONDAY", date(2017, 1, 10), date(2017, 1, 16), (RECYCLING, GARDEN)],

    ["FRIDAY", date(2016, 11, 1), date(2016, 11, 4), (RUBBISH,)],
    ["FRIDAY", date(2016, 11, 4), date(2016, 11, 4), (RUBBISH,)],
    ["FRIDAY", date(2016, 11, 5), date(2016, 11, 11), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2016, 11, 11), date(2016, 11, 11), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2016, 11, 12), date(2016, 11, 18), (RUBBISH,)],
    ["FRIDAY", date(2017, 1, 13), date(2017, 1, 13), (RUBBISH,)],
    ["FRIDAY", date(2017, 1, 14), date(2017, 1, 20), (RECYCLING, GARDEN)],
])  
def test_get_next_bin_collection(regular_collection_day, input_date, collection_date, collection_types):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


@pytest.mark.parametrize("regular_collection_day,input_date,collection_date,collection_types", [
    ["MONDAY", date(2016, 12, 26), date(2016, 12, 27), (RUBBISH,)],
    ["MONDAY", date(2016, 12, 27), date(2016, 12, 27), (RUBBISH,)],
    ["MONDAY", date(2016, 12, 28), date(2017, 1, 3), (RECYCLING,)],
    ["MONDAY", date(2017, 1, 2), date(2017, 1, 3), (RECYCLING,)],
    ["MONDAY", date(2017, 1, 3), date(2017, 1, 3), (RECYCLING,)],
    ["MONDAY", date(2017, 1, 4), date(2017, 1, 9), (RUBBISH,)],  # back to normal

    ["FRIDAY", date(2016, 12, 30), date(2016, 12, 31), (RUBBISH,)],
    ["FRIDAY", date(2016, 12, 31), date(2016, 12, 31), (RUBBISH,)],
    ["FRIDAY", date(2017, 1, 1), date(2017, 1, 7), (RECYCLING,)],
    ["FRIDAY", date(2017, 1, 6), date(2017, 1, 7), (RECYCLING,)],
    ["FRIDAY", date(2017, 1, 7), date(2017, 1, 7), (RECYCLING,)],
    ["FRIDAY", date(2017, 1, 8), date(2017, 1, 13), (RUBBISH,)],  # back to normal
])
def test_chrismas_2016(regular_collection_day, input_date, collection_date, collection_types):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types
    

def test_no_collection_data():
    assert get_next_bin_collection("FRIDAY", date(2017, 10, 27)) is not None
    assert get_next_bin_collection("FRIDAY", date(2017, 10, 28)) is None

    assert get_next_bin_collection("MONDAY", date(2017, 10, 30)) is not None
    assert get_next_bin_collection("MONDAY", date(2017, 10, 31)) is None

    assert get_next_bin_collection("TUESDAY", date(2017, 10, 31)) is not None
    assert get_next_bin_collection("TUESDAY", date(2017, 11, 1)) is None
