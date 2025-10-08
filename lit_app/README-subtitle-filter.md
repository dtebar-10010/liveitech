Subtitle filter and CKEditor guidance
===================================

What was added
---------------

- A conservative template filter `strip_outer_p` in `lit_app/templatetags/strip_paragraphs.py`.
- This filter removes a single outer `<p>...</p>` wrapper from HTML content and returns the inner HTML marked safe.
- Templates rendering subtitle content inside `<h6>` were updated to pipe subtitle values through the filter, for example:

```django
<h6>{{ about.subtitle|strip_outer_p|safe }}</h6>
```

Why this was done
------------------

CKEditor or other WYSIWYG editors sometimes wrap simple content in a `<p>` element. That caused inconsistent rendering because the original stylesheet applied a left border only to `.head_title h6 p`.

The fix moves the border to `.head_title h6` in `static/css/style.css` and removes the inner `<p>` border rule. The filter ensures the resulting HTML in templates won't have invalid nesting like `<h6><p>...</p></h6>` and keeps the visual appearance consistent.

CKEditor recommendation
-----------------------

Prefer configuring CKEditor for subtitle fields so it doesn't produce block-level wrappers. Example CKEditor 4 configuration to reduce or prevent surrounding `<p>`:

```js
// Example: disable automatic <p> wrapper by using enterMode and forceSimpleAmpersand
CKEDITOR.replace('subtitleField', {
  enterMode: CKEDITOR.ENTER_BR, // pressing Enter inserts <br> instead of <p>
  shiftEnterMode: CKEDITOR.ENTER_P,
  // Alternatively, use allowedContent to restrict output to inline elements
  allowedContent: 'strong em b i; a[!href]; br; span{*}(*);',
  // If you're using a custom inline editor instance, consider using inline mode:
  // CKEDITOR.inline('subtitleField');
});
```

Notes
-----

- The filter is intentionally conservative: it only strips a single outer `<p>` (with optional attributes) and will not alter other HTML.
- The filter returns a safe string to match the existing templates which call `|safe`. Only use this filter with trusted content or when the content has already been sanitized.

If you'd like, I can add a small admin-side CKEditor profile specifically for subtitle fields so editors can't accidentally insert block content there.
