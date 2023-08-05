from functools import wraps

from bson.objectid import ObjectId

def filter2pymongo(filter):
    for k in filter.keys():
        value = filter[k]
        if isinstance(value, dict):
            if 'in' in value.keys():
                filter[k] = {'$in':value['in']}
            elif 'between' in value.keys():
                filter[k] = {"$gte": value['between'][0], "$lt": value['between'][1]}
    return filter

def format_filter(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        filter = {}
        if len(args) > 1:
            # print('filter in args', args[1])
            args = list(args)
            args[1] = filter2pymongo(args[1])
        if 'filter' in kwargs.keys():
            kwargs['filter'] = filter2pymongo(kwargs['filter'])
            # print('filter in kwargs', kwargs['filter'])
        return f(*args, **kwargs)
    return decorated