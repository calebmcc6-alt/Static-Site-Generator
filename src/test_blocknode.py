import unittest
from blocknode import BlockType, block_to_block_type
from helper import markdown_to_html_node

class TestBlockNode(unittest.TestCase):
    def test_par(self):
        text = "Hello"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    def test_head(self):
        text = "# Hello"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    def test_code(self):
        text = "```\nHello```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    def test_quote(self):
        text = ">Hello\n> hi"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    def test_ul(self):
        text = "- Hello\n- hi"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
    def test_ol(self):
        text = "1. Hello\n2. hi"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )