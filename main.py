from model.Node import Node, NODES


def main():
    Node.load_from_db()

    action_number = menu()
    while action_number != '6':
        if action_number == '1':
            node = base_node()
            Node.create_or_update_node(node, False)

        if action_number == '2':
            node = base_node()
            children_number = int(input("Print children' number.\n"))
            i = 0
            while i < children_number:
                child = NODES.get(input("Print child's name.\n"))
                node.children[child.data] = child
                i = i + 1
            Node.create_or_update_node(node, True)

        if action_number == '3':
            node = NODES.get(input("Print node data.\n"))
            node.__delete__()

        if action_number == '4':
            Node.draw()

        if action_number == '5':
            first_node = input("Print first node data.\n")
            second_node = input("Print second node data.\n")
            Node.search(first_node, second_node)

        print(NODES.__len__())
        action_number = menu()

    Node.save_to_db()


def base_node():
    parent_name = input("Print parent name.\n")
    data = input("Print unique data.\n")
    return Node(parent_name, data)


def menu():
    print("Choose an action number:\n")
    print("1 - Create or update a node without a child.\n")
    print("2 - Create or update a node with a child.\n")
    print("3 - Delete a node.\n")
    print("4 - Draw trees.\n")
    print("5 - Find connections.\n")
    print("6 - Exit.\n")
    return input()


if __name__ == '__main__':
    main()
