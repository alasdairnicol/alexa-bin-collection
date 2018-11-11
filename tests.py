from datetime import date

import pytest

from freezegun import freeze_time

from bins import get_next_bin_collection, CollectionDate, RECYCLING, RUBBISH, GARDEN


def test_default_input_date():
    collection = get_next_bin_collection("FRIDAY")
    assert isinstance(collection, CollectionDate)

    with freeze_time("2019-1-15"):
        collection = get_next_bin_collection("FRIDAY")
        assert collection.date == date(2019, 1, 18)
        assert collection.types == (RECYCLING, GARDEN)


@pytest.mark.parametrize("regular_collection_day,input_date,collection_date,collection_types", [
    ["MONDAY", date(2017, 11, 1), date(2017, 11, 6), (RECYCLING, GARDEN)],
    ["MONDAY", date(2017, 11, 6), date(2017, 11, 6), (RECYCLING, GARDEN)],
    ["MONDAY", date(2017, 11, 7), date(2017, 11, 13), (RUBBISH,)],
    ["MONDAY", date(2017, 11, 13), date(2017, 11, 13), (RUBBISH,)],
    ["MONDAY", date(2017, 11, 14), date(2017, 11, 20), (RECYCLING, GARDEN)],
    ["MONDAY", date(2018, 1, 15), date(2018, 1, 15), (RECYCLING, GARDEN,)],
    ["MONDAY", date(2018, 1, 16), date(2018, 1, 22), (RUBBISH,)],

    ["FRIDAY", date(2017, 11, 1), date(2017, 11, 3), (RUBBISH,)],
    ["FRIDAY", date(2017, 11, 3), date(2017, 11, 3), (RUBBISH,)],
    ["FRIDAY", date(2017, 11, 4), date(2017, 11, 10), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2017, 11, 10), date(2017, 11, 10), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2017, 11, 11), date(2017, 11, 17), (RUBBISH,)],
    ["FRIDAY", date(2018, 1, 19), date(2018, 1, 19), (RECYCLING, GARDEN,)],
    ["FRIDAY", date(2018, 1, 20), date(2018, 1, 26), (RUBBISH,)],

    ["MONDAY", date(2018, 11, 1), date(2018, 11, 5), (RECYCLING, GARDEN)],
    ["MONDAY", date(2018, 11, 5), date(2018, 11, 5), (RECYCLING, GARDEN)],
    ["MONDAY", date(2018, 11, 6), date(2018, 11, 12), (RUBBISH,)],
    ["MONDAY", date(2018, 11, 12), date(2018, 11, 12), (RUBBISH,)],
    ["MONDAY", date(2018, 11, 13), date(2018, 11, 19), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 1, 14), date(2019, 1, 14), (RECYCLING, GARDEN,)],
    ["MONDAY", date(2019, 1, 15), date(2019, 1, 21), (RUBBISH,)],

    ["FRIDAY", date(2018, 11, 1), date(2018, 11, 2), (RUBBISH,)],
    ["FRIDAY", date(2018, 11, 2), date(2018, 11, 2), (RUBBISH,)],
    ["FRIDAY", date(2018, 11, 3), date(2018, 11, 9), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2018, 11, 9), date(2018, 11, 9), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2018, 11, 10), date(2018, 11, 16), (RUBBISH,)],
    ["FRIDAY", date(2019, 1, 18), date(2019, 1, 18), (RECYCLING, GARDEN,)],
    ["FRIDAY", date(2019, 1, 19), date(2019, 1, 25), (RUBBISH,)],

    # Predicted dates for November 2019
    ["MONDAY", date(2019, 11, 1), date(2019, 11, 4), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 11, 3), date(2019, 11, 4), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 11, 4), date(2019, 11, 4), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 11, 5), date(2019, 11, 11), (RUBBISH,)],
    ["MONDAY", date(2019, 11, 10), date(2019, 11, 11), (RUBBISH,)],
    ["MONDAY", date(2019, 11, 11), date(2019, 11, 11), (RUBBISH,)],
    ["MONDAY", date(2019, 11, 12), date(2019, 11, 18), (RECYCLING, GARDEN)],

    ["FRIDAY", date(2019, 11, 1), date(2019, 11, 1), (RUBBISH,)],
    ["FRIDAY", date(2019, 11, 2), date(2019, 11, 8), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 11, 7), date(2019, 11, 8), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 11, 8), date(2019, 11, 8), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 11, 9), date(2019, 11, 15), (RUBBISH,)],
])
def test_get_next_bin_collection(regular_collection_day, input_date, collection_date, collection_types):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


