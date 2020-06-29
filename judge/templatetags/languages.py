import json
from os import path

from ruamel import yaml

from django import template


register = template.Library()

@register.simple_tag
def get_language_by_json(string):
    obj = json.loads(string)
    if 'processor' not in obj:
        return None
    if 'language' in obj:
        return yaml.load(
            open(path.join(path.dirname(__file__), '../processors.yaml')),
            Loader=yaml.Loader
        )[obj['processor']]['language'][obj['language']]
    return obj['processor']
