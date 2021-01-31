import json

def to_json(output_dict, human_readable=False):
    kwargs = {}
    if human_readable:
        kwargs['indent'] = 4
    else:
        kwargs['separators'] = (",", ":")

    return json.dumps(output_dict, **kwargs)

def from_json(input_string): # to dict
    pass
