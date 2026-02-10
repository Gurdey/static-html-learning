import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("h1", "Text goes here")
        self.assertIsNotNone(node.tag)

    def test_value(self):
        node = HTMLNode("h1", "Text goes here")
        self.assertIsNotNone(node.value)

    def test_return(self):
        new_dict = {}
        new_dict["Test"] = "Test Value 1"
        new_dict["Test2"] = "Test Value 2"
        new_list = ["example", "example2"]
        node = HTMLNode("h1", "Text goes here", new_list, new_dict)
        self.assertIsNotNone(node)

    def test_to_html(self):
        new_dict = {}
        new_dict["Test"] = "Test Value 1"
        new_dict["Test2"] = "Test Value 2"
        new_list = ["example", "example2"]
        node = HTMLNode("h1", "Text goes here", new_list, new_dict)
        returned = f"props to html: {node.props_to_html()}"
        self.assertIsNotNone(returned)        

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_children(self):
        node = LeafNode("p", "Hello, world!", "props here")
        self.assertIsNone(node.children)

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )    

    def test_to_html_no_children(self):
        node = ParentNode("na", children=None)
        node_rep = node.__repr__()
        ex_result = f""
        try:
            result = node.to_html()
        except Exception as e:
            ex_result = e
        self.assertEqual(f"{ex_result}", f"ParentNode: {node_rep}, is missing self.children.")

    def test_to_html_multiple_children(self):
        child_nodes = [LeafNode("a", "a_node"), LeafNode("b", "b_node"), LeafNode("c", "c_node")]
        parent = ParentNode("na", child_nodes)
        self.assertEqual(parent.to_html(), "<na><a>a_node</a><b>b_node</b><c>c_node</c></na>")

    def test_to_html_multiple_parents(self):
        child_nodes = [LeafNode("a", "a_node"), LeafNode("b", "b_node"), LeafNode("c", "c_node")]
        parent_a = ParentNode("na", child_nodes)
        parent_b = ParentNode("nb", child_nodes)
        parent_c = ParentNode("nc", child_nodes)
        grandparent = ParentNode("gp", [parent_a, parent_b, parent_c])
        self.assertEqual(grandparent.to_html(), "<gp><na><a>a_node</a><b>b_node</b><c>c_node</c></na><nb><a>a_node</a><b>b_node</b><c>c_node</c></nb><nc><a>a_node</a><b>b_node</b><c>c_node</c></nc></gp>")


