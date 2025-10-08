import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='convert_markdown')
@stringfilter
def convert_makrkdown(value):
    # fenced_code, tables 등 유용한 확장기능을 추가할 수 있습니다.
    return mark_safe(markdown.markdown(value, extensions=['fenced_code', 'tables']))