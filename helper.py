def float_check(value, value_name):
    error = ''
    if value == '':
        error = f'Missig input: {value_name}.'
        return value, error
    try:
        value = float(value)
    except:
        error = f'Please use a numeric {value_name}.'
        return value, error
    if value < 0:
        error = f'Please enter a positive {value_name}.'
        return value, error
    return value, error