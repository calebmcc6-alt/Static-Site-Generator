class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        prop_string = ""
        if self.props != None:
            for prop in self.props:
                prop_string += f' {prop}="{self.props[prop]}"'
        return prop_string

    def __repr__(self):
        return f"tag={self.tag} value={self.value} children={self.children} props={self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"tag={self.tag} value={self.value} props={self.props}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError()
        if self.children == None:
            raise ValueError()
        html_string = f"<{self.tag}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string
