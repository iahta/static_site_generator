import re
from textnode import *

def split_nodes_delimiter (old_nodes, delimiter, text_type):
    new_list = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        
        nodes_string = node.text
        if delimiter not in nodes_string:
            new_list.append(node)
            continue
        if nodes_string.count(delimiter) < 2:
            raise ValueError(f"Invalid Markdown! No closing delimiter: {delimiter} ")   

        start = nodes_string.find(delimiter)  # finds first delimiter
        end = nodes_string.find(delimiter, start + len(delimiter))  # finds next delimiter after start

        if start != -1 and end != -1:
            before = nodes_string[:start]
            between = nodes_string[start+len(delimiter):end]
            after = nodes_string[end+len(delimiter):]

            if before:
                new_list.append(TextNode(before, node.text_type))
            new_list.append(TextNode(between, text_type))
            
            if delimiter in after:
                new_list.extend(split_nodes_delimiter([TextNode(after, node.text_type)], delimiter, text_type))
            else:
                if after:
                    new_list.append(TextNode(after, node.text_type))
    return new_list

"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
"""
"""         
    
            if nodes_string.find(delimiter) == -1:
                print("node is negative one")
            string_split = nodes_string.split(f"{delimiter}")
            new_list.append(TextNode(string_split[0], node.text_type, None))
            new_list.append(TextNode(string_split[1], text_type, None))
            new_list.append(TextNode(string_split[2], node.text_type, None))
            print(new_list)
an example, use the string split[0,1,3] to make TextNodex

"""

#extend(recursive function)
    
#new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)   

"""
should return
[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
"""


def extract_markdown_images(text):
    image = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    #capture = re.findall(r"(!\[(.*?)\]\((.*?)\))", text)
    return image


def extract_markdown_links(text):
    #link = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link




def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_list.append(node)
            continue
        for image in images:
            image_link = image[1]
            image_alt = image[0]
            text_split = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(text_split) != 2:
                raise ValueError("Invalid Markdown")
            if text_split[0] != "":
                new_list.append(TextNode(text_split[0], TextType.TEXT))
            new_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = text_split[1]
        if original_text != "":
            new_list.append(TextNode(original_text, TextType.TEXT))
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_list.append(node)
            continue
        for link in links:
            link_url = link[1]
            link_title = link[0]
            text_split = original_text.split(f"[{link_title}]({link_url})", 1)
            if len(text_split) != 2:
                raise ValueError("Invalid Markdown")
            if text_split[0] != "":
                new_list.append(TextNode(text_split[0], TextType.TEXT))
            new_list.append(TextNode(link_title, TextType.LINK, link_url))
            original_text = text_split[1]
        if original_text:
            new_list.append(TextNode(original_text, TextType.TEXT))
    return new_list


def text_to_textnodes(text):
    markdown_text = TextNode(text, TextType.TEXT)
    text_nodes = []
    bold = split_nodes_delimiter([markdown_text], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "*", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_image(code)
    link = split_nodes_link(image)
    return link





if __name__ == "__main__":
    #text = TextNode("This is a text with multiple ![link1](https://www.link1.com) or ![link2](www.bootlink2.com) and it has extra at the end", TextType.TEXT)
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )   
    print(split_nodes_link([node]))
    #print(split_nodes_image([text]))
    #print(split_nodes_image([text]))
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]