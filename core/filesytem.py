from datetime import datetime


class Node:
    """Dosya veya Klasör Nesnesi"""

    def __init__(self, name, is_dir=False, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children = {} if is_dir else None
        self.content = "" if not is_dir else None
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")


class VirtualFileSystem:
    """Dosya Sistemi Yöneticisi"""

    def __init__(self):
        self.root = Node("/", is_dir=True)
        self.current_node = self.root

    def get_path_string(self):
        path = []
        temp = self.current_node
        while temp:
            path.append(temp.name)
            temp = temp.parent
        full_path = "/".join(reversed(path)).replace("//", "/")
        return full_path if full_path else "/"

    def mkdir(self, name):
        if name in self.current_node.children:
            return "Error: Directory already exists."
        new_dir = Node(name, is_dir=True, parent=self.current_node)
        self.current_node.children[name] = new_dir
        return f"Directory '{name}' created."

    def touch(self, name):
        if name in self.current_node.children:
            return "Error: File already exists."
        new_file = Node(name, is_dir=False, parent=self.current_node)
        self.current_node.children[name] = new_file
        return f"File '{name}' created."

    def list_dir(self):
        if not self.current_node.children:
            return "Directory is empty."
        output = "Type\tName\t\tCreated\n" + "-" * 40 + "\n"
        for name, node in self.current_node.children.items():
            type_str = "<DIR>" if node.is_dir else "<FILE>"
            output += f"{type_str}\t{name}\t\t{node.created_at}\n"
        return output

    def change_dir(self, name):
        if name == "..":
            if self.current_node.parent:
                self.current_node = self.current_node.parent
            return ""
        if name == "/":
            self.current_node = self.root
            return ""
        if name in self.current_node.children:
            target = self.current_node.children[name]
            if target.is_dir:
                self.current_node = target
                return ""
            else:
                return f"Error: '{name}' is not a directory."
        return f"Error: Directory '{name}' not found."