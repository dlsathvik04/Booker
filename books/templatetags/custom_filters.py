from django import template

register = template.Library()

@register.filter
def truncate_chars(value, num):
    """Truncates a string after a certain number of characters."""
    try:
        num = int(num)
    except ValueError:
        return value

    if len(value) > num:
        return value[:num-2] + ".."
    return value