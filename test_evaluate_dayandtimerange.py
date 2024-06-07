from datetime import datetime, timezone, timedelta
import pytest

from evaluate_dayandtimerange import evaluate_dayandtimerange, generate_time_ranges

################### generate_time_ranges ###################


def test_generate_time_ranges_same_day():
    # Single day range
    start_day = 2  # Tuesday
    start_time = '08:00:00'
    end_day = 2  # Tuesday
    end_time = '18:00:00'
    time_ranges = generate_time_ranges(
        start_day, start_time, end_day, end_time)

    assert len(time_ranges) == 1
    start_dt, end_dt = time_ranges[0]
    assert start_dt.time() == datetime.strptime(start_time, "%H:%M:%S").time()
    assert end_dt.time() == datetime.strptime(end_time, "%H:%M:%S").time()
    assert start_dt.date() == end_dt.date()


def test_generate_time_ranges_multiple_days():
    # Multi-day range
    start_day = 0  # Sunday
    start_time = '22:00:00'
    end_day = 2  # Tuesday
    end_time = '07:30:00'
    time_ranges = generate_time_ranges(
        start_day, start_time, end_day, end_time)

    assert len(time_ranges) == 3
    for i, (start_dt, end_dt) in enumerate(time_ranges):
        print("Start Date:", start_dt.date())
        print("End Date:", end_dt.date())
        assert start_dt.time() == datetime.strptime(start_time, "%H:%M:%S").time()
        assert end_dt.time() == datetime.strptime(end_time, "%H:%M:%S").time()
        assert start_dt.date() != end_dt.date() or start_dt.time() != end_dt.time()


def test_generate_time_ranges_crossing_midnight():
    # Range crossing midnight
    start_day = 5  # Friday
    start_time = '23:00:00'
    end_day = 6  # Saturday
    end_time = '01:00:00'
    time_ranges = generate_time_ranges(
        start_day, start_time, end_day, end_time)

    assert len(time_ranges) == 2
    for start_dt, end_dt in time_ranges:
        if start_dt.date() == end_dt.date():
            assert start_dt.time() == datetime.strptime(start_time, "%H:%M:%S").time()
            assert end_dt.time() == datetime.strptime(end_time, "%H:%M:%S").time()
        else:
            assert start_dt.time() == datetime.strptime(start_time, "%H:%M:%S").time()
            assert end_dt.time() == datetime.strptime(end_time, "%H:%M:%S").time()
            assert end_dt.date() == start_dt.date() + timedelta(days=1)


def test_generate_time_ranges_crossing_week_boundary():
    # Range crossing week boundary
    start_day = 6  # Saturday
    start_time = '22:00:00'
    end_day = 1  # Monday
    end_time = '07:30:00'
    time_ranges = generate_time_ranges(
        start_day, start_time, end_day, end_time)

    assert len(time_ranges) == 3
    for i, (start_dt, end_dt) in enumerate(time_ranges):
        assert start_dt.time() == datetime.strptime(start_time, "%H:%M:%S").time()
        assert end_dt.time() == datetime.strptime(end_time, "%H:%M:%S").time()
        assert start_dt.date() != end_dt.date()  # Updated assertion

# ################### EVALUATE_DAYANDTIMERANGE ###################


@pytest.mark.asyncio
async def test_within_valid_time_range():
    data = {
        'now': datetime(2024, 6, 4, 6, 0, 0, tzinfo=timezone.utc),  # Tuesday
        'terms': {
            'start_day_of_week': 0,  # Sunday
            'start_time': '22:00:00',
            'end_day_of_week': 4,  # Thursday
            'end_time': '07:30:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is True


@pytest.mark.asyncio
async def test_outside_valid_time_range():
    data = {
        'now': datetime(2024, 6, 4, 8, 0, 0, tzinfo=timezone.utc),  # Tuesday
        'terms': {
            'start_day_of_week': 0,  # Sunday
            'start_time': '22:00:00',
            'end_day_of_week': 4,  # Thursday
            'end_time': '07:30:00'
        },
        'condition': {}
    }
    assert await evaluate_dayandtimerange(data) is False


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
