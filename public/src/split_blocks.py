

def markdown_to_blocks(markdown):
    block_list = []
    markdown_copy = markdown
    split_list = markdown_copy.split("\n")
    for split in split_list:
        remove_blank = split.strip()
        if remove_blank != "":
            block_list.append(remove_blank)
    return block_list



if __name__ == "__main__":
    text = "# This is a heading          \n\n\n\n\n\n\n\n\n\n\n\n              This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n* This is the first list item in a list block * This is a list item * This is another list item"
    print(markdown_to_blocks(text))
