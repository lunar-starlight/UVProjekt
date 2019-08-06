from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def icon(name, style, *args, **kwargs):
    if style not in ('s', 'solid', 'r', 'regular', 'l', 'light', 'd', 'duotone', 'b', 'brand'):
        style = 's'
    css_class = kwargs.get('class', '')

    return format_html('<i class="fa{} fa-{} {}"></i>', style[0], name, css_class)


@register.simple_tag
def is_friend(p1, p2):
    return p1.is_friend(p2)
