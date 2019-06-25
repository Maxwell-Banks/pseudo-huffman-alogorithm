"""HuffmanHeap class
By: Maxwell M. Banks
May 27th, 2019
"""
import huffman

class HuffmanMinHeap():
    """A MinHeap for a Huffman tree nodes
    Attributes:
        heap(list): A list of HuffmanNodes that can be heapified
        size(int): The given max size of the heap
        end(int): Keeps track the end of the heap
    """
    def __init__(self, size):
        
        self.heap = [None] * size
        self.size = size
        self.end = -1

    def __repr__(self):

        return "{}".format(self.heap)

    def __eq__(self, other):

        return self.heap == other.heap

    def swap(self, index1, index2):
        """Swaps two indexs in a list
        """
        temp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = temp

    def has_left_child(self, index):
        """Checks if a node at an index has a left child
        """
        return (self.end) >= (index * 2) + 1

    def has_right_child(self, index):
        """Checks if a node at an index has a right child
        """
        return (self.end) >= (index * 2) + 2

    def get_left_child(self, index):
        """Returns the left child for a given index
        """
        return self.heap[(index * 2) + 1]

    def get_right_child(self, index):
        """Returns the righ child for the given index
        """
        return self.heap[(index * 2) + 2]

    def right_child_index(self, index):
        """Returns the right child for a given index
        """
        return (index * 2) + 2

    def left_child_index(self, index):
        """Returns the left child for a given index
        """
        return (index * 2) + 1

    def peek(self):
        """Returns the lowest value in the HuffmanMinHeap without
           changing the list
        """
        return self.heap[0]

    def has_parent(self, index):
        """Checks if a node has a parent
        """
        return index != 0

    def get_parent(self, index):
        """Returns a parent Node for a given index
        """
        return self.heap[(index - 1) // 2]

    def get_parent_index(self, index):
        """Returns a parent index for a given index
        """
        return (index - 1) // 2

    def heapify_up(self):
        """Heapifies the bottom value to it's correct place
        """
        index = self.end

        while self.has_parent(index) and \
        huffman.comes_before(self.heap[index], self.get_parent(index)):
            #swap the parent and the value
            self.swap(index, self.get_parent_index(index))
            index = self.get_parent_index(index)

        

    def heapify_down(self):
        """Heapifies the top value into it's correct place
        """
        index = 0
        #while the node has any children
        while self.has_left_child(index):
            #assumes the left node is smaller
            smaller_child_index = self.left_child_index(index)
            #if there's a righ child and it's smaller than the left
            if self.has_right_child(index) \
            and huffman.comes_before(self.get_right_child(index), \
            self.get_left_child(index)):
                #set the smaller child to the right node
                smaller_child_index = self.right_child_index(index)
            
            if huffman.comes_before(self.heap[index], self.heap[smaller_child_index]):
                break
            else:
                self.swap(index, smaller_child_index)
            index = smaller_child_index

    def poll(self):
        """Removes the lowest value in the heap and reorders it
        """
        self.heap[0] = self.heap[self.end]
        self.heap[self.end] = None
        self.end -= 1
        self.heapify_down()
        

    def add(self, node):
        """Adds a new value into the list and reorders it
        """
        self.end += 1
        self.heap[self.end] = node
        self.heapify_up()


    def pop(self):
        val = self.peek()
        self.poll()
        return val
