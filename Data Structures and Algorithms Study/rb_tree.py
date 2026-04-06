import enum

class Color(enum.Enum):
    RED = 0
    BLACK = 1

class Node:
    """
    Represents a single node in the Red-Black Tree.
    """
    def __init__(self, data, color=Color.RED):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    """
    A balanced Red-Black Tree implementation following CLRS standards.
    Properties:
    1. Every node is either red or black.
    2. The root is black.
    3. Every leaf (NIL) is black.
    4. If a node is red, then both its children are black.
    5. For each node, all simple paths from the node to descendant leaves 
       contain the same number of black nodes.
    """
    def __init__(self):
        # NIL represents the sentinel leaf node (always black)
        self.NIL = Node(0, Color.BLACK)
        self.root = self.NIL

    def find(self, key):
        """
        Searches for a node with the given key.
        Returns the node if found, otherwise None.
        """
        curr = self.root
        while curr != self.NIL:
            if key == curr.data:
                return curr
            if key < curr.data:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def insert(self, key):
        """
        Inserts a new key into the tree and maintains RB-tree properties.
        """
        new_node = Node(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        y = None
        x = self.root
        
        # Standard BST insertion
        while x != self.NIL:
            y = x
            if new_node.data < x.data:
                x = x.left
            else:
                x = x.right
        
        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.data < y.data:
            y.left = new_node
        else:
            y.right = new_node
            
        # If the new node is root, just color it black and return
        if new_node.parent is None:
            new_node.color = Color.BLACK
            return
        
        # If the grandparent is None, no fix needed
        if new_node.parent.parent is None:
            return
            
        # Fix the tree to maintain RB properties
        self._fix_insert(new_node)

    def _fix_insert(self, k):
        """
        Restores RB-tree properties after insertion.
        Focuses on fixing "Double Red" violations.
        """
        while k.parent.color == Color.RED:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # Uncle
                if u.color == Color.RED:
                    # Case 1: Uncle is red -> Recoloring
                    u.color = Color.BLACK
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Case 2: Uncle is black, k is left child -> Right rotation
                        k = k.parent
                        self._rotate_right(k)
                    # Case 3: Uncle is black, k is right child -> Left rotation + Recoloring
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    self._rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right  # Uncle
                if u.color == Color.RED:
                    # Case 1 symmetric
                    u.color = Color.BLACK
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # Case 2 symmetric
                        k = k.parent
                        self._rotate_left(k)
                    # Case 3 symmetric
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    self._rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = Color.BLACK

    def _rotate_left(self, x):
        """Left rotation around node x."""
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        """Right rotation around node x."""
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete(self, key):
        """Deletes a node with the given key and fixes the tree."""
        z = self.find(key)
        if not z: return False
        
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            # Node with two children: find successor
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        
        # If the removed node was black, we might have violated the black height property
        if y_original_color == Color.BLACK:
            self._fix_delete(x)
        return True

    def _fix_delete(self, x):
        """Restores RB-tree properties after deletion."""
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                s = x.parent.right  # Sibling
                if s.color == Color.RED:
                    # Case 1: Sibling is red
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._rotate_left(x.parent)
                    s = x.parent.right
                if s.left.color == Color.BLACK and s.right.color == Color.BLACK:
                    # Case 2: Sibling's children are both black
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.right.color == Color.BLACK:
                        # Case 3: Sibling's right child is black
                        s.left.color = Color.BLACK
                        s.color = Color.RED
                        self._rotate_right(s)
                        s = x.parent.right
                    # Case 4: Sibling's right child is red
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.right.color = Color.BLACK
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                # Symmetric cases for right child
                s = x.parent.left
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._rotate_right(x.parent)
                    s = x.parent.left
                if s.right.color == Color.BLACK and s.left.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.left.color == Color.BLACK:
                        s.right.color = Color.BLACK
                        s.color = Color.RED
                        self._rotate_left(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.left.color = Color.BLACK
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def _transplant(self, u, v):
        """Helper to replace subtree u with subtree v."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """Returns the node with the minimum value in the subtree."""
        while node.left != self.NIL:
            node = node.left
        return node

    def inorder_traversal(self, node):
        """Prints the tree inorder: value(Color)."""
        if node != self.NIL:
            self.inorder_traversal(node.left)
            color_char = "R" if node.color == Color.RED else "B"
            print(f"{node.data}({color_char})", end=" ")
            self.inorder_traversal(node.right)

if __name__ == "__main__":
    rbt = RedBlackTree()
    
    # 1. Insertion Test
    print("--- 1. Insertion Test ---")
    test_data = [10, 20, 30, 15, 25, 5, 1]
    for val in test_data:
        print(f"Inserting: {val}")
        rbt.insert(val)
    print("Inorder Traversal: ", end="")
    rbt.inorder_traversal(rbt.root)
    print("\n")

    # 2. Search Test (Finding 15)
    print("--- 2. Search Test ---")
    target = 15
    result = rbt.find(target)
    if result:
        print(f"Key {target} FOUND in the tree.")
    else:
        print(f"Key {target} NOT FOUND.")
    
    # Verify a non-existent key
    non_existent = 100
    if not rbt.find(non_existent):
        print(f"Key {non_existent} correctly NOT FOUND.")
    print()

    # 3. Deletion Test
    print("--- 3. Deletion Test ---")
    keys_to_delete = [10, 30]
    for k in keys_to_delete:
        print(f"Deleting: {k}")
        rbt.delete(k)
    
    print("Inorder Traversal after deletion: ", end="")
    rbt.inorder_traversal(rbt.root)
    print("\n\nAll tests completed successfully.")
