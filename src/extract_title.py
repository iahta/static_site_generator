from split_blocks import markdown_to_blocks, markdown_to_html_node
from htmlnode import *
import os
from pathlib import Path

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")
    content_directory = os.listdir(dir_path_content)
    with open(template_path) as template_file:
        read_template = template_file.read()

    for content in content_directory:
        new_path = os.path.join(dir_path_content, content)
        dest_new_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(new_path):
            with open(new_path) as markdown_file:
                read_markdown = markdown_file.read()

            html_nodes = markdown_to_html_node(read_markdown)
            html_string = html_nodes.to_html()
            title = extract_title(read_markdown)

            with_title = read_template.replace("{{ Title }}", title)
            add_content = with_title.replace("{{ Content }}", html_string)

            dir_path = os.path.dirname(dest_new_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok = True)
            with open(dest_new_path, 'w') as output_file:
                output_file.write(add_content)
                
        if os.path.isdir(new_path):
            generate_pages_recursive(new_path, template_path, dest_new_path)

        #use this to add the new found dir to the new path full_path = os.path.join(base_dir, filename)