@pytest.mark.parametrize("regular_collection_day,input_date,collection_date,collection_types", [
    ["MONDAY", date(2017, 12, 25), date(2017, 12, 27), (RUBBISH,)],
    ["MONDAY", date(2017, 12, 26), date(2017, 12, 27), (RUBBISH,)],
    ["MONDAY", date(2017, 12, 27), date(2017, 12, 27), (RUBBISH,)],
    ["MONDAY", date(2017, 12, 28), date(2018, 1, 3), (RECYCLING,)],

    ["MONDAY", date(2018, 1, 1), date(2018, 1, 3), (RECYCLING,)],
    ["MONDAY", date(2018, 1, 2), date(2018, 1, 3), (RECYCLING,)],
    ["MONDAY", date(2018, 1, 3), date(2018, 1, 3), (RECYCLING,)],
    ["MONDAY", date(2018, 1, 4), date(2018, 1, 9), (RUBBISH,)],

    ["MONDAY", date(2018, 1, 8), date(2018, 1, 9), (RUBBISH,)],
    ["MONDAY", date(2018, 1, 9), date(2018, 1, 9), (RUBBISH,)],
    ["MONDAY", date(2018, 1, 10), date(2018, 1, 15), (RECYCLING, GARDEN)],  # back to normal

    ["TUESDAY", date(2017, 12, 26), date(2017, 12, 28), (RUBBISH,)],
    ["TUESDAY", date(2017, 12, 27), date(2017, 12, 28), (RUBBISH,)],
    ["TUESDAY", date(2017, 12, 28), date(2017, 12, 28), (RUBBISH,)],
    ["TUESDAY", date(2017, 12, 29), date(2018, 1, 4), (RECYCLING,)],

    ["TUESDAY", date(2018, 1, 2), date(2018, 1, 4), (RECYCLING,)],
    ["TUESDAY", date(2018, 1, 3), date(2018, 1, 4), (RECYCLING,)],
    ["TUESDAY", date(2018, 1, 4), date(2018, 1, 4), (RECYCLING,)],
    ["TUESDAY", date(2018, 1, 5), date(2018, 1, 10), (RUBBISH,)],

    ["TUESDAY", date(2018, 1, 9), date(2018, 1, 10), (RUBBISH,)],
    ["TUESDAY", date(2018, 1, 10), date(2018, 1, 10), (RUBBISH,)],
    ["TUESDAY", date(2018, 1, 11), date(2018, 1, 16), (RECYCLING, GARDEN)],  # back to normal

    ["WEDNESDAY", date(2017, 12, 27), date(2017, 12, 29), (RUBBISH,)],
    ["WEDNESDAY", date(2017, 12, 28), date(2017, 12, 29), (RUBBISH,)],
    ["WEDNESDAY", date(2017, 12, 29), date(2017, 12, 29), (RUBBISH,)],
    ["WEDNESDAY", date(2017, 12, 30), date(2018, 1, 5), (RECYCLING,)],

    ["WEDNESDAY", date(2018, 1, 3), date(2018, 1, 5), (RECYCLING,)],
    ["WEDNESDAY", date(2018, 1, 4), date(2018, 1, 5), (RECYCLING,)],
    ["WEDNESDAY", date(2018, 1, 5), date(2018, 1, 5), (RECYCLING,)],
    ["WEDNESDAY", date(2018, 1, 6), date(2018, 1, 11), (RUBBISH,)],

    ["WEDNESDAY", date(2018, 1, 10), date(2018, 1, 11), (RUBBISH,)],
    ["WEDNESDAY", date(2018, 1, 11), date(2018, 1, 11), (RUBBISH,)],
    ["WEDNESDAY", date(2018, 1, 12), date(2018, 1, 17), (RECYCLING, GARDEN)],  # back to normal

    ["THURSDAY", date(2017, 12, 28), date(2017, 12, 30), (RUBBISH,)],
    ["THURSDAY", date(2017, 12, 29), date(2017, 12, 30), (RUBBISH,)],
    ["THURSDAY", date(2017, 12, 30), date(2017, 12, 30), (RUBBISH,)],
    ["THURSDAY", date(2017, 12, 31), date(2018, 1, 6), (RECYCLING,)],

    ["THURSDAY", date(2018, 1, 4), date(2018, 1, 6), (RECYCLING,)],
    ["THURSDAY", date(2018, 1, 5), date(2018, 1, 6), (RECYCLING,)],
    ["THURSDAY", date(2018, 1, 6), date(2018, 1, 6), (RECYCLING,)],
    ["THURSDAY", date(2018, 1, 7), date(2018, 1, 12), (RUBBISH,)],

    ["THURSDAY", date(2018, 1, 11), date(2018, 1, 12), (RUBBISH,)],
    ["THURSDAY", date(2018, 1, 12), date(2018, 1, 12), (RUBBISH,)],
    ["THURSDAY", date(2018, 1, 13), date(2018, 1, 18), (RECYCLING, GARDEN)],  # back to normal

    ["FRIDAY", date(2017, 12, 29), date(2018, 1, 2), (RUBBISH,)],
    ["FRIDAY", date(2017, 12, 30), date(2018, 1, 2), (RUBBISH,)],
    ["FRIDAY", date(2017, 12, 31), date(2018, 1, 2), (RUBBISH,)],
    ["FRIDAY", date(2018, 1, 1), date(2018, 1, 2), (RUBBISH,)],
    ["FRIDAY", date(2018, 1, 2), date(2018, 1, 2), (RUBBISH,)],
    ["FRIDAY", date(2018, 1, 3), date(2018, 1, 8), (RECYCLING,)],

    ["FRIDAY", date(2018, 1, 5), date(2018, 1, 8), (RECYCLING,)],
    ["FRIDAY", date(2018, 1, 6), date(2018, 1, 8), (RECYCLING,)],
    ["FRIDAY", date(2018, 1, 7), date(2018, 1, 8), (RECYCLING,)],
    ["FRIDAY", date(2018, 1, 8), date(2018, 1, 8), (RECYCLING,)],
    ["FRIDAY", date(2018, 1, 9), date(2018, 1, 13), (RUBBISH,)],

    ["FRIDAY", date(2018, 1, 12), date(2018, 1, 13), (RUBBISH,)],
    ["FRIDAY", date(2018, 1, 13), date(2018, 1, 13), (RUBBISH,)],
    ["FRIDAY", date(2018, 1, 14), date(2018, 1, 19), (RECYCLING, GARDEN)],  # back to normal
])
def test_christmas_2017(regular_collection_day, input_date, collection_date, collection_types):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


