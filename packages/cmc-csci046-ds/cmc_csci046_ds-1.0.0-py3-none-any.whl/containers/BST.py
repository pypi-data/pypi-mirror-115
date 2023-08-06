'''
This file implements the Binary Search Tree data structure.
The functions in this file are considerably harder than the
functions in the BinaryTree file.
'''

from containers.BinaryTree import BinaryTree, Node


class BST(BinaryTree):
    '''
    The BST is a superclass of BinaryTree.
    That means that the BST class "inherits" all of the methods
    from BinaryTree,
    and we don't have to reimplement them.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the BST.
        '''
        super().__init__()
        if xs:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string
        that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command BST([1,2,3])
        it's __repr__ will return "BST([1,2,3])"

        For the BST, type(self).__name__ will be the string "BST",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of BST
        will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def __eq__(self, t2):
        '''
        This method checks to see if the contents of self and t2 are equal.
        The expression `a == b` desugars to `a.__eq__(b)`.

        NOTE:
        We only care about "semantic" equality,
        and not "syntactic" equality.
        That is, we do not care about the tree structure itself,
        and only care about the contents of what the tree contains.

        HINT:
        Convert the contents of both trees into a sorted list,
        then compare those sorted lists for equality.
        '''
        return self.to_list('inorder') == t2.to_list('inorder')

    def is_bst_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that
        checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether
        insert/delete functions
        are actually working.
        '''
        if self.root:
            return BST._is_bst_satisfied(self.root)
        return True

    @staticmethod
    def _is_bst_satisfied(node):
        '''
        FIXME:
        The current implementation has a bug:
        it only checks if the children of the current node
        are less than/greater than,
        rather than ensuring that all nodes to the left/right
        are less than/greater than.

        HINT:
        Use the _find_smallest and _find_largest functions to fix the bug.
        You should use the _ prefixed methods because those are
        static methods just like this one.
        '''
        ret = True
        if node.left:
            if node.value >= BST._find_largest(node.left):
                ret &= BST._is_bst_satisfied(node.left)
            else:
                ret = False
        if node.right:
            if node.value <= BST._find_smallest(node.right):
                ret &= BST._is_bst_satisfied(node.right)
            else:
                ret = False
        return ret

    def insert(self, value):
        '''
        Inserts value into the BST.

        FIXME:
        Implement this function.

        HINT:
        Create a staticmethod helper function following the
        pattern of _is_bst_satisfied.
        '''
        # Tree is empty
        if not self.root:
            self.root = Node(value)
            return
        # Value to insert is the root
        elif self.root.value == value:
            return
        else:
            return self._insert(self.root, value)

    @staticmethod
    def _insert(node, value):
        if value < node.value:
            if node.left:
                return BST._insert(node.left, value)
            node.left = Node(value)

        if value > node.value:
            if node.right:
                return BST._insert(node.right, value)
            node.right = Node(value)

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.
        '''
        for x in xs:
            self.insert(x)

    def __contains__(self, value):
        '''
        Recall that `x in tree` desugars to `tree.__contains__(x)`.
        '''
        return self.find(value)

    def find(self, value):
        '''
        Returns whether value is contained in the BST.
        '''
        if not self.root:
            return False

        if self.root.value == value:
            return True

        else:
            if value < self.root.value:
                return self._find(value, self.root.left)

            if value > self.root.value:
                return self._find(value, self.root.right)

    @staticmethod
    def _find(value, node):
        '''
        recursive helper function to find a value in a BST
        '''
        if not node:
            return False

        if node.value == value:
            return True

        else:
            if node.value > value:
                return BST._find(value, node.left)
            if node.value < value:
                return BST._find(value, node.right)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_smallest(self.root)

    @staticmethod
    def _find_smallest(node):
        '''
        This is a helper function for find_smallest and not
        intended to be called directly by the user.
        '''
        assert node is not None
        if node.left is None:
            return node.value
        else:
            return BST._find_smallest(node.left)

    def find_largest(self):
        '''
        Returns the largest value in the tree.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_largest(self.root)

    @staticmethod
    def _find_largest(node):
        '''
        This is a helper function for find_largest and not
        intended to be called directly by the user.
        '''
        assert node is not None
        if node.right is None:
            return node.value
        else:
            return BST._find_largest(node.right)

    def remove(self, value):
        '''
        Removes value from the BST.
        If value is not in the BST, it does nothing.
        '''
        if not self.root:
            return self.root

        else:
            self.root = self._remove(value, self.root)

    @staticmethod
    def _remove(value, node):
        if not node:
            return node

        if value > node.value:
            node.right = BST._remove(value, node.right)
            return node

        if value < node.value:
            node.left = BST._remove(value, node.left)
            return node

        if node.value == value:
            if node.left and node.right:
                largest = BST._find_largest(node.left)
                node.value = largest
                node.left = BST._remove(largest, node.left)
                return node

            if node.left and not node.right:
                return node.left

            if node.right and not node.left:
                return node.right

    def remove_list(self, xs):
        '''
        Given a list xs, remove each element of xs from self.
        '''
        for x in xs:
            self.remove(x)
