from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    attrs = {}
    class_css, val = css.split(':')
    attrs[class_css] = val
    return field.as_widget(attrs=attrs)
