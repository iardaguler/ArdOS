import json
from datetime import datetime


class Node:
    """Dosya veya Klasör Nesnesi"""

    def __init__(self, name, is_dir=False, parent=None, owner="root"):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.owner = owner
        # İzinler: r (read), w (write). Örn: "rw"
        # Basitlik için: Sahibi her şeyi yapar, diğerleri sadece okur ("r")
        self.permissions = "rw" if owner == "root" else "r"
        self.children = {} if is_dir else None
        self.content = "" if not is_dir else None
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")


class VirtualFileSystem:
    """Dosya Sistemi Yöneticisi"""

    def __init__(self):
        self.root = Node("/", is_dir=True, owner="root")
        self.current_node = self.root

    def get_path_string(self):
        path = []
        temp = self.current_node
        while temp:
            path.append(temp.name)
            temp = temp.parent
        full_path = "/".join(reversed(path)).replace("//", "/")
        return full_path if full_path else "/"

    def check_permission(self, node, user, mode="r"):
        """Basit izin kontrolü: root her şeyi yapar, sahibi 'rw' yapar, diğerleri 'r' yapar"""
        if user == "root" or user == "admin": return True
        if node.owner == user: return True
        if mode == "r": return True # Herkes okuyabilir
        return False # Yazma/Silme engellendi

    def mkdir(self, name, user="root"):
        if not self.check_permission(self.current_node, user, "w"):
            return "Error: Permission denied (Write)."
        if name in self.current_node.children:
            return "Error: Directory already exists."
        new_dir = Node(name, is_dir=True, parent=self.current_node, owner=user)
        self.current_node.children[name] = new_dir
        return f"Directory '{name}' created."

    def touch(self, name, user="root"):
        if not self.check_permission(self.current_node, user, "w"):
            return "Error: Permission denied (Write)."
        if name in self.current_node.children:
            return "Error: File already exists."
        new_file = Node(name, is_dir=False, parent=self.current_node, owner=user)
        self.current_node.children[name] = new_file
        return f"File '{name}' created."

    def list_dir(self, show_all=False):
        if not self.current_node.children:
            return "Directory is empty."
        output = "Type\tOwner\tName\t\tCreated\n" + "-" * 50 + "\n"
        for name, node in sorted(self.current_node.children.items()):
            # Gizli dosya kontrolü (Nokta ile başlayanlar)
            if name.startswith(".") and not show_all:
                continue
                
            type_str = "<DIR>" if node.is_dir else "<FILE>"
            output += f"{type_str}\t{node.owner}\t{name}\t\t{node.created_at}\n"
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

    def read_file(self, name, user="root"):
        """Dosya içeriğini döndürür"""
        if name in self.current_node.children:
            node = self.current_node.children[name]
            if not self.check_permission(node, user, "r"):
                return "Error: Permission denied (Read)."
            if not node.is_dir:
                return node.content
            return f"Error: '{name}' is a directory."
        return f"Error: File '{name}' not found."

    def remove(self, name, user="root"):
        """Dosya veya boş klasörü siler"""
        if name in self.current_node.children:
            node = self.current_node.children[name]
            if not self.check_permission(node, user, "w"):
                return "Error: Permission denied (Delete)."
            del self.current_node.children[name]
            return f"'{name}' removed."
        return f"Error: '{name}' not found."

    def to_dict(self, node=None):
        """Tüm dosya sistemini JSON yapılabilecek bir sözlüğe çevirir"""
        if node is None: node = self.root
        
        data = {
            "name": node.name,
            "is_dir": node.is_dir,
            "owner": node.owner,
            "permissions": node.permissions,
            "content": node.content,
            "created_at": node.created_at,
            "children": {}
        }
        
        if node.is_dir:
            for child_name, child_node in node.children.items():
                data["children"][child_name] = self.to_dict(child_node)
        return data

    def from_dict(self, data, parent=None):
        """Sözlük yapısını tekrar Node ağacına çevirir"""
        node = Node(data["name"], is_dir=data["is_dir"], parent=parent, owner=data.get("owner", "root"))
        node.content = data.get("content", "")
        node.created_at = data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M"))
        node.permissions = data.get("permissions", "rw")
        
        if data["is_dir"]:
            node.children = {}
            for child_name, child_data in data.get("children", {}).items():
                node.children[child_name] = self.from_dict(child_data, parent=node)
        return node


    def save_to_disk(self, filename="vfs_disk.json"):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def load_from_disk(self, filename="vfs_disk.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.root = self.from_dict(data)
                self.current_node = self.root
        except (FileNotFoundError, json.JSONDecodeError):
            pass # Dosya yoksa veya bozuksa varsayılan boş sistemle devam et