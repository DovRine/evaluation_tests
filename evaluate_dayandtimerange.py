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


def generate_time_ranges(start_day, start_time, end_day, end_time):
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

        if start_day_of_week <= end_day_of_week:
            if start_day_of_week <= current_weekday <= end_day_of_week:
                if is_within_time_range(start_time, end_time, current_time):
                    return not_operator ^ True
        else:
            if current_weekday >= start_day_of_week or \
                    current_weekday <= end_day_of_week:
                if is_within_time_range(start_time, end_time, current_time):
                    return not_operator ^ True

        return not_operator ^ False

    except Exception as e:
        print(f"Error in evaluate_dayandtimerange: {e}")
        return not_operator ^ False
