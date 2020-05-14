import json
import os

import settings

NODES = dict()
TREES = list()


class Node:

    def __init__(self, parent_name, data, children_names=None):
        if children_names is None:
            children_names = {}
        self.parent_name = parent_name
        self.data = data
        self.children = children_names

    def eq(self, other):
        return self.data == other.data

    @staticmethod
    def create_or_update_node(node, with_child):
        parent_node = ''
        if node.parent_name.__len__() > 0:
            parent_node = NODES.get(node.parent_name)
            parent_node.children[node.data] = node

        if with_child is True:
            for child in node.children.values():
                child_node = NODES.get(child.data)
                if node.parent_name.__len__() > 0:
                    if parent_node.children.get(child.data) is not None:
                        parent_node.children.pop(child.data)
                if child_node is not None:
                    child_node.parent_name = node.data
                else:
                    new_child_node = Node(child.parent_name, child.data)
                    NODES.update({new_child_node.data: new_child_node})
        NODES.update({node.data: node})
        return node

    def __delete__(self):
        NODES.get(self.parent_name) \
            .children_names.pop(self.data)
        NODES.pop(self.data)

    @staticmethod
    def draw():
        for node in NODES.values():
            if node.parent_name.__len__() == 0:
                print("Tree")
                print(node.str())

    def str(self, level=0):
        ret = "\t" * level + "|__" + repr(self.data) + "\n"
        for child in self.children.values():
            ret += child.str(level + 1)
        return ret

    found = False

    @staticmethod
    def search(first_node_data, second_node_data):
        first_node = NODES.get(first_node_data)
        second_node = NODES.get(second_node_data)
        if second_node.parent_name.__eq__(first_node.parent_name):
            Node.found = True
            print("{} and {} are siblings".format(first_node_data, second_node_data))
        else:
            if first_node is not None and second_node is not None:
                Tree.make_trees()
                for tree in TREES:
                    if tree.nodes.get(first_node_data) is not None and tree.nodes.get(second_node_data) is not None:
                        element = tree.nodes.get(first_node_data)
                        element.check_parent(first_node_data, second_node_data)
        if not Node.found:
            print("No connection is found")

    def check_parent(self, first_node_data, second_node_data):
        if self.parent_name.__len__() > 0:
            if self.parent_name.__eq__(second_node_data):
                Node.found = True
                print("{} is a child for {}".format(first_node_data, second_node_data))
            else:
                NODES.get(self.parent_name).check_parent(first_node_data, second_node_data)
        else:
            NODES.get(first_node_data).check_children(first_node_data, second_node_data)

    def check_children(self, first_node_data, second_node_data):
        if self.children.__len__() > 0:
            for child in self.children.values():
                if child.data.__eq__(second_node_data):
                    Node.found = True
                    print("{} is a parent for {}".format(first_node_data, second_node_data))
                    break
                else:
                    NODES.get(child.data).check_children(first_node_data, second_node_data)

    @classmethod
    def load_from_db(cls):
        file_path = settings.DB_FILE_PATH

        if os.stat(file_path).st_size != 0:
            with open(file_path, 'r') as infile:
                data = json.load(infile)
                for element in data:
                    node = Node(element['parent_name'], element['data'])
                    children_dict = element['children']
                    if children_dict.__len__() > 0:
                        for child_dict in children_dict:
                            child_node = Node(child_dict['parent_name'], child_dict['data'])
                            node.children[child_node.data] = child_node
                        Node.create_or_update_node(node, True)
                    else:
                        Node.create_or_update_node(node, False)
                    print('Схема "{}" загружена из {}\n'.format(node.data, file_path))

        else:
            print('DB is empty')

    @staticmethod
    def save_to_db():
        data = []
        file_path = settings.DB_FILE_PATH

        Tree.make_trees()
        for element in TREES:
            for node in element.nodes_list:
                data.append(node.serialize())
                print('Схема "{}" сохранена в {}\n'.format(node.data, file_path))

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=1, ensure_ascii=False)

    def serialize(self):
        data = {
            'parent_name': self.parent_name,
            'data': self.data,
            'children': []
        }
        for child in self.children.values():
            child = child.serialize()
            data['children'].append(child)

        return data

    @classmethod
    def deserialize(cls, data):
        node = Node(cls)

        for key, value in data.items():
            getattr(node, key).value = value

        return node


class Tree:

    def __init__(self, nodes=None):
        if nodes is None:
            nodes = {}
        self.nodes = nodes
        self.nodes_list = []

    @staticmethod
    def make_trees():
        TREES.clear()
        for node in NODES.values():
            if node.parent_name.__len__() == 0:
                tree = Tree()
                tree.find_child(node)
                tree.nodes_list = list(tree.nodes.values())
                tree.nodes_list.reverse()
                TREES.append(tree)

    def find_child(self, node):
        if node.children.__len__() == 0:
            self.nodes.update({node.data: node})
        else:
            for child in node.children.values():
                self.find_child(child)
            self.nodes.update({node.data: node})
