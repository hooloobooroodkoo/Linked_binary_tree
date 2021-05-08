"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log
import random
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from linked_binary_tree import LinkedBinaryTree

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                _r = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if _r == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return _r

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = newItem
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None


    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        size = self._size
        return height < 2 * log(size + 1, 2) -1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = []
        for element in self:
            if low <= element <= high:
                lst.append(element)
        if lst == []:
            return None
        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def recursive(lst_of_values, lst=LinkedQueue()):
            if len(lst_of_values) != 0:
                mid = len(lst_of_values)//2
                lst.add(lst_of_values[mid:][0])
                lst_of_values.remove(lst_of_values[mid:][0])
                recursive(lst_of_values[:mid])
                recursive(lst_of_values[mid:])
            return lst
        values = list(self.inorder())
        ordered_values = recursive(values)
        self.clear()
        while len(ordered_values) != 0:
            self.add(ordered_values.pop())

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = None
        lst_of_values = list(self.inorder())
        if item not in lst_of_values:
            lst_of_values.append(item)
            lst_of_values.sort()
        index = lst_of_values.index(item) + 1
        try:
            result = lst_of_values[index]
        except IndexError:
            pass
        return result


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = None
        lst_of_values = list(self.inorder())
        if item not in lst_of_values:
            lst_of_values.append(item)
            lst_of_values.sort()
        try:
            index = lst_of_values.index(item) - 1
            if index >= 0:
                result = lst_of_values[index]
        except Exception:
            pass
        return result
    @staticmethod
    def create_balanced_tree(lst):
        '''
        Rebalances the tree.
        :return:
        '''

        def recursive(lst_of_values, lst=LinkedQueue()):
            if len(lst_of_values) != 0:
                mid = len(lst_of_values)//2
                lst.add(lst_of_values[mid:][0])
                lst_of_values.remove(lst_of_values[mid:][0])
                recursive(lst_of_values[:mid])
                recursive(lst_of_values[mid:])
            return lst
        lst.sort()
        ordered_values = recursive(lst)
        tree = LinkedBST()
        while len(ordered_values) != 0:
            tree.add(ordered_values.pop())
        return tree

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        dictionary = []
        dictionary = [line[:-1] for line in\
                        open(path, 'r', encoding='utf-8').readlines()]
        find_words = random.sample(dictionary, 10000)

        print("\nComparing...\n")
        # list
        dictionary.sort()
        time_1_start = time.time()
        [word in dictionary for word in find_words]
        time_1_end = time.time()
        time_1 = time_1_end - time_1_start
        print(f'Time 1:  {time_1}   *find 10.000 words among 250.000 using list\n')

        # alphabetic order of adding values to the tree
        search_tree = LinkedBST()
        for word in dictionary[:900]:
            search_tree.add(word)
        time_2_start = time.time()
        for word in find_words:
            search_tree.find(word)
        time_2_end = time.time()
        time_2 = time_2_end - time_2_start
        print(f'Time 2:  {time_2}   *find 10.000 words among 900 using tree and adding values in alphabetic order\n')
        
        # This commented code is working with the whole dictionary using LinkedBinaryTree() and alphabetic adding,
        #  but it works too long
        # search_tree = LinkedBinaryTree(dictionary[0])
        # for word in dictionary[1:]:
        #     search_tree.insert_right(word)
        # time_2_start = time.time()
        # for word in find_words:
        #     check = search_tree.get_right_child()
        #     while check.key != word:
        #         check = check.get_right_child()
        # time_2_end = time.time()
        # time_2 = time_2_end - time_2_start
        # print(f'Time 2:  {time_2}   *find 10.000 words among 2200 using tree and adding values in alphabetic order\n')
        
        # random order of adding values to the tree
        search_tree_random_order = LinkedBST()
        mixed = random.sample(dictionary, len(dictionary))
        for word in mixed:
            search_tree_random_order.add(word)
        time_3_start = time.time()
        for word in find_words:
            search_tree_random_order.find(word)
        time_3_end = time.time()
        time_3 = time_3_end - time_3_start
        print(f"Time 3:  {time_3}   *find 10.000 words among 250.000 using tree and adding values in random order\n")
        
        # balanced tree
        balanced_tree = self.create_balanced_tree(dictionary)
        time_4_start = time.time()
        for word in find_words:
            balanced_tree.find(word)
        time_4_end = time.time()
        time_4 = time_4_end - time_4_start
        print(f"Time 4:  {time_4}   *find 10.000 words among 250.000 using balanced tree\n")
