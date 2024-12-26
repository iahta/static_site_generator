from htmlnode import *
from split_nodes import text_to_textnodes
import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"



def markdown_to_blocks(markdown):
    block_list = []
    markdown_copy = markdown
    split_list = markdown_copy.split("\n\n")
    for split in split_list:
        remove_blank = split.strip()
        if remove_blank != "":
            block_list.append(remove_blank)
    return block_list


def block_to_block_type(text_block):
    lines = text_block.split("\n")

    if text_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if text_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if text_block.startswith("* ") or text_block.startswith("- "):
        for line in lines:
            if not (line.startswith("* ") or line.startswith("- ")):
                return block_type_paragraph
        return block_type_unordered_list
    if text_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    return block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    node_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "paragraph":
            remove_blank = block.strip()
            children_list = text_to_children(remove_blank)
            node_list.append(HTMLNode("p", None, children_list))
        elif block_type == "heading":
            heading_level = len(block) - len(block.lstrip('#'))
            heading_text = block[heading_level:].strip()
            children_list = text_to_children(heading_text)
            node_list.append(HTMLNode(f"h{heading_level}", None, children_list))
        elif block_type == "quote":
            list_items = block.split("\n")
            list_of_list = []
            for item in list_items:
                remove_markdown = item.lstrip(">")
                remove_blank = remove_markdown.strip()
                if remove_blank:
                    list_of_list.append(remove_blank)
            complete_text = "\n".join(list_of_list)
            children_list = text_to_children(complete_text)
            node_list.append(HTMLNode("blockquote", None, children_list)) 
        elif block_type == "unordered list":
            list_items = block.split("\n")
            list_of_list = []
            for item in list_items:
                remove_markdown = item.lstrip("*")
                remove_blank = remove_markdown.strip()
                children_list = text_to_children(remove_blank)
                list_of_list.append(HTMLNode("li", None, children_list))
            node_list.append(HTMLNode("ul", None, list_of_list))
        elif block_type == "ordered list":
            list_items = block.split("\n")
            list_of_list = []
            for item in list_items:
                remove_markdown = re.sub(r"^\d+\.", "", item, count=1)
                remove_blank = remove_markdown.strip()
                children_list = text_to_children(remove_blank)
                list_of_list.append(HTMLNode("li", None, children_list))
            node_list.append(HTMLNode("ol", None, list_of_list))
        elif block_type == "code":
            start_strip = block.lstrip("```")
            end_strip = start_strip.rstrip("```")
            code_node = HTMLNode("code", end_strip, None)
            node_list.append(HTMLNode("pre", None, [code_node]))

    return HTMLNode("div", None, node_list)

def text_to_children(text):
    node_list = []
    text_nodes = text_to_textnodes(text)
    for text in text_nodes:
        new_node = text_node_to_html_node(text)
        node_list.append(new_node)
    return node_list


""" 
def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
"""



#if __name__ == "__main__":
