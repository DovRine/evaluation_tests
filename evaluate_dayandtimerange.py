import datetime


async def evaluate_time_range_same_day(current_time, start_time, end_time):
    """
    Evaluates if the current_time is within the start_time and end_time on the same day.

    Args:
        current_time (datetime.time): The current time to evaluate.
        start_time (datetime.time): The start time of the range.
        end_time (datetime.time): The end time of the range.

    Returns:
        bool: True if current_time is within the range, else False.

    Examples:
        >>> import datetime
        >>> await evaluate_time_range_same_day(datetime.time(12, 0), datetime.time(9, 0), datetime.time(18, 0))
        True
        >>> await evaluate_time_range_same_day(datetime.time(20, 0), datetime.time(9, 0), datetime.time(18, 0))
        False
    """
    return start_time <= current_time <= end_time


def is_on_start_day_after_start_time(target_weekday, current_time, start_day, start_time):
    """
    Evaluates if the target_weekday is the same as the start_day and current_time is after start_time.

    Args:
        target_weekday (int): The current weekday (0-6, where 0 is Monday).
        current_time (datetime.time): The current time.
        start_day (int): The start day of the week (0-6, where 0 is Monday).
        start_time (datetime.time): The start time of the range.

    Returns:
        bool: True if on the start day and after start time, else False.

    Examples:
        >>> is_on_start_day_after_start_time(1, datetime.time(10, 0), 1, datetime.time(8, 0))
        True
        >>> is_on_start_day_after_start_time(1, datetime.time(7, 0), 1, datetime.time(8, 0))
        False
    """
    return target_weekday == start_day and current_time >= start_time


def is_on_end_day_before_end_time(target_weekday, current_time, end_day, end_time):
    """
    Evaluates if the target_weekday is the same as the end_day and current_time is before end_time.

    Args:
        target_weekday (int): The current weekday (0-6, where 0 is Monday).
        current_time (datetime.time): The current time.
        end_day (int): The end day of the week (0-6, where 0 is Monday).
        end_time (datetime.time): The end time of the range.

    Returns:
        bool: True if on the end day and before end time, else False.

    Examples:
        >>> is_on_end_day_before_end_time(1, datetime.time(10, 0), 1, datetime.time(12, 0))
        True
        >>> is_on_end_day_before_end_time(1, datetime.time(13, 0), 1, datetime.time(12, 0))
        False
    """
    return target_weekday == end_day and current_time <= end_time


def is_between_days(target_weekday, start_day, end_day):
    """
    Evaluates if the target_weekday is between the start_day and end_day.

    Args:
        target_weekday (int): The current weekday (0-6, where 0 is Monday).
        start_day (int): The start day of the week (0-6, where 0 is Monday).
        end_day (int): The end day of the week (0-6, where 0 is Monday).

    Returns:
        bool: True if the target weekday is between the start and end days, else False.

    Examples:
        >>> is_between_days(2, 1, 3)
        True
        >>> is_between_days(4, 1, 3)
        False
    """
    return start_day < target_weekday < end_day


def is_within_night_shift(target_weekday, current_time, start_day, start_time, end_day, end_time):
    """
    Evaluates if the current time and day are within a night shift spanning multiple days.

    Args:
        target_weekday (int): The current weekday (0-6, where 0 is Monday).
        current_time (datetime.time): The current time.
        start_day (int): The start day of the week (0-6, where 0 is Monday).
        start_time (datetime.time): The start time of the range.
        end_day (int): The end day of the week (0-6, where 0 is Monday).
        end_time (datetime.time): The end time of the range.

    Returns:
        bool: True if within the night shift range, else False.

    Examples:
        >>> is_within_night_shift(1, datetime.time(23, 0), 0, datetime.time(22, 0), 2, datetime.time(6, 0))
        True
        >>> is_within_night_shift(3, datetime.time(23, 0), 0, datetime.time(22, 0), 2, datetime.time(6, 0))
        False
    """
    if start_time > end_time:
        on_start_day_after_start_time = is_on_start_day_after_start_time(
            target_weekday, current_time, start_day, start_time)
        on_end_day_before_end_time = is_on_end_day_before_end_time(
            target_weekday, current_time, end_day, end_time)
        between_days_in_week = start_day < end_day and is_between_days(
            target_weekday, start_day, end_day)
        crossing_week_boundary = start_day > end_day and (
            (target_weekday > start_day or target_weekday <= end_day)
        )

        return on_start_day_after_start_time or on_end_day_before_end_time or between_days_in_week or crossing_week_boundary
    return False


