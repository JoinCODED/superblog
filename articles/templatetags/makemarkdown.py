import markdown
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs
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
    return bleach.clean(markdown.markdown(value), markdown_tags, markdown_attrs)
