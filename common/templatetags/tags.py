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


# https://djangosnippets.org/snippets/2428/
class AddGetParameter(template.Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = template.Variable('request').resolve(context)
        params = req.GET.copy()
        for key, value in self.values.items():
            resolved = value.resolve(context)
            if resolved:
                params[key] = resolved
        return f'?{params.urlencode()}'


@register.tag
def add_get(parser, token):
    pairs = token.split_contents()[1:]
    values = {}
    for pair in pairs:
        s = pair.split('=', 1)
        values[s[0]] = parser.compile_filter(s[1])
    return AddGetParameter(values)
