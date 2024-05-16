from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """Фильтрация пути к изображению"""
    if path:
        return f"/media/{path}"
    else:
        return "#"
