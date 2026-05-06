from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from blocknode import BlockType, block_to_block_type
import re

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception()
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
    return

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text.count(delimiter) % 2 == 1:
                raise Exception()
            split_node = node.text.split(delimiter)
            for index, s_node in enumerate(split_node):
                if s_node != "":
                    if index % 2 == 0:
                        node_list.append(TextNode(s_node, TextType.TEXT))
                    else:
                        node_list.append(TextNode(s_node, text_type))
        else:
            node_list.append(node)
    return node_list

def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            index = 0
            for image in images:
                image_markdown = f"![{image[0]}]({image[1]})"
                image_index = node.text.find(image_markdown, index)
                if node.text[index:image_index] != "":
                    node_list.append(TextNode(node.text[index:image_index], TextType.TEXT))
                node_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
                index = image_index + len(image_markdown)
            else:
                if node.text[index:] != "":
                    node_list.append(TextNode(node.text[index:], TextType.TEXT))
        else:
            node_list.append(node)
    return node_list

def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            index = 0
            for link in links:
                link_markdown = f"[{link[0]}]({link[1]})"
                link_index = node.text.find(link_markdown, index)
                if node.text[index:link_index] != "":
                    node_list.append(TextNode(node.text[index:link_index], TextType.TEXT))
                node_list.append(TextNode(link[0], TextType.LINK, link[1]))
                index = link_index + len(link_markdown)
            else:
                if node.text[index:] != "":
                    node_list.append(TextNode(node.text[index:], TextType.TEXT))
        else:
            node_list.append(node)
    return node_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnode(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block != "":
            if new_block.startswith("```") and new_block.endswith("```"):
                lines = new_block.split("\n")
                closing_indent = len(lines[-1]) - len(lines[-1].lstrip())
                if closing_indent > 0:
                    for i in range(1, len(lines)):
                        if lines[i].startswith(" " * closing_indent):
                            lines[i] = lines[i][closing_indent:]
                    new_block = "\n".join(lines)
                clean_blocks.append(new_block)
                continue
            lines = new_block.split("\n")
            clean_block = ""
            for line in lines:
                clean_block += line.strip() +"\n"
            else:
                clean_block = clean_block[:-1]
            clean_blocks.append(clean_block)
    return clean_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes = []
        if block_type == BlockType.PARAGRAPH:
            new_block = block.replace("\n", " ")
            text_nodes = text_to_textnode(new_block)
            for text_node in text_nodes:
                child_nodes.append(text_node_to_html_node(text_node))
            block_nodes.append(ParentNode("p", child_nodes))
        elif block_type == BlockType.HEADING:
            heading = 0
            if block[:2] == "# ":
                heading = 1
                block = block[2:]
            elif block[:3] == "## ":
                heading = 2
                block = block[3:]
            elif block[:4] == "### ":
                heading = 3
                block = block[4:]
            elif block[:5] == "#### ":
                heading = 4
                block = block[5:]
            elif block[:6] == "##### ":
                heading = 5
                block = block[6:]
            elif block[:7] == "###### ":
                heading = 6
                block = block[7:]
            text_nodes = text_to_textnode(block)
            for text_node in text_nodes:
                child_nodes.append(text_node_to_html_node(text_node))
            block_nodes.append(ParentNode(f"h{heading}", child_nodes))
        elif block_type == BlockType.CODE:
            block = block[4:-3]
            text_nodes = [TextNode(block, TextType.TEXT)]
            for text_node in text_nodes:
                child_nodes.append(text_node_to_html_node(text_node))
            code_node = ParentNode("code", child_nodes)
            block_nodes.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            block_splits = block.split("\n")
            block = ""
            for block_split in block_splits:
                block += block_split[1:].strip() + "\n"
            text_nodes = text_to_textnode(block)
            for text_node in text_nodes:
                child_nodes.append(text_node_to_html_node(text_node))
            block_nodes.append(ParentNode("blockquote", child_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            middle_nodes = []
            block_splits = block.split("\n")
            for block_split in block_splits:
                curr_split = block_split[2:].strip()
                text_nodes = text_to_textnode(curr_split)
                child_nodes = []
                for text_node in text_nodes:
                    child_nodes.append(text_node_to_html_node(text_node))
                middle_nodes.append(ParentNode("li", child_nodes))
            block_nodes.append(ParentNode("ul", middle_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            middle_nodes = []
            block_splits = block.split("\n")
            for block_split in block_splits:
                curr_split = block_split[3:].strip()
                text_nodes = text_to_textnode(curr_split)
                child_nodes = []
                for text_node in text_nodes:
                    child_nodes.append(text_node_to_html_node(text_node))
                middle_nodes.append(ParentNode("li", child_nodes))
            block_nodes.append(ParentNode("ol", middle_nodes))
    return ParentNode("div", block_nodes)
