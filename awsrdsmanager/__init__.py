import json, decimal


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
        separators=(',', ': '),
        cls=CommonJSONEncoder
    ))


class CommonJSONEncoder(json.JSONEncoder):
    """
    Common JSON Encoder
    json.dumps(myString, cls=CommonJSONEncoder)
    """

    def default(self, obj):
        """
        Override the default JSON encode to allow the correct parsing of Decimal objects

        :param obj:
        :return:
        """
        if isinstance(obj, decimal.Decimal):
            return str(obj)
