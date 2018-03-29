# Class for a circular, doubly linked list with a sentinel.
# Written by Devin Balkcom, modified by THC.

# Changelog:
#   March 27 2018: Added insert_before, and __iter__ by Jose Pinilla
#   Winter 2016: Original by Thomas H. Cormen
# Based on: http://www.cs.dartmouth.edu/~thc/cs1/lectures/lecture17/lecture17.html


# Class for a node in a circular, doubly linked list with a sentinel.
class Node:
    def __init__(self, data):
        self.data = data  # instance variable to store the data
        self.next = None  # instance variable with address of next node
        self.prev = None  # instance variable with address of previous node

    # Return the data in the Node.
    def get_data(self):
        return self.data

# Class for a circular, doubly linked list with a sentinel.
class LL:
    # Create the sentinel node, which is before the first node
    # and after the last node.
    def __init__(self):
        self.sentinel = Node(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

    # Allow list to be iterable
    def __iter__(self):
        # In order to get to the first Node, we must do
        current = self.first_node()
        # and then, until we have reached the end:
        while current.get_data() is not None:
            yield current.get_data()
            # in order to get from one Node to the next one:
            current = current.next

    # Return a reference to the first node in the list, if there is one.
    # If the list is empty, return None.
    def first_node(self):
        if self.sentinel.next == self.sentinel:
            return None
        else:
            return self.sentinel.next

    # Insert a new node with data after node x.
    def insert_after(self, x, data):
        y = Node(data)   # make a new Node object.
        # Fix up the links in the new node.
        y.prev = x
        y.next = x.next
        # The new node follows x.
        x.next = y
        # And it's the previous node of its next node.
        y.next.prev = y
        return y

    # Insert a new node with data before node x.
    def insert_before(self, x, data):
        y = Node(data)   # make a new Node object.
        # Fix up the links in the new node.
        y.prev = x.prev
        y.next = x
        # The new node follows x.prev
        x.prev.next = y
        # And it's the previous node of x
        x.prev = y
        return y

    # Insert a new node at the end of the list.
    def append(self, data):
        last_node = self.sentinel.prev
        y = self.insert_after(last_node, data)
        return y

    # Insert a new node at the start of the list.
    def prepend(self, data):
        self.insert_after(self.sentinel, data)

    # Delete node x from the list.
    def delete(self, x):
        # Splice out node x by making its next and previous
        # reference each other.
        x.prev.next = x.next
        x.next.prev = x.prev

    # Find a node containing data, and return a reference to it.
    # If no node contains data, return None.
    def find(self, data):
        # Trick: Store a copy of the data in the sentinel,
        # so that the data is always found.
        self.sentinel.data = data

        x = self.first_node()
        while x.data != data:
            x = x.next

        # Restore the sentinel's data.
        self.sentinel.data = None

        # Why did we drop out of the while-loop?
        # If we found the data in the sentinel, then it wasn't
        # anywhere else in the list.
        if x == self.sentinel:
            return None     # data wasn't really in the list
        else:
            return x        # we found it in x, in the list

    #  Return the string representation of a circular, doubly linked
    #  list with a sentinel, just as if it were a Python list.
    def __str__(self):
        s = "["

        x = self.sentinel.next
        while x != self.sentinel:  # look at each node in the list
            if type(x.data) == str:
                s += "'"
            s += str(x.data)        # concatenate this node's data
            if type(x.data) == str:
                s += "'"
            if x.next != self.sentinel:
                s += ", "   # if not the last node, add the comma and space
            x = x.next

        s += "]"
        return s
