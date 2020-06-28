from django import template
from django.template.defaultfilters import stringfilter

import readme_renderer.markdown
import readme_renderer.rst


register = template.Library()


@register.filter
@stringfilter
def markdown(value):
    return readme_renderer.markdown.render(value)


@register.filter
@stringfilter
def rst(value):
    return readme_renderer.rst.render(value)
