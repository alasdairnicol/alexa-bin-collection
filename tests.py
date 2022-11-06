from datetime import date

import pytest

from freezegun import freeze_time

from bins import get_next_bin_collection, CollectionDate, RECYCLING, RUBBISH


def test_default_input_date():
    collection = get_next_bin_collection("FRIDAY")
    assert isinstance(collection, CollectionDate)

    with freeze_time("2023-01-11"):
        collection = get_next_bin_collection("FRIDAY")
        assert collection.date == date(2023, 1, 13)
        assert collection.types == (RECYCLING,)


@pytest.mark.parametrize(
    "regular_collection_day,input_date,collection_date,collection_types",
    [
        ["MONDAY", date(2022, 10, 31), date(2022, 10, 31), (RECYCLING,)],
        ["MONDAY", date(2022, 11, 1), date(2022, 11, 7), (RUBBISH,)],
        ["MONDAY", date(2022, 11, 6), date(2022, 11, 7), (RUBBISH,)],
        ["MONDAY", date(2022, 11, 7), date(2022, 11, 7), (RUBBISH,)],
        ["MONDAY", date(2022, 11, 8), date(2022, 11, 14), (RECYCLING,)],
        ["FRIDAY", date(2022, 11, 1), date(2022, 11, 4), (RECYCLING,)],
        ["FRIDAY", date(2022, 11, 3), date(2022, 11, 4), (RECYCLING,)],
        ["FRIDAY", date(2022, 11, 4), date(2022, 11, 4), (RECYCLING,)],
        ["FRIDAY", date(2022, 11, 5), date(2022, 11, 11), (RUBBISH,)],
        ["FRIDAY", date(2022, 11, 10), date(2022, 11, 11), (RUBBISH,)],
        ["FRIDAY", date(2022, 11, 11), date(2022, 11, 11), (RUBBISH,)],
        ["FRIDAY", date(2022, 11, 12), date(2022, 11, 18), (RECYCLING,)],


    ],
)
def test_get_next_bin_collection(
    regular_collection_day, input_date, collection_date, collection_types
):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


@pytest.mark.parametrize(
    "regular_collection_day,input_date,collection_date,collection_types",
    [
        ["MONDAY", date(2022, 12, 19), date(2022, 12, 19), (RUBBISH,)],
        ["MONDAY", date(2022, 12, 20), date(2022, 12, 27), (RECYCLING,)],
        ["MONDAY", date(2022, 12, 26), date(2022, 12, 27), (RECYCLING,)],
        ["MONDAY", date(2022, 12, 27), date(2022, 12, 27), (RECYCLING,)],
        ["MONDAY", date(2022, 12, 28), date(2023, 1, 2), (RUBBISH,)],  # back to normal
        ["TUESDAY", date(2022, 12, 20), date(2022, 12, 20), (RUBBISH,)],
        ["TUESDAY", date(2022, 12, 21), date(2022, 12, 28), (RECYCLING,)],
        ["TUESDAY", date(2022, 12, 27), date(2022, 12, 28), (RECYCLING,)],
        ["TUESDAY", date(2022, 12, 28), date(2022, 12, 28), (RECYCLING,)],
        ["TUESDAY", date(2022, 12, 29), date(2023, 1, 3), (RUBBISH,)],  # back to normal
        ["WEDNESDAY", date(2022, 12, 21), date(2022, 12, 21), (RUBBISH,)],
        ["WEDNESDAY", date(2022, 12, 22), date(2022, 12, 29), (RECYCLING,)],
        ["WEDNESDAY", date(2022, 12, 28), date(2022, 12, 29), (RECYCLING,)],
        ["WEDNESDAY", date(2022, 12, 29), date(2022, 12, 29), (RECYCLING,)],
        ["WEDNESDAY", date(2022, 12, 30), date(2023, 1, 4), (RUBBISH,)],  # back to normal
        ["THURSDAY", date(2022, 12, 22), date(2022, 12, 22), (RUBBISH,)],
        ["THURSDAY", date(2022, 12, 23), date(2022, 12, 30), (RECYCLING,)],
        ["THURSDAY", date(2022, 12, 24), date(2022, 12, 30), (RECYCLING,)],
        ["THURSDAY", date(2022, 12, 30), date(2022, 12, 30), (RECYCLING,)],
        ["THURSDAY", date(2022, 12, 31), date(2023, 1, 5), (RUBBISH,)],  # back to normal
        ["FRIDAY", date(2022, 12, 23), date(2022, 12, 23), (RUBBISH,)],
        ["FRIDAY", date(2022, 12, 24), date(2022, 12, 31), (RECYCLING,)],
        ["FRIDAY", date(2022, 12, 30), date(2022, 12, 31), (RECYCLING,)],
        ["FRIDAY", date(2022, 12, 31), date(2022, 12, 31), (RECYCLING,)],
        ["FRIDAY", date(2023, 1, 1), date(2023, 1, 6), (RUBBISH,)],  # back to normal
    ],
)
def test_christmas_2022(
    regular_collection_day, input_date, collection_date, collection_types
):
    collection = get_next_bin_collection(regular_collection_day, input_date)
    assert collection.date == collection_date
    assert collection.types == collection_types


def test_no_collection_data():
    assert get_next_bin_collection("MONDAY", date(2023, 12, 4)) is not None
    assert get_next_bin_collection("MONDAY", date(2023, 12, 5)) is None

    assert get_next_bin_collection("FRIDAY", date(2023, 12, 8)) is not None
    assert get_next_bin_collection("FRIDAY", date(2023, 12, 9)) is None


def test_no_collection_data_too_early():
    assert get_next_bin_collection("MONDAY", date(2022, 10, 30)) is None
    assert get_next_bin_collection("MONDAY", date(2022, 10, 31)) is not None

    assert get_next_bin_collection("FRIDAY", date(2022, 10, 30)) is None
    assert get_next_bin_collection("FRIDAY", date(2022, 10, 31)) is not None


def test_friendly_date():
    with freeze_time("2017-1-15"):
        collection = CollectionDate(date(2017, 1, 15), [])
        assert collection.friendly_date == "today"

        collection = CollectionDate(date(2017, 1, 16), [])
        assert collection.friendly_date == "tomorrow"

        collection = CollectionDate(date(2017, 1, 17), [])
        assert collection.friendly_date == "on Tuesday the 17th of January"
