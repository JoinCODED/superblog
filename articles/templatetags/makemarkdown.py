import markdown
from django import template
from django.template.defaultfilters import stringfilter
from markdown.extensions.codehilite import CodeHiliteExtension

register = template.Library()
extension_list = [
    'markdown.extensions.attr_list'
]


@register.filter
@stringfilter
def makemarkdown(value):
    return markdown.markdown(value, extensions=extension_list)
