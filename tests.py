from datetime import date

import pytest

from freezegun import freeze_time

from bins import get_next_bin_collection, CollectionDate, RECYCLING, RUBBISH, GARDEN


def test_default_input_date():
    collection = get_next_bin_collection("FRIDAY")
    assert isinstance(collection, CollectionDate)

    with freeze_time("2020-1-15"):
        collection = get_next_bin_collection("FRIDAY")
        assert collection.date == date(2020, 1, 17)
        assert collection.types == (RECYCLING, GARDEN)


@pytest.mark.parametrize("regular_collection_day,input_date,collection_date,collection_types", [
    ["MONDAY", date(2019, 11, 1), date(2019, 11, 4), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 11, 3), date(2019, 11, 4), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 11, 4), date(2019, 11, 4), (RECYCLING, GARDEN)],
    ["MONDAY", date(2019, 11, 5), date(2019, 11, 11), (RUBBISH,)],
    ["MONDAY", date(2019, 11, 10), date(2019, 11, 11), (RUBBISH,)],
    ["MONDAY", date(2019, 11, 11), date(2019, 11, 11), (RUBBISH,)],
    ["MONDAY", date(2019, 11, 12), date(2019, 11, 18), (RECYCLING, GARDEN)],
    ["MONDAY", date(2020, 1, 13), date(2020, 1, 13), (RECYCLING, GARDEN,)],
    ["MONDAY", date(2020, 1, 14), date(2020, 1, 20), (RUBBISH,)],

    ["FRIDAY", date(2019, 11, 1), date(2019, 11, 1), (RUBBISH,)],
    ["FRIDAY", date(2019, 11, 2), date(2019, 11, 8), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 11, 7), date(2019, 11, 8), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 11, 8), date(2019, 11, 8), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2019, 11, 9), date(2019, 11, 15), (RUBBISH,)],
    ["FRIDAY", date(2020, 1, 17), date(2020, 1, 17), (RECYCLING, GARDEN,)],
    ["FRIDAY", date(2020, 1, 18), date(2020, 1, 24), (RUBBISH,)],

    # Predicted dates for 2020
    ["MONDAY", date(2020, 11, 1), date(2020, 11, 2), (RECYCLING, GARDEN)],
    ["MONDAY", date(2020, 11, 2), date(2020, 11, 2), (RECYCLING, GARDEN)],
    ["MONDAY", date(2020, 11, 3), date(2020, 11, 9), (RUBBISH,)],
    ["MONDAY", date(2020, 11, 8), date(2020, 11, 9), (RUBBISH,)],
    ["MONDAY", date(2020, 11, 9), date(2020, 11, 9), (RUBBISH,)],
    ["MONDAY", date(2020, 11, 10), date(2020, 11, 16), (RECYCLING, GARDEN)],

    ["FRIDAY", date(2020, 11, 1), date(2020, 11, 6), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2020, 11, 5), date(2020, 11, 6), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2020, 11, 6), date(2020, 11, 6), (RECYCLING, GARDEN)],
    ["FRIDAY", date(2020, 11, 7), date(2020, 11, 13), (RUBBISH,)],
    ["FRIDAY", date(2020, 11, 12), date(2020, 11, 13), (RUBBISH,)],
    ["FRIDAY", date(2020, 11, 13), date(2020, 11, 13), (RUBBISH,)],
    ["FRIDAY", date(2020, 11, 14), date(2020, 11, 20),(RECYCLING, GARDEN)],
])
def test_get_next_bin_collection(regular_collection_day, input_date, collection_date, collection_types):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


