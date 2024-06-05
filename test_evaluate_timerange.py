import datetime
import pytest
from evaluate_timerange import evaluate_timerange


@pytest.mark.asyncio
async def test_within_time_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 10, 30),
        'start': '10:00:00',
        'end': '11:00:00'
    }
    src = 'logaction'
    expected = True
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_outside_time_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 9, 30),
        'start': '10:00:00',
        'end': '11:00:00'
    }
    src = 'logaction'
    expected = False
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_not_operator_within_time_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 10, 30),
        'not_operator': True,
        'start': '10:00:00',
        'end': '11:00:00'
    }
    src = 'logaction'
    expected = False
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_wrap_around_midnight_within_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 0, 30),
        'start': '23:00:00',
        'end': '01:00:00'
    }
    src = 'logaction'
    expected = True
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_wrap_around_midnight_outside_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 2, 30),
        'start': '23:00:00',
        'end': '01:00:00'
    }
    src = 'logaction'
    expected = False
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_default_src_within_time_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 10, 30),
        'condition': {'not_operator': False},
        'terms': {'start': '10:00:00', 'end': '11:00:00'}
    }
    src = None
    expected = True
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_default_src_outside_time_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 9, 30),
        'condition': {'not_operator': False},
        'terms': {'start': '10:00:00', 'end': '11:00:00'}
    }
    src = None
    expected = False
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_wrap_around_midnight_default_src_within_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 0, 30),
        'condition': {'not_operator': False},
        'terms': {'start': '23:00:00', 'end': '01:00:00'}
    }
    src = None
    expected = True
    result = await evaluate_timerange(data, src)
    assert result == expected


@pytest.mark.asyncio
async def test_wrap_around_midnight_default_src_outside_range():
    data = {
        'now': datetime.datetime(2024, 6, 4, 2, 30),
        'condition': {'not_operator': False},
        'terms': {'start': '23:00:00', 'end': '01:00:00'}
    }
    src = None
    expected = False
    result = await evaluate_timerange(data, src)
    assert result == expected
