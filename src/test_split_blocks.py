import unittest

from split_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_blocks(self):
        text = "**This is** a test of Markdown.\n\n\n\n\n      We dont want *any* extra spacing.\n\n `this is code`\n"
        result = markdown_to_blocks(text)
        self.assertListEqual(
            [
                "**This is** a test of Markdown.",
                "We dont want *any* extra spacing.",
                "`this is code`",
            ],
            result
        )

    def test_markdown_blocks_blank_spaces(self):
        text = "* Testing Markdown\n\n         With Blank Spaces.\n"
        result = markdown_to_blocks(text)
        self.assertListEqual(
            [
                "* Testing Markdown",
                "With Blank Spaces.",
            ],
            result
        )

    def test_single_block_no_newlines(self):
        input_markdown = "# Just a single heading"
        expected_output = ["# Just a single heading"]
        result = markdown_to_blocks(input_markdown)
        assert result == expected_output, f"Expected {expected_output}, but got {result}"

    def test_block_paragraphs(self):
        text = "This is a paragraph\nthat spans multiple lines.\n\n Another paragraph here."
        result = markdown_to_blocks(text)
        self.assertListEqual(
            [
                "This is a paragraph\nthat spans multiple lines.",
                "Another paragraph here."
            ],
            result
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


    def test_block_to_block(self):
        text = "##### This is a list\n* with items"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")

        text = "```\nThis is a code block\n```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "code")

        text =">'This is a quote\n>every line\n>must have >"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "quote")

        text = "* An unrodered list\n- is unordered\n* and not ordered"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered list")

        text = "1. An ordered list\n2. has numbers\n3. and a period"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "ordered list")

    def test_markdown_to_html(self):
        test_markdown = """# My Cool Heading

This is a paragraph with **bold** and *italic* text.

* First item
* Second item with **bold**
* Third item with *italic*

1. Ordered first
2. Ordered second

> Here's a quote
> With multiple lines

```python
def hello():
    print("Hello World!")
```"""

# Try printing the output of your function:
        html_node = markdown_to_html_node(test_markdown)
        result = html_node.to_html()
        self.assertEqual(result, """<div><h1>My Cool Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i></li></ul><ol><li>Ordered first</li><li>Ordered second</li></ol><blockquote>Here's a quote
With multiple lines</blockquote><pre><code>python
def hello():
    print("Hello World!")
</code></pre></div>""" )


if __name__ == "__main__":
    unittest.main()