import datetime


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

        # Adjust target_weekday to make Sunday 0
        target_weekday = (current_datetime.isoweekday() % 7)

        if target_weekday < start_day or target_weekday > end_day:
            return not_operator ^ False
        
        current_time = datetime.datetime.strptime(current_datetime.strftime("%H:%M"), "%H:%M").time()
        start_time = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
        end_time = datetime.datetime.strptime(end_time, "%H:%M:%S").time()

        # Check if the current time is within the valid time range
        if start_time <= end_time:
            # logger.info('Simple case: time range does not cross midnight')
            result = start_time <= current_time <= end_time
        else:
            # logger.info('Complex case: time range crosses midnight')
            result = current_time >= start_time or current_time <= end_time
        
        return not_operator ^ result
        
    except Exception as err:
        print(str(err))
        return False
