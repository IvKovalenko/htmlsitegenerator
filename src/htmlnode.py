class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag                  # A string representing the HTML tag name (e.g. “p”, “a”, “h1”, etc.)
        self.value = value              # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children        # A list of HTMLNode objects representing the children of this node
        self.props = props              # A dictionary of key-value pairs representing the attributes of the HTML tag. 
                                        # For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HMTL: no children")
        res = ""
        for child in self.children:
            if child == ParentNode:
                res += child.to_html() #should be call of .to_html for parentNode
            res += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children = {self.children}, {self.props})"