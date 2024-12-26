from textnode import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        if self.value is not None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
    
        if self.children is not None:
            children_html = []
            for child in self.children:
                child_html = child.to_html()
                children_html.append(child_html)
        
            inner_html = "".join(children_html)
        
        return f"<{self.tag}>{inner_html}</{self.tag}>"
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
           props_html += f' {prop}="{self.props[prop]}"'
        return props_html
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 
    
    def __eq__(self, other):
        return (
        self.tag == other.tag and
        self.value == other.value and
        self.props == other.props
        # include other attributes if necessary
    )
       
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("parent node must have tag")
        if self.children == None:
            raise ValueError("parent node must have children")
        children_concate = ""
        for child in self.children:
            children_concate += child.to_html()
        return f"<{self.tag}>{children_concate}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
