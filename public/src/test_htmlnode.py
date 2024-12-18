import unittest

from htmlnode import HTMLNode, LeafNode


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

         
       

        """
        node2 = HTMLNode("p", "Paragraph", "No children", {"p": "paragraph", "d":"dinosuar"})
        test = HTMLNode.props_to_html(node)
        test2 = HTMLNode.props_to_html(node2)
        result = "href=www.href.com a=a for awesome "
        result2 = "p=paragraph d=dinosuar "
        
        self.assertEqual(test2, result2)
        self.assertEqual(HTMLNode.__repr__(node), ("h1", "This is the value inside of h1", ["list of objects"], {"href":"www.href.com", "a":"a for awesome"}))
"""

    #def test_props(self):
        
        

""" self.props_to_html(node)
        self.to_htmL(node)
        
        self.to_html(node2)
        self.props_to_html(node2)
        self.__repr__(node)
        self.__repr__(node2)
"""

if __name__ == "__main__":
    unittest.main()