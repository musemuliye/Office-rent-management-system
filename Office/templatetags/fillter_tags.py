from django import template

register = template.Library()

@register.filter(name="count")
def count(queryset):
    print("count fillter")
    if queryset is None:
        return 0
    return queryset.count()