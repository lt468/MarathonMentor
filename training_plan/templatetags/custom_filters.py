from django import template

register = template.Library()

@register.filter
def format_timedelta(td):
    minutes, seconds = divmod(td.seconds, 60)
    return f"{minutes:02}:{seconds:02}"
