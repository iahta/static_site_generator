import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("Text Node", TextType.ITALIC)
        node4 = TextNode("Text Node", TextType.ITALIC)
        node5 = TextNode("URL is none", TextType.CODE)
        node6 = TextNode("URL is none", TextType.CODE, "www.isnotnone.com")
        node7 = TextNode("This is not the same", TextType.LINK)
        node8 = TextNode("Not the same", TextType.IMAGE)
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertIsNone(node5.url)
        self.assertNotEqual(node7, node8)
        



    
if __name__ == "__main__":
    unittest.main()