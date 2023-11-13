from django import template

"""
Django template filters for custom formatting.

This module defines custom template filters to format timedelta objects for display in templates.

Filters:
- `format_timedelta`: Formats a timedelta object as a string in the format MM:SS.

Usage:
1. Load the filters in your template:

    {% load custom_filters %}

2. Apply the `format_timedelta` filter to a timedelta object:

    {{ your_timedelta_object|format_timedelta }}

Example:
```python
# In a Django template
{% load custom_filters %}

{{ some_timedelta_object|format_timedelta }}

This example assumes that some_timedelta_object is a timedelta object, and the format_timedelta filter will
format it as a string in the MM:SS format.

Note:
This module needs to be loaded in your template using the {% load custom_filters %} tag before using the filters.
"""

register = template.Library()


@register.filter
def format_timedelta(td):
    minutes, seconds = divmod(td.seconds, 60)
    return f"{minutes:02}:{seconds:02}"
