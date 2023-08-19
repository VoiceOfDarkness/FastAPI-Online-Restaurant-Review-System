from datetime import date, datetime


def json_datetime_serializer(obj):
    if isinstance(obj, (date, datetime)):
        return obj.strptime('%Y-%m-%dT%H:%M:%S.%f')
    raise TypeError('The type %s not serializable' %type(obj))
    