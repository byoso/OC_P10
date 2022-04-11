"""Here are some helpers
"""


def check_type(value, a_type):
    """Takes 2 parameters : a value and a type (bool, int or float)
    check_type returns a boolean.
    check_type does NOT convert the value of the input.
    """
    if a_type == bool:
        if value.lower() in ["true", "false"]:
            return True
        else:
            return False
    else:
        try:
            a_type(value)
        except ValueError:
            return False
        return True


def expected_values(data, *args):
    """To be used in the serializers 'validate' method.
    Check if a set of data given by the client is
    matching the expected values.
    Args:
    - data : data from a form-data (from the client)
    - args : a list of tuples.
        tuples are made like that:
        ([name (str)], a lambda (optionnal) )
        the function takes the data as argument, and
        returns a boolean.

    ex: [('age', lambda x: check_type(x, int) and x >= 0),]
    """
    valid = True
    for arg in args:
        if arg[0] in data:
            if len(arg) > 1:
                valid *= arg[1](data[arg[0]])

    return bool(valid)
