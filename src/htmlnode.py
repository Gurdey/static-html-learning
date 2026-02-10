class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props = f""
        if self.props == None:
            return props
        if len(self.props) < 1:
            return props
        for prop in self.props:
            props += f' {prop}="{self.props[prop]}"'
        return props
    
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError(f"LeafNode: {self.__repr__()}, is missing a self.value.")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError(f"ParentNode: {self.__repr__()}, is missing a self.tag.")
        if self.children == None:
            raise ValueError(f"ParentNode: {self.__repr__()}, is missing self.children.")
        end_value = f""
        for child in self.children:
            end_value += child.to_html()
        return f"<{self.tag}{super().props_to_html()}>{end_value}</{self.tag}>"

