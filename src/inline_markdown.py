from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_list.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        #print(f"Processing node: {node.text}")  # Debug print
        #print(f"Sections: {sections}")  # Debug print
        if len(sections) % 2 == 0:
            if sections[-1] == "":
                sections.pop()
            else:
                raise ValueError("that’s invalid Markdown syntax")
        for i in range(len(sections)):
            if sections[i] == "" and i == len(sections) - 1:
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        ret_list.extend(split_nodes)
    return ret_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    ret_list =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_list.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            ret_list.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                 ret_list.append(TextNode(sections[0], TextType.TEXT))
            ret_list.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            ret_list.append(TextNode(original_text, TextType.TEXT))
    return ret_list

def split_nodes_link(old_nodes):
    ret_list =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_list.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            ret_list.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                 ret_list.append(TextNode(sections[0], TextType.TEXT))
            ret_list.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            ret_list.append(TextNode(original_text, TextType.TEXT))
    return ret_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):  # Check if line starts with "# " (H1)
            return line[2:].strip()  # Remove "# " and return the rest
        
    raise ValueError("No H1 header found")

