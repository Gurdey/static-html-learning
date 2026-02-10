from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
import re
from enum import Enum
import os
import shutil

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
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
            raise Exception("Incorrect TextType Enum")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception(f"Invalid markdown syntax: closing delimiter '{delimiter}' was not found.")
            for i in range(0, len(split_node)):
                if i % 2 == 0:
                    if len(split_node[i]) > 0:
                        new_nodes.append(TextNode(split_node[i], node.text_type))
                else:
                    if len(split_node[i]) > 0:
                        new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes

#Bold Italic and Code splitter.
def bic_splitter(nodes):
    bold_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    bold_italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    return split_nodes_delimiter(bold_italic_nodes, "`", TextType.CODE)

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            current_text = node.text
            images = extract_markdown_images(node.text)
            for image in images:
                seperator = f"![{image[0]}]({image[1]})"
                text_list = current_text.split(seperator, 1)
                if len(text_list[0]) > 0:
                    new_nodes.append(TextNode(text_list[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                current_text = text_list[1]
            if len(current_text) > 0:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            current_text = node.text
            links = extract_markdown_links(node.text)
            for link in links:
                seperator = f"[{link[0]}]({link[1]})"
                text_list = current_text.split(seperator, 1)
                if len(text_list[0]) > 0:
                    new_nodes.append(TextNode(text_list[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                current_text = text_list[1]
            if len(current_text) > 0:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

#Bold, Italic, Code, Image and Link splitter.
def full_splitter(nodes):
    new_nodes = bic_splitter(nodes)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    return full_splitter([node])

def markdown_to_blocks(markdown):
    block_list = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        block = block.strip()
        if len(block) < 1:
            continue
        elif block.startswith("\n"):
            block = block.removeprefix("\n")
            block = block.strip()
        block_list.append(block)
    return block_list

class BlockType(Enum):
    PARAGRAPH = "Generic fallback"
    HEADING = "1-6 #, space + heading text"
    CODE = "Starts with ```\n, ends with ```"
    QUOTE = "Every line starts with '> '"
    UNORDERED_LIST = "Every line starts with '- '"
    ORDERED_LIST = "Every line starts with a number+., incrementing by 1"

def block_to_block_type(block):
    lines = block.split("\n")
    #if block.startswith(("# ","## ","### ","#### ","##### ","###### "))
    if block[0] == "#":
        line = lines[0]
        counter = 0
        while line[counter] == "#" and counter < 6:
            counter += 1
            if line[counter] == " ":
                line = line[counter:].strip()
                if len(line) > 0:
                    return BlockType.HEADING
                else:
                    break
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        quote = True
        for line in lines:
            if not line.startswith(">"):
                quote = False
                break
        if quote == True:
            return BlockType.QUOTE
    if block.startswith("- "):
        unordered = True
        for line in lines:
            if not line.startswith("- "):
                unordered = False
                break
        if unordered == True:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        counter = 1
        #for line in lines:
        #   if not line.startswith(f"{counter}. "):
        #       return BlockType.PARAGRAPH
        #       counter += 1
        #return BlockType.ORDERED_LIST
        ordered = True
        for line in lines:
            if not line.startswith(f"{counter}. "):
                ordered = False
                break
            counter += 1
        if ordered == True:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def heading_to_heading_size(block):
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"
    
def list_block_to_html_nodes(block):
    parent_list_nodes = []
    split_block = block.split("\n")
    for line in split_block:
        parent_list_nodes.append(ParentNode("li", text_to_children(line)))
    return parent_list_nodes

def markdown_tag_remover(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return block.replace("\n", " ")
        case BlockType.HEADING:
            heading_size = heading_to_heading_size(block)
            if heading_size == "h1":
                return block[2:].replace("\n", " ")
            if heading_size == "h2":
                return block[3:].replace("\n", " ")
            if heading_size == "h3":
                return block[4:].replace("\n", " ")
            if heading_size == "h4":
                return block[5:].replace("\n", " ")
            if heading_size == "h5":
                return block[6:].replace("\n", " ")
            if heading_size == "h6":
                return block[7:].replace("\n", " ")
        case BlockType.CODE:
            return block[4:-4]
        case BlockType.QUOTE:
            block = block[2:]
            return block.replace("\n>", "")
        case BlockType.UNORDERED_LIST:
            finished_block = ""
            split_block = block.split("\n")
            for line in split_block:
                if len(finished_block) < 1:
                    finished_block = finished_block + line[2:]
                else:
                    finished_block = finished_block + "\n" + line[2:]
            return finished_block
        case BlockType.ORDERED_LIST:
            finished_block = ""
            split_block = block.split("\n")
            for line in split_block:
                if len(finished_block) < 1:
                    finished_block = finished_block + line[3:]
                else:
                    finished_block = finished_block + "\n" + line[3:]
            return finished_block

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_blocks.append(ParentNode("p", text_to_children(markdown_tag_remover(block))))
        
            case BlockType.HEADING:
                html_blocks.append(ParentNode(heading_to_heading_size(block), text_to_children(markdown_tag_remover(block))))

            case BlockType.CODE:
                html_blocks.append(ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(markdown_tag_remover(block), TextType.TEXT))])]))

            case BlockType.QUOTE:
                html_blocks.append(ParentNode("blockquote", text_to_children(markdown_tag_remover(block))))

            case BlockType.UNORDERED_LIST:
                html_blocks.append(ParentNode("ul", list_block_to_html_nodes(markdown_tag_remover(block))))

            case BlockType.ORDERED_LIST:
                html_blocks.append(ParentNode("ol", list_block_to_html_nodes(markdown_tag_remover(block))))
    return ParentNode("div", html_blocks)

def clear_public_directory(dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)

def copy_static_to_public(path="static/", target_dir="public/"):
    for file in os.listdir(path):
        current_file_path = os.path.join(path, file)
        if os.path.isfile(current_file_path):
            shutil.copy(current_file_path, target_dir)
        else:
            new_tar_dir = os.path.join(target_dir, file)
            os.mkdir(new_tar_dir)
            copy_static_to_public(current_file_path, new_tar_dir)

def extract_title(markdown):
    md_lines = markdown.split("\n")
    for line in md_lines:
        if line.startswith("# "):
            line = line[1:]
            return line.strip()
    raise Exception("No Title Found")

def make_dest_path(current_path, dest_path, template=None):
    if not os.path.exists(current_path):
        make_dest_path(os.path.dirname(current_path), dest_path)
        if current_path == dest_path:
            with open(current_path, 'w') as f:
                f.write(template)
        else:
            os.mkdir(current_path)
    else: 
        return


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    page_md = ""
    template = ""
    with open(from_path, 'r') as f:
        page_md = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    page_html = markdown_to_html_node(page_md).to_html()
    page_title = extract_title(page_md)
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", page_html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    if os.path.exists(dest_path):
        with open(dest_path, 'w') as f:
            f.write(template)
    else:
        make_dest_path(dest_path, dest_path, template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_dir = os.listdir(dir_path_content)
    for file in content_dir:
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, os.path.splitext(dest_path)[0]+".html", basepath)
        else:
            generate_pages_recursive(file_path, template_path, dest_path, basepath)

    