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
            raise Exception(f"Invalid Markdown! No closing delimiter: {delimiter} ")   

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