@pytest.mark.parametrize("regular_collection_day,input_date,collection_date,collection_types", [
    ["MONDAY", date(2018, 12, 23), date(2018, 12, 24), (RUBBISH,)],
    ["MONDAY", date(2018, 12, 24), date(2018, 12, 24), (RUBBISH,)],
    ["MONDAY", date(2018, 12, 25), date(2019, 1, 2), (RECYCLING, GARDEN)],

    ["MONDAY", date(2018, 12, 30), date(2019, 1, 2), (RECYCLING, GARDEN)],
    ["MONDAY", date(2018, 12, 31), date(2019, 1, 2), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 1, 1), date(2019, 1, 2), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 1, 2), date(2019, 1, 2), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 1, 3), date(2019, 1, 8), (RUBBISH,)],

    ["MONDAY", date(2019, 1, 6), date(2019, 1, 8), (RUBBISH,)],
    ["MONDAY", date(2019, 1, 7), date(2019, 1, 8), (RUBBISH,)],
    ["MONDAY", date(2019, 1, 8), date(2019, 1, 8), (RUBBISH,)],
    ["MONDAY", date(2019, 1, 9), date(2019, 1, 14), (RECYCLING, GARDEN)],  # back to normal

    ["TUESDAY", date(2018, 12, 24), date(2018, 12, 27), (RUBBISH,)],
    ["TUESDAY", date(2018, 12, 25), date(2018, 12, 27), (RUBBISH,)],
    ["TUESDAY", date(2018, 12, 26), date(2018, 12, 27), (RUBBISH,)],
    ["TUESDAY", date(2018, 12, 27), date(2018, 12, 27), (RUBBISH,)],
    ["TUESDAY", date(2018, 12, 28), date(2019, 1, 3), (RECYCLING, GARDEN)],

    ["TUESDAY", date(2018, 12, 31), date(2019, 1, 3), (RECYCLING, GARDEN)],
    ["TUESDAY", date(2019, 1, 1), date(2019, 1, 3), (RECYCLING, GARDEN)],
    ["TUESDAY", date(2019, 1, 2), date(2019, 1, 3), (RECYCLING, GARDEN)],
    ["TUESDAY", date(2019, 1, 3), date(2019, 1, 3), (RECYCLING, GARDEN)],
    ["TUESDAY", date(2019, 1, 4), date(2019, 1, 9), (RUBBISH,)],

    ["TUESDAY", date(2019, 1, 7), date(2019, 1, 9), (RUBBISH,)],
    ["TUESDAY", date(2019, 1, 8), date(2019, 1, 9), (RUBBISH,)],
    ["TUESDAY", date(2019, 1, 9), date(2019, 1, 9), (RUBBISH,)],
    ["TUESDAY", date(2019, 1, 10), date(2019, 1, 15), (RECYCLING, GARDEN)],  # back to normal

    ["WEDNESDAY", date(2018, 12, 25), date(2018, 12, 28), (RUBBISH,)],
    ["WEDNESDAY", date(2018, 12, 26), date(2018, 12, 28), (RUBBISH,)],
    ["WEDNESDAY", date(2018, 12, 27), date(2018, 12, 28), (RUBBISH,)],
    ["WEDNESDAY", date(2018, 12, 28), date(2018, 12, 28), (RUBBISH,)],
    ["WEDNESDAY", date(2018, 12, 29), date(2019, 1, 4), (RECYCLING, GARDEN)],

    ["WEDNESDAY", date(2019, 1, 1), date(2019, 1, 4), (RECYCLING, GARDEN)],
    ["WEDNESDAY", date(2019, 1, 2), date(2019, 1, 4), (RECYCLING, GARDEN)],
    ["WEDNESDAY", date(2019, 1, 3), date(2019, 1, 4), (RECYCLING, GARDEN)],
    ["WEDNESDAY", date(2019, 1, 4), date(2019, 1, 4), (RECYCLING, GARDEN)],
    ["WEDNESDAY", date(2019, 1, 5), date(2019, 1, 10), (RUBBISH,)],

    ["WEDNESDAY", date(2019, 1, 8), date(2019, 1, 10), (RUBBISH,)],
    ["WEDNESDAY", date(2019, 1, 9), date(2019, 1, 10), (RUBBISH,)],
    ["WEDNESDAY", date(2019, 1, 10), date(2019, 1, 10), (RUBBISH,)],
    ["WEDNESDAY", date(2019, 1, 11), date(2019, 1, 16), (RECYCLING, GARDEN)],  # back to normal

    ["THURSDAY", date(2018, 12, 26), date(2018, 12, 29), (RUBBISH,)],
    ["THURSDAY", date(2018, 12, 27), date(2018, 12, 29), (RUBBISH,)],
    ["THURSDAY", date(2018, 12, 28), date(2018, 12, 29), (RUBBISH,)],
    ["THURSDAY", date(2018, 12, 29), date(2018, 12, 29), (RUBBISH,)],
    ["THURSDAY", date(2018, 12, 30), date(2019, 1, 5), (RECYCLING, GARDEN)],

    ["THURSDAY", date(2019, 1, 2), date(2019, 1, 5), (RECYCLING, GARDEN)],
    ["THURSDAY", date(2019, 1, 3), date(2019, 1, 5), (RECYCLING, GARDEN)],
    ["THURSDAY", date(2019, 1, 4), date(2019, 1, 5), (RECYCLING, GARDEN)],
    ["THURSDAY", date(2019, 1, 5), date(2019, 1, 5), (RECYCLING, GARDEN)],
    ["THURSDAY", date(2019, 1, 6), date(2019, 1, 11), (RUBBISH,)],

    ["THURSDAY", date(2019, 1, 9), date(2019, 1, 11), (RUBBISH,)],
    ["THURSDAY", date(2019, 1, 10), date(2019, 1, 11), (RUBBISH,)],
    ["THURSDAY", date(2019, 1, 11), date(2019, 1, 11), (RUBBISH,)],
    ["THURSDAY", date(2019, 1, 12), date(2019, 1, 17), (RECYCLING, GARDEN)],  # back to normal

    ["FRIDAY", date(2018, 12, 27), date(2018, 12, 31), (RUBBISH,)],
    ["FRIDAY", date(2018, 12, 28), date(2018, 12, 31), (RUBBISH,)],
    ["FRIDAY", date(2018, 12, 29), date(2018, 12, 31), (RUBBISH,)],
    ["FRIDAY", date(2018, 12, 30), date(2018, 12, 31), (RUBBISH,)],
    ["FRIDAY", date(2018, 12, 31), date(2018, 12, 31), (RUBBISH,)],
    ["FRIDAY", date(2019, 1, 1), date(2019, 1, 7), (RECYCLING, GARDEN)],

    ["FRIDAY", date(2019, 1, 3), date(2019, 1, 7), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 1, 4), date(2019, 1, 7), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 1, 5), date(2019, 1, 7), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 1, 6), date(2019, 1, 7), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 1, 7), date(2019, 1, 7), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 1, 8), date(2019, 1, 12), (RUBBISH,)],

    ["FRIDAY", date(2019, 1, 10), date(2019, 1, 12), (RUBBISH,)],
    ["FRIDAY", date(2019, 1, 11), date(2019, 1, 12), (RUBBISH,)],
    ["FRIDAY", date(2019, 1, 12), date(2019, 1, 12), (RUBBISH,)],
    ["FRIDAY", date(2019, 1, 13), date(2019, 1, 18), (RECYCLING, GARDEN)],  # back to normal
])
def test_christmas_2018(regular_collection_day, input_date, collection_date, collection_types):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


def test_no_collection_data():
    assert get_next_bin_collection("MONDAY", date(2019, 11, 25)) is not None
    assert get_next_bin_collection("MONDAY", date(2019, 11, 26)) is None

    assert get_next_bin_collection("FRIDAY", date(2019, 11, 29)) is not None
    assert get_next_bin_collection("FRIDAY", date(2019, 11, 30)) is None


def test_friendly_date():
    with freeze_time("2017-1-15"):
        collection = CollectionDate(date(2017,1,15), [])
        assert collection.friendly_date == "today"

        collection = CollectionDate(date(2017,1,16), [])
        assert collection.friendly_date == "tomorrow"

        collection = CollectionDate(date(2017,1,17), [])
        assert collection.friendly_date == "on Tuesday the 17th of January"
