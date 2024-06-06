from datetime import datetime, timezone
import pytest

from evaluate_dayandtimerange import evaluate_dayandtimerange

# Define the test cases


@pytest.mark.asyncio
async def test_within_range_single_day():
    data = {
        'now': datetime(2024, 6, 4, 12, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
        'now': datetime(2024, 6, 4, 19, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
        'now': datetime(2024, 6, 4, 2, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
        'now': datetime(2024, 6, 4, 4, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
        'now': datetime(2024, 6, 4, 12, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
        'now': datetime(2024, 6, 4, 12, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
        'now': datetime(2024, 6, 4, 12, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
        'now': datetime(2024, 6, 4, 12, 0, 0, tzinfo=timezone.utc),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '08:00:00',
            'end_day_of_week': 1,
            'end_time': '-1:-1:-1'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_edge_case_midnight_single_day():
    data = {
        # Midnight Tuesday
        'now': datetime(2024, 6, 4, 0, 0, 0, tzinfo=timezone.utc),
        'terms': {
            'start_day_of_week': 1,  # Monday
            'start_time': '23:00:00',
            'end_day_of_week': 2,  # Tuesday
            'end_time': '01:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is True


@pytest.mark.asyncio
async def test_edge_case_third_shift_out_of_range():
    # 22:00 - 07:30 Sun to Thurs (PST)

    data = {
        # Tuesday
        'now': datetime(2024, 6, 4, 13, 0, 0, tzinfo=timezone.utc),
        'terms': {
            'start_day_of_week': 1,  # Monday
            'start_time': '05:00:00',
            'end_day_of_week': 5,  # Friday
            'end_time': '14:30:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_not_operator_condition():
    data = {
        'now': datetime(2024, 6, 4, 12, 0, 0, tzinfo=timezone.utc),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '08:00:00',
            'end_day_of_week': 1,
            'end_time': '18:00:00'
        },
        'condition': {
            'not_operator': True
        }
    }
    assert await evaluate_dayandtimerange(data) is False


@pytest.mark.asyncio
async def test_day_transition():
    data = {
        'now': datetime(2024, 6, 3, 23, 30, 0, tzinfo=timezone.utc),  # Monday
        'terms': {
            'start_day_of_week': 0,  # Sunday
            'start_time': '23:00:00',
            'end_day_of_week': 1,  # Monday
            'end_time': '01:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is True


@pytest.mark.asyncio
async def test_boundary_start_time():
    data = {
        'now': datetime(2024, 6, 4, 8, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
async def test_boundary_end_time():
    data = {
        'now': datetime(2024, 6, 4, 18, 0, 0, tzinfo=timezone.utc),  # Tuesday
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
async def test_outside_boundary_end_time():
    data = {
        'now': datetime(2024, 6, 4, 18, 0, 1, tzinfo=timezone.utc),  # Tuesday
        'terms': {
            'start_day_of_week': 1,
            'start_time': '08:00:00',
            'end_day_of_week': 1,
            'end_time': '18:00:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False

if __name__ == '__main__':
    pytest.main()
