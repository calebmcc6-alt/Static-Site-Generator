from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(markdown):
    if markdown[:2] == "# " or markdown[:3] == "## " or markdown[:4] == "### " or markdown[:5] == "#### " or markdown[:6] == "##### " or markdown[:7] == "###### ":
        return BlockType.HEADING
    if markdown[:4] == "```\n" and markdown[-3:] == "```":
        return BlockType.CODE
    split_markdown = markdown.split("\n")
    quote, unordered, ordered = True, True, True
    prev_ordered = 0
    for line in split_markdown:
        if line[0] != ">":
            quote = False
        if line[:2] != "- ":
            unordered = False
        if ordered:
            if line[:3] != f"{prev_ordered+1}. ":
                ordered = False
            else:
                prev_ordered += 1
    if quote:
        return BlockType.QUOTE
    if unordered:
        return BlockType.UNORDERED_LIST
    if ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH