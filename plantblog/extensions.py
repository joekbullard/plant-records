from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class TailwindExtension(Extension):
    """An extension to add classes to tags"""

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            TailwindTreeProcessor(md), "tailwind", 20)


class TailwindTreeProcessor(Treeprocessor):
    """Walk the root node and modify any discovered tag"""

    classes = {
        "a": "underline text-blue-700 hover:text-blue-500",
        "p": "pb-4 text-base",
    }

    def run(self, root):
        for node in root.iter():
            tag_classes = self.classes.get(node.tag)
            if tag_classes:
                node.attrib["class"] = tag_classes
