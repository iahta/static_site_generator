import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode




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
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag is None
        assert html_node.value == "Hello, world!"
  
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "b"
        assert html_node.value == "Bold text"
    
    # Continue with other types...
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "i"
        assert html_node.value == "Italic text"
        
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "code"
        assert html_node.value == "Code text"
        
        text_node = TextNode("Link", TextType.LINK)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "a"
        assert html_node.value == "Link"
        assert html_node.props == {"href": text_node.url}

        text_node = TextNode("Image", TextType.IMAGE)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "img"
        assert html_node.value == ""
        assert html_node.props == {"src": text_node.url, "alt": text_node.text}
    
        
        invalid_node = TextNode("test", None)
        try:
            text_node_to_html_node(invalid_node)
            assert False, "Expected ValueError"
        except ValueError as e:
            assert str(e) == f"Invalid text type: {None}"

if __name__ == "__main__":
    unittest.main()