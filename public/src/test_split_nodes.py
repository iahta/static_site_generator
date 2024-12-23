import unittest
from split_nodes import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        #node = TextNode("**bold**/**bold2**", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        #new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
        

    """
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("/", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
            ],
            new_nodes
        )  
    """

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    #EXTRACT IMAGES
    #def test_extract_images(self):
        #text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        #print(extract_markdown_images(text)) # 

    def test_extrac_images_multiple(self):
        text = "This is a text with multiple ![link1](https://www.link1.com) or ![link2](www.bootlink2.com)"
        new_text = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("link1", "https://www.link1.com"), ("link2", "www.bootlink2.com")
            ],
            new_text
        )


    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        new_links = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            new_links
        )


    def test_split_nodes_image(self):
    # Test with a single image
        node = TextNode("Check this image: ![cat](http://cat.com)", TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 2
        assert result[0].text == "Check this image: "
        assert result[1].text == "cat"
        assert result[1].url == "http://cat.com"

    # Test with no images
        node = TextNode("Just plain text here.", TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 1
        assert result[0].text == "Just plain text here."

        node = TextNode("Start ![one](http://one.com) middle ![two](http://two.com) end", TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 5
    # Add more assertions to verify each part
        node = TextNode("![first](http://first.com)![second](http://second.com)", TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 2
    # Add assertions


    def test_split_nodes_links(self):
        node = TextNode("These are not the links you're looking for", TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 1
        assert result[0].text == "These are not the links you're looking for"

        node = TextNode("We going back to back, [BACK](www.movieman.com),[BACK](www.backstage.net).", TextType.TEXT)
        result = split_nodes_link([node])
        text1 = "We going back to back, "
        text2 = "BACK"
        url2 = "www.movieman.com"
        text3 = ","
        text4 = "BACK"
        url4 = "www.backstage.net"
        text5 = "."
        assert len(result) == 5
        self.assertListEqual(
            [
                TextNode(text1, TextType.TEXT),
                TextNode(text2, TextType.LINK, url2),
                TextNode(text3, TextType.TEXT),
                TextNode(text4, TextType.LINK, url4),
                TextNode(text5, TextType.TEXT),
            ],
            result
        )
         
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result
        )
      

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        assert len(nodes) == 1
        assert nodes[0].text == ""
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[0].url == None


    def test_empty_delimiters(self):
    # Empty bold
        with self.assertRaises(ValueError):
            text_to_textnodes("**")
        

        nodes = text_to_textnodes("[]()") 
        assert len(nodes) == 1
        assert nodes[0].text == ""
        assert nodes[0].text_type == TextType.LINK
        assert nodes[0].url == "" 

    # Empty code block
        with self.assertRaises(ValueError):
            text_to_textnodes("`")

if __name__ == "__main__":
    unittest.main()