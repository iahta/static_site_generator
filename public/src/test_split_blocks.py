import unittest

from split_blocks import markdown_to_blocks, block_to_block_type


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

        text = "*An unrodered list\n-is unordered\n*and not ordered"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered list")


if __name__ == "__main__":
    unittest.main()