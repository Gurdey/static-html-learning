import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_two(self):
        node = TextNode("This is a text node", TextType.BOLD, "url.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)        
        self.assertNotEqual(node, node2)

    def test_url_exists(self):
        node = TextNode("Url test", TextType.LINK, "https://www.boot.dev")
        self.assertIsNotNone(node.url)

    def test_url_none(self):
        node = TextNode("No url", TextType.TEXT)
        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()