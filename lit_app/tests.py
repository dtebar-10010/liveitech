from django.test import TestCase
from django.template import Template, Context


class StripOuterPFilterTests(TestCase):
	def test_strip_outer_p_removes_single_wrapper(self):
		tpl = Template("{% load strip_paragraphs %}{{ value|strip_outer_p }}")
		ctx = Context({"value": "<p>This is a subtitle</p>"})
		rendered = tpl.render(ctx).strip()
		self.assertEqual(rendered, "This is a subtitle")

	def test_strip_outer_p_leaves_inner_html(self):
		tpl = Template("{% load strip_paragraphs %}{{ value|strip_outer_p }}")
		ctx = Context({"value": "<p><strong>Bold</strong> and <em>em</em></p>"})
		rendered = tpl.render(ctx).strip()
		self.assertEqual(rendered, "<strong>Bold</strong> and <em>em</em>")

	def test_strip_outer_p_no_change_when_no_wrapper(self):
		tpl = Template("{% load strip_paragraphs %}{{ value|strip_outer_p }}")
		ctx = Context({"value": "Plain subtitle"})
		rendered = tpl.render(ctx).strip()
		self.assertEqual(rendered, "Plain subtitle")

# Create your tests here.
