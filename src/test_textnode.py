import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_ineq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_ineq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_ineq3(self):
        node = TextNode("This is a text node", TextType.LINK, "Hello")
        node2 = TextNode("This is a text node", TextType.LINK, None)
        self.assertNotEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.LINK, "Hello")
        node2 = TextNode("This is a text node", TextType.LINK, "Hello")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()