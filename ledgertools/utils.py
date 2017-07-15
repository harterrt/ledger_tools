from decimal import Decimal


def parse_amount(string_amount):
    """Convert string dollar amount to integer of cents"""
    return Decimal(string_amount)


def dump_amount(decimal, unit='$'):
    return unit + str(decimal)
