def get_tag(tags, tag_name):
    tag = [tag.get('Value') for tag in tags if tag['Key'] == tag_name]
    return tag[0] if tag else 'Unknown'

def get_filters(**kwargs):
    result = []
    for k, v in kwargs.iteritems():
        result += [dict(Name=k, Value=v if type(v) == list else [v])]
    return result
