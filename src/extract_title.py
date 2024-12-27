from split_blocks import markdown_to_blocks, markdown_to_html_node
from htmlnode import *
import os

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if blocks[0].startswith("# "):
        heading = blocks[0].strip("# ")
        heading_stripped = heading.strip()
        return heading_stripped
    raise Exception("Missing h1 heading")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


    with open(from_path) as markdown_file:
        read_markdown = markdown_file.read()
    
    with open(template_path) as template_file:
        read_template = template_file.read()


    html_nodes = markdown_to_html_node(read_markdown)
    html_string = html_nodes.to_html()
    title = extract_title(read_markdown)
    
    with_title = read_template.replace("{{ Title }}", title)
    add_content = with_title.replace("{{ Content }}", html_string)
    
    dir_path = os.path.dirname(dest_path)
    if dir_path:  # only try to create directories if there's actually a path
        os.makedirs(dir_path, exist_ok=True)
    with open(dest_path, 'w') as output_file:
        output_file.write(add_content)

