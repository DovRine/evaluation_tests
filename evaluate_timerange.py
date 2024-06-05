import datetime


async def evaluate_timerange(data: dict, src=None):
    try:
        current_datetime = data.get('now', datetime.datetime.now())

        if src == 'logaction':
            not_operator = data.get('not_operator', False)
            start = data.get('start', '')
            end = data.get('end', '')

        elif src is None:
            condition = data.get('condition', {})
            terms = data.get('terms', {})
            not_operator = condition.get('not_operator', False)
            start = terms.get('start', '')
            end = terms.get('end', '')

        else:
            raise ValueError('invalid src')

        current_time = datetime.datetime.strptime(
            current_datetime.strftime("%H:%M"), "%H:%M").time()
        start = datetime.datetime.strptime(start, "%H:%M:%S").time()
        end = datetime.datetime.strptime(end, "%H:%M:%S").time()

        # Check if the current time is within the valid time range
        if start <= end:
            result = start <= current_time <= end
        else:
            result = current_time >= start or current_time <= end

        return not_operator ^ result

    except Exception as err:
        print(str(err))
        return False
