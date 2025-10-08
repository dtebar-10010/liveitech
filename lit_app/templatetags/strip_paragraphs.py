from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(is_safe=True)
def strip_outer_p(value):
    """Remove a single outer <p>...</p> wrapper from the given HTML string.

    This is intentionally conservative: it only removes one exact outer
    <p>...</p> pair (optionally with attributes on the opening tag) and
    preserves the rest of the HTML unchanged.

    Use only for subtitle fields placed inside <h6> elements to avoid
    invalid HTML such as <h6><p>..</p></h6>.
    """
    if not value:
        return value

    # Regex to match an opening <p> or <div> (with optional attributes) and closing
    # tag wrapping the entire string. This handles the common CKEditor behavior of
    # wrapping inline content in a block-level tag. It's intentionally conservative
    # and only removes a single outer wrapper when it spans the whole value.
    pattern = r"^\s*<(p|div)(?:\s+[^>]*)?>([\s\S]*?)</\1>\s*$"
    m = re.match(pattern, str(value), flags=re.IGNORECASE)
    if m:
        # inner content is in group 2 when capturing the tag name
        inner = m.group(2)
        return mark_safe(inner)
    return mark_safe(value)
