import datetime


async def evaluate_time_range_same_day(current_time, start_time, end_time):
    return start_time <= current_time <= end_time


def is_on_start_day_after_start_time(target_weekday, current_time, start_day, start_time):
    return target_weekday == start_day and current_time >= start_time


def is_on_end_day_before_end_time(target_weekday, current_time, end_day, end_time):
    return target_weekday == end_day and current_time <= end_time


def is_between_days(target_weekday, start_day, end_day):
    return start_day < target_weekday < end_day


def is_within_night_shift(target_weekday, current_time, start_day, start_time, end_day, end_time):
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


async def evaluate_time_range(current_datetime, start_day, start_time, end_day, end_time):
    time_ranges = generate_time_ranges(
        start_day, start_time, end_day, end_time)
    current_time = current_datetime

    print(f"Evaluating Time Range - current_datetime: {current_datetime}")

    for start_dt, end_dt in time_ranges:
        if start_dt <= current_time <= end_dt:
            return True

    return False


def generate_time_ranges(start_day, start_time, end_day, end_time):
    time_ranges = []

    # Check if start_time and end_time are already datetime.time objects
    if isinstance(start_time, str):
        start_time_dt = datetime.datetime.strptime(
            start_time, "%H:%M:%S").time()
    else:
        start_time_dt = start_time

    if isinstance(end_time, str):
        end_time_dt = datetime.datetime.strptime(end_time, "%H:%M:%S").time()
    else:
        end_time_dt = end_time

    # Calculate base date based on the current date
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
        time_ranges.append(create_range(
            base_date + datetime.timedelta(days=start_day), start_time_dt, end_time_dt))
    elif start_day < end_day:
        current_date = base_date + datetime.timedelta(days=start_day)
        while current_date.weekday() != end_day:
            time_ranges.append(create_range(
                current_date, start_time_dt, end_time_dt))
            current_date += datetime.timedelta(days=1)
        time_ranges.append(create_range(
            current_date, start_time_dt, end_time_dt))  # Add the last day
    else:  # start_day > end_day (crossing week boundary)
        current_date = base_date + datetime.timedelta(days=start_day - 7)
        while current_date.weekday() != end_day:
            time_ranges.append(create_range(
                current_date, start_time_dt, end_time_dt))
            current_date += datetime.timedelta(days=1)
        time_ranges.append(create_range(
            current_date, start_time_dt, end_time_dt))  # Add the last day

    # Debug log
    print("Generated time ranges:", time_ranges)

    return time_ranges


async def evaluate_dayandtimerange(data: dict, src=None):
    try:
        current_datetime = data.get(
            'now', datetime.datetime.now(datetime.timezone.utc))

        if src == 'logaction':
            not_operator = data.get('not_operator', False)
            start_day = data.get('start_day_of_week', -1)
            start_time = data.get('start_time', '-1:-1:-1')
            end_day = data.get('end_day_of_week', -1)
            end_time = data.get('end_time', '-1:-1:-1')

        elif src is None:
            terms = data.get('terms', {})
            condition = data.get('condition', {})
            not_operator = condition.get('not_operator', False)
            start_day = terms.get('start_day_of_week', -1)
            start_time = terms.get('start_time', '-1:-1:-1')
            end_day = terms.get('end_day_of_week', -1)
            end_time = terms.get('end_time', '-1:-1:-1')
        else:
            raise ValueError('invalid src')

        if start_day == -1 or end_day == -1 or '-1' in start_time or '-1' in end_time:
            raise ValueError('invalid parameters')

        # Debug prints to check types
        print(f"start_time before parsing: {
              start_time}, type: {type(start_time)}")
        print(f"end_time before parsing: {end_time}, type: {type(end_time)}")

        # Check if start_time and end_time are already datetime.time objects
        if not isinstance(start_time, datetime.time):
            start_time = datetime.datetime.strptime(
                start_time, "%H:%M:%S").time()
        if not isinstance(end_time, datetime.time):
            end_time = datetime.datetime.strptime(end_time, "%H:%M:%S").time()

        # Debug prints to check types after parsing
        print(f"start_time after parsing: {
              start_time}, type: {type(start_time)}")
        print(f"end_time after parsing: {end_time}, type: {type(end_time)}")

        time_ranges = generate_time_ranges(
            start_day, start_time, end_day, end_time)
        current_time_aware = current_datetime.replace(
            tzinfo=datetime.timezone.utc)

        for start_dt, end_dt in time_ranges:
            start_dt = start_dt.replace(tzinfo=datetime.timezone.utc)
            end_dt = end_dt.replace(tzinfo=datetime.timezone.utc)
            if start_dt <= current_time_aware <= end_dt:
                return not_operator ^ True

        return not_operator ^ False

    except Exception as err:
        print(str(err))
        return False
