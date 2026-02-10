import unittest
from textnode import TextNode, TextType

from functions import (
    text_node_to_html_node, 
    bic_splitter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    full_splitter, 
    text_to_textnodes, 
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title,
)

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "image.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.url", "alt": "This is an image"})
        
    def test_bold_split(self):
        node = TextNode("This has **bold** text.", TextType.TEXT)
        split_node = bic_splitter([node])
        self.assertEqual(split_node[0].text, "This has ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "bold")
        self.assertEqual(split_node[1].text_type, TextType.BOLD)
        self.assertEqual(split_node[2].text, " text.")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)

    def test_italic_split(self):
        node = TextNode("This has _italic_ text.", TextType.TEXT)
        split_node = bic_splitter([node])
        self.assertEqual(split_node[0].text, "This has ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "italic")
        self.assertEqual(split_node[1].text_type, TextType.ITALIC)
        self.assertEqual(split_node[2].text, " text.")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)

    def test_code_split(self):
        node = TextNode("This has `code` text.", TextType.TEXT)
        split_node = bic_splitter([node])
        self.assertEqual(split_node[0].text, "This has ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "code")
        self.assertEqual(split_node[1].text_type, TextType.CODE)
        self.assertEqual(split_node[2].text, " text.")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)

    def test_multiple_split(self):
        node = TextNode("This has _italic_, **bold**, `code`, and more **bold** text.", TextType.TEXT)
        split_node = bic_splitter([node])
        self.assertEqual(split_node[0].text, "This has ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "italic")
        self.assertEqual(split_node[1].text_type, TextType.ITALIC)
        self.assertEqual(split_node[2].text, ", ")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[3].text, "bold")
        self.assertEqual(split_node[3].text_type, TextType.BOLD)
        self.assertEqual(split_node[4].text, ", ")
        self.assertEqual(split_node[4].text_type, TextType.TEXT)
        self.assertEqual(split_node[5].text, "code")
        self.assertEqual(split_node[5].text_type, TextType.CODE)
        self.assertEqual(split_node[6].text, ", and more ")
        self.assertEqual(split_node[6].text_type, TextType.TEXT)
        self.assertEqual(split_node[7].text, "bold")
        self.assertEqual(split_node[7].text_type, TextType.BOLD)
        self.assertEqual(split_node[8].text, " text.")
        self.assertEqual(split_node[8].text_type, TextType.TEXT)

    def test_multiple_node_split(self):
        node = TextNode("This has **bold** text.", TextType.TEXT)
        node_2 = TextNode("This has _italic_ text.", TextType.TEXT)
        node_3 = TextNode("This has `code` text.", TextType.TEXT)
        nodes = [node, node_2, node_3]
        split_nodes = bic_splitter(nodes)
        self.assertEqual(split_nodes[0].text, "This has ")
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[1].text, "bold")
        self.assertEqual(split_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[2].text, " text.")
        self.assertEqual(split_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[3].text, "This has ")
        self.assertEqual(split_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[4].text, "italic")
        self.assertEqual(split_nodes[4].text_type, TextType.ITALIC)
        self.assertEqual(split_nodes[5].text, " text.")
        self.assertEqual(split_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[6].text, "This has ")
        self.assertEqual(split_nodes[6].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[7].text, "code")
        self.assertEqual(split_nodes[7].text_type, TextType.CODE)
        self.assertEqual(split_nodes[8].text, " text.")
        self.assertEqual(split_nodes[8].text_type, TextType.TEXT)

    def test_empty_string_split(self):
        node = TextNode("This has **bold,**_italic,_`and code` text.", TextType.TEXT)
        split_node = bic_splitter([node])
        self.assertEqual(split_node[0].text, "This has ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "bold,")
        self.assertEqual(split_node[1].text_type, TextType.BOLD)
        self.assertEqual(split_node[2].text, "italic,")
        self.assertEqual(split_node[2].text_type, TextType.ITALIC)
        self.assertEqual(split_node[3].text, "and code")
        self.assertEqual(split_node[3].text_type, TextType.CODE)
        self.assertEqual(split_node[4].text, " text.")
        self.assertEqual(split_node[4].text_type, TextType.TEXT)

    def test_image_collect(self):
        text = "This is text with an image ![Look at this!](wow/some.text) in it."
        result = extract_markdown_images(text)
        self.assertEqual(result[0][0], "Look at this!")
        self.assertEqual(result[0][1], "wow/some.text")

    def test_multiple_image_collect(self):
        text = "Multiple images ![Look at this!](wow/some.text), and ![Another one.](my/image.folder) here."
        result = extract_markdown_images(text)
        self.assertEqual(result[0][0], "Look at this!")
        self.assertEqual(result[0][1], "wow/some.text")
        self.assertEqual(result[1][0], "Another one.")
        self.assertEqual(result[1][1], "my/image.folder")

    def test_link_collect(self):
        text = "This is text with a link [Link 1](https://www.thisisalink.com) in it."
        result = extract_markdown_links(text)
        self.assertListEqual(result, [("Link 1", "https://www.thisisalink.com")])

    def test_multiple_link_collect(self):
        text = "This is text with two links [Link 1](https://www.thisisalink.com) [Link 2](https://www.thisisanotherlink.com) in it."
        result = extract_markdown_links(text)
        self.assertListEqual(result, [("Link 1", "https://www.thisisalink.com"), ("Link 2", "https://www.thisisanotherlink.com")])

    def test_link_image_collect(self):
        text = "This is text with two images and a link ![Look at this!](wow/some.text), [Link 1](https://www.thisisalink.com), ![Another one.](my/image.folder), in it."
        image_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        self.assertListEqual(image_result, [("Look at this!", "wow/some.text"), ("Another one.", "my/image.folder")])
        self.assertListEqual(link_result, [("Link 1", "https://www.thisisalink.com")])

    def test_image_split(self):
        node = TextNode("This is text with an image ![Look at this!](wow/some.text) in it.", TextType.TEXT)
        split_node = split_nodes_image([node])
        self.assertEqual(split_node[0].text, "This is text with an image ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "Look at this!")
        self.assertEqual(split_node[1].text_type, TextType.IMAGE)
        self.assertEqual(split_node[1].url, "wow/some.text")
        self.assertEqual(split_node[2].text, " in it.")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)

    def test_link_split(self):
        node = TextNode("This is text with a link [Link 1](https://www.thisisalink.com) in it.", TextType.TEXT)
        split_node = split_nodes_link([node])
        self.assertEqual(split_node[0], TextNode("This is text with a link ", TextType.TEXT))
        self.assertEqual(split_node[1], TextNode("Link 1", TextType.LINK, "https://www.thisisalink.com"))
        self.assertEqual(split_node[2], TextNode(" in it.", TextType.TEXT))

    def test_no_space_link_image(self):
        node = TextNode("![Image](ImageLink)", TextType.TEXT)
        node2 = TextNode("[Link](LinkLink)", TextType.TEXT)
        node_list = [node, node2]
        node_list = split_nodes_image(node_list)
        node_list = split_nodes_link(node_list)
        self.assertEqual(node_list[0], TextNode("Image", TextType.IMAGE, "ImageLink"))
        self.assertEqual(node_list[1], TextNode("Link", TextType.LINK, "LinkLink"))

    def test_full_splitter(self):
        node = TextNode("_This_`is`**a**`test`![of](the)_full_[splitter](in)**action**[multi](link)`included`", TextType.TEXT)
        split_node = full_splitter([node])
        self.assertEqual(split_node[0], TextNode("This", TextType.ITALIC))
        self.assertEqual(split_node[1], TextNode("is", TextType.CODE))
        self.assertEqual(split_node[2], TextNode("a", TextType.BOLD))
        self.assertEqual(split_node[3], TextNode("test", TextType.CODE))
        self.assertEqual(split_node[4], TextNode("of", TextType.IMAGE, "the"))
        self.assertEqual(split_node[5], TextNode("full", TextType.ITALIC))
        self.assertEqual(split_node[6], TextNode("splitter", TextType.LINK, "in"))
        self.assertEqual(split_node[7], TextNode("action", TextType.BOLD))
        self.assertEqual(split_node[8], TextNode("multi", TextType.LINK, "link"))
        self.assertEqual(split_node[9], TextNode("included", TextType.CODE))

    def test_text_full_split(self):
        text = "_This_`is`**a**`test`![of](the)_full_[splitter](in)**action**[multi](link)`included`"
        result = text_to_textnodes(text)
        self.assertEqual(result[0], TextNode("This", TextType.ITALIC))
        self.assertEqual(result[1], TextNode("is", TextType.CODE))
        self.assertEqual(result[2], TextNode("a", TextType.BOLD))
        self.assertEqual(result[3], TextNode("test", TextType.CODE))
        self.assertEqual(result[4], TextNode("of", TextType.IMAGE, "the"))
        self.assertEqual(result[5], TextNode("full", TextType.ITALIC))
        self.assertEqual(result[6], TextNode("splitter", TextType.LINK, "in"))
        self.assertEqual(result[7], TextNode("action", TextType.BOLD))
        self.assertEqual(result[8], TextNode("multi", TextType.LINK, "link"))
        self.assertEqual(result[9], TextNode("included", TextType.CODE))

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_two(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "new line",
                "- This is a list\n- with items",
            ],
        )    

    def test_block_type_heading(self):
        block = "#### This is a heading.\nWith another line after."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_code(self):
        block = "```\nThis is Code.\nWith another line in it.\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_type_quote(self):
        block = "> This is a quote.\n> With multiple lines.\n> As a test."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_type_unordered(self):
        block = "- This is an unordered list.\n- With multiple lines.\n- As a test."
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_type_ordered(self):
        block = """1. This is an ordered list.
2. With multiple lines.
3. As a test."""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_type_paragraph_one(self):
        block = "This is a paragraph.\nWith no special traits\nAs a test."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_paragraph_two(self):
        block = "###     \nThis is a fake header.\nWhich is actually a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_paragraph_three(self):
        block = "```\nThis is fake code.\nWhich is actually a paragraph\n``"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_paragraph_four(self):
        block = "> This is a fake quote.\nWhich is actually a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_paragraph_five(self):
        block = "- This is a fake unordered list.\nWhich is actually a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_paragraph_six(self):
        block = "1. This is a fake ordered list.\nWhich is actually a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )   

    def test_full_block(self):
        md = """
## **Heading**

```
**Code** block _here_
```

> **Quote**
> block
> _here_

**Paragraph** with ![an](image) _here_
and [a](link) _here_

- An
- `Unordered`
- List
- _here_

1. An
2. `Ordered`
3. List
4. _here_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2><b>Heading</b></h2><pre><code>**Code** block _here_</code></pre><blockquote><b>Quote</b> block <i>here</i></blockquote><p><b>Paragraph</b> with <img src=\"image\" alt=\"an\"></img> <i>here</i> and <a href=\"link\">a</a> <i>here</i></p><ul><li>An</li><li><code>Unordered</code></li><li>List</li><li><i>here</i></li></ul><ol><li>An</li><li><code>Ordered</code></li><li>List</li><li><i>here</i></li></ol></div>")

    def test_title_extract(self):
        md = """
# Title Here        

Random Text Here

More Here
"""
        title = extract_title(md)
        self.assertEqual(title, "Title Here")


