import datetime


async def evaluate_time_range_same_day(current_time, start_time, end_time):
    return start_time <= current_time <= end_time


async def evaluate_time_range_multiple_days(current_datetime, start_day, start_time, end_day, end_time):
    target_weekday = (current_datetime.weekday() + 1) % 7
    current_time = current_datetime.time()

    if start_day < end_day:
        is_after_start_day = target_weekday > start_day
        is_on_start_day_after_start_time = target_weekday == start_day and current_time >= start_time
        is_before_end_day = target_weekday < end_day
        is_on_end_day_before_end_time = target_weekday == end_day and (
            (current_time <= end_time and end_time > start_time) or
            (end_time < start_time and (current_time <=
             end_time or current_time >= start_time))
        )

        return (is_after_start_day or is_on_start_day_after_start_time) and \
               (is_before_end_day or is_on_end_day_before_end_time)
    else:  # Range crosses the week boundary
        is_on_start_day_after_start_time = target_weekday == start_day and current_time >= start_time
        is_on_end_day_before_end_time = target_weekday == end_day and (
            (current_time <= end_time and end_time > start_time) or
            (end_time < start_time and (current_time <=
             end_time or current_time >= start_time))
        )
        is_between_days = target_weekday >= start_day or target_weekday <= end_day

        return is_on_start_day_after_start_time or is_on_end_day_before_end_time or is_between_days


async def evaluate_dayandtimerange(data: dict, src=None):
    try:
        current_datetime = data.get('now', datetime.datetime.now())

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

        if start_day == -1:
            raise ValueError('invalid start day')
        if end_day == -1:
            raise ValueError('invalid end day')
        if '-1' in end_time:
            raise ValueError('invalid end time')
        if '-1' in start_time:
            raise ValueError('invalid start time')

        # Convert times to time objects
        current_time = current_datetime.time()
        start_time = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
        end_time = datetime.datetime.strptime(end_time, "%H:%M:%S").time()

        if start_day == end_day:
            result = await evaluate_time_range_same_day(current_time, start_time, end_time)
        else:
            result = await evaluate_time_range_multiple_days(current_datetime, start_day, start_time, end_day, end_time)

        return not_operator ^ result

    except Exception as err:
        print(str(err))
        return False
