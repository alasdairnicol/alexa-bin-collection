from datetime import date

import pytest

from freezegun import freeze_time

from bins import get_next_bin_collection, CollectionDate, RECYCLING, RUBBISH, GARDEN


def test_no_input_date():
    collection = get_next_bin_collection()
    assert isinstance(collection, CollectionDate)

    with freeze_time("2017-1-15"):
        collection = get_next_bin_collection()
        assert collection.date == date(2017, 1, 20)
        assert collection.types == (RECYCLING, GARDEN)


@pytest.mark.parametrize("input_date,collection_date,collection_types", [
    [date(2016, 11, 4), date(2016, 11, 4), (RUBBISH,)],
    [date(2016, 11, 5), date(2016, 11, 11), (RECYCLING, GARDEN)],
    [date(2016, 11, 11), date(2016, 11, 11), (RECYCLING, GARDEN)],
    [date(2016, 11, 12), date(2016, 11, 18), (RUBBISH,)],
    [date(2017, 1, 13), date(2017, 1, 13), (RUBBISH,)],
    [date(2017, 1, 14), date(2017, 1, 20), (RECYCLING, GARDEN)],
])  
def test_get_next_bin_collection(input_date, collection_date, collection_types):
    collection = get_next_bin_collection(input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


@pytest.mark.parametrize("input_date,collection_date,collection_types", [
    [date(2016, 12, 30), date(2016, 12, 31), (RUBBISH,)],
    [date(2016, 12, 31), date(2016, 12, 31), (RUBBISH,)],
    [date(2017, 1, 1), date(2017, 1, 7), (RECYCLING,)],
    [date(2017, 1, 6), date(2017, 1, 7), (RECYCLING,)],
    [date(2017, 1, 7), date(2017, 1, 7), (RECYCLING,)],
    [date(2017, 1, 8), date(2017, 1, 13), (RUBBISH,)],  # back to normal
])
def test_chrismas_2016(input_date, collection_date, collection_types):
    collection = get_next_bin_collection(input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types
    

def test_no_collection_data():
    # 2017-10-27 is the last Friday collection we have data for 
    assert get_next_bin_collection(date(2017, 10, 27)) is not None
    # We do not have any collection data after this
    assert get_next_bin_collection(date(2017, 10, 28)) is None
    assert get_next_bin_collection(date(2017, 11, 1)) is None
