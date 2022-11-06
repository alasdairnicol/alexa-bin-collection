from datetime import date

import pytest

from freezegun import freeze_time

from bins import get_next_bin_collection, CollectionDate, RECYCLING, RUBBISH


def test_default_input_date():
    collection = get_next_bin_collection("FRIDAY")
    assert isinstance(collection, CollectionDate)

    with freeze_time("2022-01-11"):
        collection = get_next_bin_collection("FRIDAY")
        assert collection.date == date(2022, 1, 14)
        assert collection.types == (RECYCLING,)


@pytest.mark.parametrize(
    "regular_collection_day,input_date,collection_date,collection_types",
    [
        ["MONDAY", date(2021, 11, 1), date(2021, 11, 1), (RECYCLING,)],
        ["MONDAY", date(2021, 11, 2), date(2021, 11, 8), (RUBBISH,)],
        ["MONDAY", date(2021, 11, 3), date(2021, 11, 8), (RUBBISH,)],
        ["MONDAY", date(2021, 11, 7), date(2021, 11, 8), (RUBBISH,)],
        ["MONDAY", date(2021, 11, 8), date(2021, 11, 8), (RUBBISH,)],
        ["MONDAY", date(2021, 11, 9), date(2021, 11, 15), (RECYCLING,)],
        ["FRIDAY", date(2021, 11, 1), date(2021, 11, 5), (RECYCLING,)],
        ["FRIDAY", date(2021, 11, 4), date(2021, 11, 5), (RECYCLING,)],
        ["FRIDAY", date(2021, 11, 5), date(2021, 11, 5), (RECYCLING,)],
        ["FRIDAY", date(2021, 11, 6), date(2021, 11, 12), (RUBBISH,)],
        ["FRIDAY", date(2021, 11, 11), date(2021, 11, 12), (RUBBISH,)],
        ["FRIDAY", date(2021, 11, 12), date(2021, 11, 12), (RUBBISH,)],
        ["FRIDAY", date(2021, 11, 13), date(2021, 11, 19), (RECYCLING,)],
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
        ["MONDAY", date(2021, 12, 20), date(2021, 12, 20), (RUBBISH,)],
        ["MONDAY", date(2021, 12, 21), date(2021, 12, 28), (RECYCLING,)],
        ["MONDAY", date(2021, 12, 27), date(2021, 12, 28), (RECYCLING,)],
        ["MONDAY", date(2021, 12, 28), date(2021, 12, 28), (RECYCLING,)],
        ["MONDAY", date(2021, 12, 29), date(2022, 1, 4), (RUBBISH,)],
        ["MONDAY", date(2022, 1, 3), date(2022, 1, 4), (RUBBISH,)],
        ["MONDAY", date(2022, 1, 4), date(2022, 1, 4), (RUBBISH,)],
        ["MONDAY", date(2022, 1, 5), date(2022, 1, 10), (RECYCLING,)],  # back to normal
        ["TUESDAY", date(2021, 12, 21), date(2021, 12, 21), (RUBBISH,)],
        ["TUESDAY", date(2021, 12, 22), date(2021, 12, 29), (RECYCLING,)],
        ["TUESDAY", date(2021, 12, 28), date(2021, 12, 29), (RECYCLING,)],
        ["TUESDAY", date(2021, 12, 29), date(2021, 12, 29), (RECYCLING,)],
        ["TUESDAY", date(2021, 12, 30), date(2022, 1, 5), (RUBBISH,)],
        ["TUESDAY", date(2022, 1, 4), date(2022, 1, 5), (RUBBISH,)],
        ["TUESDAY", date(2022, 1, 5), date(2022, 1, 5), (RUBBISH,)],
        ["TUESDAY", date(2022, 1, 6), date(2022, 1, 11), (RECYCLING,)],  # back to normal
        ["WEDNESDAY", date(2021, 12, 22), date(2021, 12, 22), (RUBBISH,)],
        ["WEDNESDAY", date(2021, 12, 23), date(2021, 12, 30), (RECYCLING,)],
        ["WEDNESDAY", date(2021, 12, 29), date(2021, 12, 30), (RECYCLING,)],
        ["WEDNESDAY", date(2021, 12, 30), date(2021, 12, 30), (RECYCLING,)],
        ["WEDNESDAY", date(2021, 12, 31), date(2022, 1, 6), (RUBBISH,)],
        ["WEDNESDAY", date(2022, 1, 5), date(2022, 1, 6), (RUBBISH,)],
        ["WEDNESDAY", date(2022, 1, 6), date(2022, 1, 6), (RUBBISH,)],
        ["WEDNESDAY", date(2022, 1, 7), date(2022, 1, 12), (RECYCLING,)],  # back to normal
        ["THURSDAY", date(2021, 12, 23), date(2021, 12, 23), (RUBBISH,)],
        ["THURSDAY", date(2021, 12, 24), date(2021, 12, 31), (RECYCLING,)],
        ["THURSDAY", date(2021, 12, 30), date(2021, 12, 31), (RECYCLING,)],
        ["THURSDAY", date(2021, 12, 31), date(2021, 12, 31), (RECYCLING,)],
        ["THURSDAY", date(2022, 1, 1), date(2022, 1, 7), (RUBBISH,)],
        ["THURSDAY", date(2022, 1, 6), date(2022, 1, 7), (RUBBISH,)],
        ["THURSDAY", date(2022, 1, 7), date(2022, 1, 7), (RUBBISH,)],
        ["THURSDAY", date(2022, 1, 8), date(2022, 1, 13), (RECYCLING,)],  # back to normal
        ["FRIDAY", date(2021, 12, 24), date(2021, 12, 24), (RUBBISH,)],
        ["FRIDAY", date(2021, 12, 25), date(2022, 1, 3), (RECYCLING,)],
        ["FRIDAY", date(2022, 1, 2), date(2022, 1, 3), (RECYCLING,)],
        ["FRIDAY", date(2022, 1, 3), date(2022, 1, 3), (RECYCLING,)],
        ["FRIDAY", date(2022, 1, 4), date(2022, 1, 8), (RUBBISH,)],
        ["FRIDAY", date(2022, 1, 7), date(2022, 1, 8), (RUBBISH,)],
        ["FRIDAY", date(2022, 1, 8), date(2022, 1, 8), (RUBBISH,)],
        ["FRIDAY", date(2022, 1, 9), date(2022, 1, 14), (RECYCLING,)],  # back to normal
    ],
)
def test_christmas_2021(
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
    assert get_next_bin_collection("MONDAY", date(2022, 12, 5)) is not None
    assert get_next_bin_collection("MONDAY", date(2022, 12, 6)) is None

    assert get_next_bin_collection("FRIDAY", date(2022, 12, 9)) is not None
    assert get_next_bin_collection("FRIDAY", date(2022, 12, 10)) is None


def test_no_collection_data_too_early():
    assert get_next_bin_collection("MONDAY", date(2020, 9, 27)) is None
    assert get_next_bin_collection("MONDAY", date(2020, 9, 28)) is not None

    assert get_next_bin_collection("FRIDAY", date(2020, 9, 27)) is None
    assert get_next_bin_collection("FRIDAY", date(2020, 9, 28)) is not None


def test_friendly_date():
    with freeze_time("2017-1-15"):
        collection = CollectionDate(date(2017, 1, 15), [])
        assert collection.friendly_date == "today"

        collection = CollectionDate(date(2017, 1, 16), [])
        assert collection.friendly_date == "tomorrow"

        collection = CollectionDate(date(2017, 1, 17), [])
        assert collection.friendly_date == "on Tuesday the 17th of January"
