def parse_amount(string_amount):
    """Convert string dollar amount to integer of cents"""
    sign = -1 if string_amount[0] == '-' else 1
    parts = list(map(int, string_amount.split('.')))

    if '.' not in string_amount:
        # No cents
        value = parts[0] * 100
    elif len(parts) == 1:
        # No dollars
        value = parts[0]
    elif len(parts) == 2:
        # Dollars and cents
        value = (parts[0] * 100) + parts[1]
    else:
        raise Exception("Amount {} is poorly formatted".format(string_amount))

    return value * sign


def dump_amount(cents, unit='$'):
    dollars_str = str(abs(cents))[:-2]
    cents_str = str(abs(cents))[-2:]
    sign = '-' if cents < 0 else ''

    return sign + unit + dollars_str + '.' + cents_str
