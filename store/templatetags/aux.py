import re
from urllib.parse import unquote
from django.template.defaultfilters import stringfilter, register

SEARCH_PATTERN = re.compile(".*?search=(.*)")

@register.filter
@stringfilter
def extract_keywords(uri):
    return re.search(SEARCH_PATTERN, unquote(uri)).group(1)

@register.filter
def names(lst):
    return ", ".join(d["name"] for d in lst)

@register.filter
def div(dividend, divisor):
    return dividend // divisor + (dividend % divisor > 0)
