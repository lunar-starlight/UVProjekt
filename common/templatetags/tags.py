from django import template

register = template.Library()


@register.simple_tag
def icon(name, style, *args, **kwargs):
    if style not in ('s', 'solid', 'r', 'regular', 'l', 'light', 'd', 'duotone', 'b', 'brand'):
        style = 's'
    css_class = kwargs.get('class', '')

    return f'<i class="fa{style[0]} fa-{name} {css_class}"></i>'
