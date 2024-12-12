from django import template

register = template.Library()

@register.filter
def truncate_chars(value, num):
    """Truncates a string after a certain number of characters."""
    try:
        num = int(num)
        print(num)
    except ValueError:
        return value  # Return the original value if `num` is invalid

    if len(value) > num:
        return value[:num-2] + ".."
    return value