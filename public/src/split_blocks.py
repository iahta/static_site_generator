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
    if text_block.startswith("*") or text_block.startswith("-"):
        for line in lines:
            if not (line.startswith("*") or line.startswith("-")):
                return block_type_paragraph
        return block_type_unordered_list


#if __name__ == "__main__":
#    block_to_block_type("``` This is a code block\n```")     