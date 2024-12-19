import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode
from htmlnode import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode("h1",
                         "This is the value inside of h1",
                            ["children: list of objects"], 
                           {"href": "www.href.com", "a": "a for awesome"},
                           )
        self.assertEqual(
            node.props_to_html(), ' href="www.href.com" a="a for awesome"'
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
            )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
        def test_toHTML(self):
            node = LeafNode("p", "This is a paragraph of text.")
            node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            self.assertEqual(
                 node.to_html(),
                 "<p>This is a paragraph of text.</p>",
            )
            self.assertEqual(
                 node2.to_html(),
                 '<a href="https://www.google.com">Click me!</a>',
            )

        def test_to_no_children(self):
             node = LeafNode("p", "Hello, world!")
             self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        def test_to_html_no_tag(self):
             node = LeafNode(None, "Hello, world!")
             self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
        def test_to_html(self):
            node = ParentNode(
                  "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )

            self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
         
            node2 = ParentNode(
                 "p",
                 [
                      LeafNode("h5", "Header to the Paragraph"),
                      ParentNode(
                           "p",
                           [
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                                ParentNode(
                                     "ol",
                                     [
                                          LeafNode("li", "this"),
                                          LeafNode("li", "is"),
                                          LeafNode("li", "a"),
                                          LeafNode("li", "list"),
                                     ])
                           ]
                           )
                 ]
            )
            
            self.assertEqual(node2.to_html(), "<p><h5>Header to the Paragraph</h5><p><i>italic text</i>Normal text<ol><li>this</li><li>is</li><li>a</li><li>list</li></ol></p></p>")
        
        
        def test_no_children(self):
             node = ParentNode("p", None)
             with self.assertRaises(ValueError):
                  node.to_html()
                 
        def test_no_tag(self):
             node = ParentNode(None, ["theres, no, tag"])
             with self.assertRaises(ValueError):
                  node.to_html()
      
class TestTextToHTML(unittest.TestCase):
     def test_text_node_to_html_node(self):
        node2 = TextNode("This is a text node", TextType.BOLD)
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node), LeafNode("b", "This is a text node"))



if __name__ == "__main__":
    unittest.main()