@pytest.mark.parametrize("regular_collection_day,input_date,collection_date,collection_types", [
    ["MONDAY", date(2019, 12, 22), date(2019, 12, 23), (RUBBISH,)],
    ["MONDAY", date(2019, 12, 23), date(2019, 12, 23), (RUBBISH,)],
    ["MONDAY", date(2019, 12, 24), date(2019, 12, 31), (RECYCLING,)],

    ["MONDAY", date(2019, 12, 29), date(2019, 12, 31), (RECYCLING,)],
    ["MONDAY", date(2019, 12, 30), date(2019, 12, 31), (RECYCLING,)],
    ["MONDAY", date(2019, 12, 31), date(2019, 12, 31), (RECYCLING,)],
    ["MONDAY", date(2020, 1, 1), date(2020, 1, 7), (RUBBISH,)],

    ["MONDAY", date(2020, 1, 5), date(2020, 1, 7), (RUBBISH,)],
    ["MONDAY", date(2020, 1, 6), date(2020, 1, 7), (RUBBISH,)],
    ["MONDAY", date(2020, 1, 7), date(2020, 1, 7), (RUBBISH,)],
    ["MONDAY", date(2020, 1, 8), date(2020, 1, 13), (RECYCLING, GARDEN)],  # back to normal

    ["TUESDAY", date(2019, 12, 23), date(2019, 12, 24), (RUBBISH,)],
    ["TUESDAY", date(2019, 12, 24), date(2019, 12, 24), (RUBBISH,)],
    ["TUESDAY", date(2019, 12, 25), date(2020, 1, 2), (RECYCLING,)],

    ["TUESDAY", date(2019, 12, 31), date(2020, 1, 2), (RECYCLING,)],
    ["TUESDAY", date(2020, 1, 1), date(2020, 1, 2), (RECYCLING,)],
    ["TUESDAY", date(2020, 1, 2), date(2020, 1, 2), (RECYCLING,)],
    ["TUESDAY", date(2020, 1, 3), date(2020, 1, 8), (RUBBISH,)],

    ["TUESDAY", date(2020, 1, 6), date(2020, 1, 8), (RUBBISH,)],
    ["TUESDAY", date(2020, 1, 7), date(2020, 1, 8), (RUBBISH,)],
    ["TUESDAY", date(2020, 1, 8), date(2020, 1, 8), (RUBBISH,)],
    ["TUESDAY", date(2020, 1, 9), date(2020, 1, 14), (RECYCLING, GARDEN)],  # back to normal

    ["WEDNESDAY", date(2019, 12, 24), date(2019, 12, 27), (RUBBISH,)],
    ["WEDNESDAY", date(2019, 12, 25), date(2019, 12, 27), (RUBBISH,)],
    ["WEDNESDAY", date(2019, 12, 26), date(2019, 12, 27), (RUBBISH,)],
    ["WEDNESDAY", date(2019, 12, 27), date(2019, 12, 27), (RUBBISH,)],
    ["WEDNESDAY", date(2019, 12, 28), date(2020, 1, 3), (RECYCLING,)],

    ["WEDNESDAY", date(2019, 12, 31), date(2020, 1, 3), (RECYCLING,)],
    ["WEDNESDAY", date(2020, 1, 1), date(2020, 1, 3), (RECYCLING,)],
    ["WEDNESDAY", date(2020, 1, 2), date(2020, 1, 3), (RECYCLING,)],
    ["WEDNESDAY", date(2020, 1, 3), date(2020, 1, 3), (RECYCLING,)],
    ["WEDNESDAY", date(2020, 1, 4), date(2020, 1, 9), (RUBBISH,)],

    ["WEDNESDAY", date(2020, 1, 7), date(2020, 1, 9), (RUBBISH,)],
    ["WEDNESDAY", date(2020, 1, 8), date(2020, 1, 9), (RUBBISH,)],
    ["WEDNESDAY", date(2020, 1, 9), date(2020, 1, 9), (RUBBISH,)],
    ["WEDNESDAY", date(2020, 1, 10), date(2020, 1, 15), (RECYCLING, GARDEN)],  # back to normal

    ["THURSDAY", date(2019, 12, 25), date(2019, 12, 28), (RUBBISH,)],
    ["THURSDAY", date(2019, 12, 26), date(2019, 12, 28), (RUBBISH,)],
    ["THURSDAY", date(2019, 12, 27), date(2019, 12, 28), (RUBBISH,)],
    ["THURSDAY", date(2019, 12, 28), date(2019, 12, 28), (RUBBISH,)],
    ["THURSDAY", date(2019, 12, 29), date(2020, 1, 4), (RECYCLING,)],

    ["THURSDAY", date(2020, 1, 1), date(2020, 1, 4), (RECYCLING,)],
    ["THURSDAY", date(2020, 1, 2), date(2020, 1, 4), (RECYCLING,)],
    ["THURSDAY", date(2020, 1, 3), date(2020, 1, 4), (RECYCLING,)],
    ["THURSDAY", date(2020, 1, 4), date(2020, 1, 4), (RECYCLING,)],
    ["THURSDAY", date(2020, 1, 5), date(2020, 1, 10), (RUBBISH,)],

    ["THURSDAY", date(2020, 1, 8), date(2020, 1, 10), (RUBBISH,)],
    ["THURSDAY", date(2020, 1, 9), date(2020, 1, 10), (RUBBISH,)],
    ["THURSDAY", date(2020, 1, 10), date(2020, 1, 10), (RUBBISH,)],
    ["THURSDAY", date(2020, 1, 11), date(2020, 1, 16), (RECYCLING, GARDEN)],  # back to normal

    ["FRIDAY", date(2019, 12, 26), date(2019, 12, 30), (RUBBISH,)],
    ["FRIDAY", date(2019, 12, 27), date(2019, 12, 30), (RUBBISH,)],
    ["FRIDAY", date(2019, 12, 28), date(2019, 12, 30), (RUBBISH,)],
    ["FRIDAY", date(2019, 12, 29), date(2019, 12, 30), (RUBBISH,)],
    ["FRIDAY", date(2019, 12, 30), date(2019, 12, 30), (RUBBISH,)],
    ["FRIDAY", date(2019, 12, 31), date(2020, 1, 6), (RECYCLING,)],

    ["FRIDAY", date(2020, 1, 2), date(2020, 1, 6), (RECYCLING,)],
    ["FRIDAY", date(2020, 1, 3), date(2020, 1, 6), (RECYCLING,)],
    ["FRIDAY", date(2020, 1, 4), date(2020, 1, 6), (RECYCLING,)],
    ["FRIDAY", date(2020, 1, 5), date(2020, 1, 6), (RECYCLING,)],
    ["FRIDAY", date(2020, 1, 6), date(2020, 1, 6), (RECYCLING,)],
    ["FRIDAY", date(2020, 1, 7), date(2020, 1, 11), (RUBBISH,)],

    ["FRIDAY", date(2020, 1, 9), date(2020, 1, 11), (RUBBISH,)],
    ["FRIDAY", date(2020, 1, 10), date(2020, 1, 11), (RUBBISH,)],
    ["FRIDAY", date(2020, 1, 11), date(2020, 1, 11), (RUBBISH,)],
    ["FRIDAY", date(2020, 1, 12), date(2020, 1, 17), (RECYCLING, GARDEN)],  # back to normal
])
def test_christmas_2019(regular_collection_day, input_date, collection_date, collection_types):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


def test_no_collection_data():
    assert get_next_bin_collection("MONDAY", date(2020, 11, 30)) is not None
    assert get_next_bin_collection("MONDAY", date(2020, 12, 1)) is None

    assert get_next_bin_collection("FRIDAY", date(2020, 11, 27)) is not None
    assert get_next_bin_collection("FRIDAY", date(2020, 11, 28)) is None


def test_no_collection_data_too_early():
    assert get_next_bin_collection("MONDAY", date(2019, 9, 29)) is None
    assert get_next_bin_collection("MONDAY", date(2019, 9, 30)) is not None

    assert get_next_bin_collection("FRIDAY", date(2019, 9, 29)) is None
    assert get_next_bin_collection("FRIDAY", date(2019, 9, 30)) is not None


def test_friendly_date():
    with freeze_time("2017-1-15"):
        collection = CollectionDate(date(2017,1,15), [])
        assert collection.friendly_date == "today"

        collection = CollectionDate(date(2017,1,16), [])
        assert collection.friendly_date == "tomorrow"

        collection = CollectionDate(date(2017,1,17), [])
        assert collection.friendly_date == "on Tuesday the 17th of January"