def generate_time_ranges(start_day, start_time, end_day, end_time):
    """
    Generates a list of time ranges based on start and end days and times.

    Args:
        start_day (int): The start day of the week (0-6, where 0 is Monday).
        start_time (str): The start time in HH:MM:SS format.
        end_day (int): The end day of the week (0-6, where 0 is Monday).
        end_time (str): The end time in HH:MM:SS format.

    Returns:
        list of tuples: Each tuple contains the start and end datetime objects for the time ranges.

    Examples:
        >>> generate_time_ranges(0, '22:00:00', 2, '07:30:00')
        [(datetime.datetime(2024, 6, 2, 22, 0), datetime.datetime(2024, 6, 3, 7, 30)), ...]
    """
    time_ranges = []

    if isinstance(start_time, str):
        start_time = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
    if isinstance(end_time, str):
        end_time = datetime.datetime.strptime(end_time, "%H:%M:%S").time()

    today = datetime.datetime.today()
    current_weekday = today.weekday()
    base_date = today - datetime.timedelta(days=current_weekday)

    def create_range(current_date, start_time, end_time):
        start_dt = datetime.datetime.combine(current_date, start_time)
        if start_time <= end_time:
            end_dt = datetime.datetime.combine(current_date, end_time)
        else:
            end_dt = datetime.datetime.combine(
                current_date + datetime.timedelta(days=1), end_time)
        return (start_dt, end_dt)

    if start_day == end_day:
        current_date = base_date + datetime.timedelta(days=start_day)
        time_ranges.append(create_range(current_date, start_time, end_time))
    elif start_day < end_day:
        current_date = base_date + datetime.timedelta(days=start_day)
        while current_date.weekday() != end_day:
            time_ranges.append(create_range(
                current_date, start_time, end_time))
            current_date += datetime.timedelta(days=1)
        time_ranges.append(create_range(current_date, start_time, end_time))
    else:
        current_date = base_date + datetime.timedelta(days=start_day)
        while current_date.weekday() != end_day:
            time_ranges.append(create_range(
                current_date, start_time, end_time))
            current_date += datetime.timedelta(days=1)
        time_ranges.append(create_range(current_date, start_time, end_time))

    return time_ranges


async def evaluate_dayandtimerange(data):
    """
    Evaluates if the current date and time fall within the specified range in data.

    Args:
        data (dict): A dictionary containing:
            - 'now' (datetime): The current date and time.
            - 'terms' (dict): A dictionary with:
                - 'start_day_of_week' (int): Start day of the week (0-6, where 0 is Monday).
                - 'start_time' (str): Start time in HH:MM:SS format.
                - 'end_day_of_week' (int): End day of the week (0-6, where 0 is Monday).
                - 'end_time' (str): End time in HH:MM:SS format.
            - 'condition' (dict): A dictionary with optional 'not_operator' (bool).

    Returns:
        bool: True if the current date and time are within the range, else False.

    Examples:
        >>> data = {
        ...     'now': datetime.datetime(2024, 6, 4, 6, 0, 0, tzinfo=datetime.timezone.utc),
        ...     'terms': {
        ...         'start_day_of_week': 0,
        ...         'start_time': '22:00:00',
        ...         'end_day_of_week': 4,
        ...         'end_time': '07:30:00'
        ...     },
        ...     'condition': {}
        ... }
        >>> await evaluate_dayandtimerange(data)
        True
    """
    not_operator = False
    try:
        current_datetime = data['now']
        current_weekday = current_datetime.weekday()
        current_time = current_datetime.time()

        src = data.get('terms', data.get('condition', {}))

        start_day_of_week = src.get('start_day_of_week', -1)
        start_time = src.get('start_time', '-1:-1:-1')
        end_day_of_week = src.get('end_day_of_week', -1)
        end_time = src.get('end_time', '-1:-1:-1')
        not_operator = data.get('condition', {}).get('not_operator', False)

        if start_day_of_week == -1 or \
                start_time == '-1:-1:-1' or \
                end_day_of_week == -1 or \
                end_time == '-1:-1:-1':
            return not_operator ^ False

        if isinstance(start_time, str):
            start_time = datetime.datetime.strptime(
                start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.datetime.strptime(end_time, "%H:%M:%S").time()

        def is_within_time_range(start_time, end_time, current_time):
            if start_time <= end_time:
                return start_time <= current_time <= end_time
            else:
                return current_time >= start_time or current_time <= end_time

        # Explicit check for single-day ranges
        if start_day_of_week == end_day_of_week:
            if current_weekday == start_day_of_week:
                if is_within_time_range(start_time, end_time, current_time):
                    return not_operator ^ True

        if start_day_of_week <= end_day_of_week:
            if start_day_of_week <= current_weekday <= end_day_of_week:
                if is_within_time_range(start_time, end_time, current_time):
                    return not_operator ^ True
        else:
            # Adjust for cross-week evaluation
            current_weekday = (current_weekday + 1) % 7
            if current_weekday > start_day_of_week or current_weekday < end_day_of_week:
                if is_within_time_range(start_time, end_time, current_time):
                    return not_operator ^ True
            elif current_weekday == start_day_of_week:
                if current_time >= start_time:
                    return not_operator ^ True
            elif current_weekday == end_day_of_week:
                if current_time <= end_time:
                    return not_operator ^ True
            elif (current_weekday == (end_day_of_week + 1) % 7):
                if current_time <= end_time:
                    return not_operator ^ False

        return not_operator ^ False

    except Exception as e:
        print(f"Error in evaluate_dayandtimerange: {e}")
        return not_operator ^ False
