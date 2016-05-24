import json


def json_pprint(data):
    """
    Return the data as a string formatted json payload.

    :param object data:
    :return str: JSON encoded representation of the data.
    """
    print(json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    ))
