import datetime
import pytest

from main import evaluate_dayandtimerange

# Define the test cases


@pytest.mark.asyncio
async def test_within_range_single_day():
    data = {
        'now': datetime.datetime(2024, 6, 4, 12, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '08:00:00',
            'end_day_of_week': 1,
            'end_time': '18:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is True


@pytest.mark.asyncio
async def test_outside_range_single_day():
    data = {
        'now': datetime.datetime(2024, 6, 4, 19, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '08:00:00',
            'end_day_of_week': 1,
            'end_time': '18:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_within_range_multiple_days():
    data = {
        'now': datetime.datetime(2024, 6, 4, 2, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': 0,  # Sunday
            'start_time': '23:00:00',
            'end_day_of_week': 2,  # Wednesday
            'end_time': '03:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is True


@pytest.mark.asyncio
async def test_outside_range_multiple_days():
    data = {
        'now': datetime.datetime(2024, 6, 4, 4, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': 0,  # Sunday
            'start_time': '23:00:00',
            'end_day_of_week': 2,  # Wednesday
            'end_time': '03:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_invalid_start_day():
    data = {
        'now': datetime.datetime(2024, 6, 4, 12, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': -1,
            'start_time': '08:00:00',
            'end_day_of_week': 1,
            'end_time': '18:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_invalid_end_day():
    data = {
        'now': datetime.datetime(2024, 6, 4, 12, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '08:00:00',
            'end_day_of_week': -1,
            'end_time': '18:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_invalid_start_time():
    data = {
        'now': datetime.datetime(2024, 6, 4, 12, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '-1:-1:-1',
            'end_day_of_week': 1,
            'end_time': '18:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_invalid_end_time():
    data = {
        'now': datetime.datetime(2024, 6, 4, 12, 0, 0),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '08:00:00',
            'end_day_of_week': 1,
            'end_time': '-1:-1:-1'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False

if __name__ == '__main__':
    pytest.main()
