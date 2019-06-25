"""Huffman Coding
CPE202

Author: Maxwell M. Banks
"""

import huffman_heap
import collections

class Node:
    """A node for a Huffanman Data tree
    Attributes:
        freq(int): The number of times a letter is found in the text
        data(str): The letter
        left(HuffmanNode): The left node attached to it
        right(HuffmanNode): The right node attached to it
    """
    def __init__(self, frequency, letter=None, left=None, right=None):
        self.freq = int(frequency)
        self.data = letter
        self.left = left
        self.right = right
        self.bin_code = None

    def __repr__(self):
        return "  '{}' freq:{} bin code:{} \n  ({})\n  ({})".format(\
            self.data, self.freq, self.bin_code, self.left, self.right)
        
    def __eq__(self, other):

        return self.freq == other.freq\
          and self.data == other.data\
          and self.left == other.left\
          and self.right == other.right

def cnt_freq(filename):
    """Takes a text file name and finds the amount of times every
       character appears
    
    Inputs:
        filename(string): the name of the file we're looking at

    Returns:
        list: A list with 256 values, one for each 8-bit charecters
    """
    #open the file
    file = open(filename, 'r')
    #read the file
    file_contents = file.read()
    #iterate through every character in the file
    freq = [0] * 256
    for char in file_contents:
            #increase the  value in the index's list
            freq[ord(char)] += 1
    file.close()
    return freq

def comes_before(a, b):
    """takes two Huffamn nodes and tells you which one has more or 
       less apperences in the text file you got
    
    Inputs:
        a(Node): One given Node
        b(Node): The other given Node
    
    Returns:
        Node: The Node with the larger number of apperences
    """
    if a.freq < b.freq:
        return True
    
    elif b.freq < a.freq:
        return False
    
    else:
        if a.data < b.data:
            return True
        else:
            return False

def create_huff_tree(list_of_freqs):
    #creates an empty list to hold all of the charecters
    list_of_chars = []
    #Repeats the number of values in the given text file
    for x in range(len(list_of_freqs)):
        #finds all the values that have data
        if list_of_freqs[x] != 0:
            #appends them to a list if they aren't empty
            list_of_chars.append((list_of_freqs[x], chr(x)))
    #makes a new empty heap desgned for huffman nodes
    
    char_nodes_heap = huffman_heap.HuffmanMinHeap(len(list_of_chars))
        #takes every value and adds it into a heap

    for x in list_of_chars:
        char_nodes_heap.add(Node(x[0], x[1]))
        #print(char_nodes_heap)
    #print(char_nodes_heap)

    #While the tree isn't completly built
    #print(char_nodes_heap)

    while char_nodes_heap.end > 0:
                #take the lowest two values
        #print('\n==========================================================\n')
        node1 = char_nodes_heap.pop()
        node2 = char_nodes_heap.pop()
        #create a node with their combined frequency and smaller letter
        node3 = Node(node1.freq + node2.freq, min(node1.data, node2.data))
        #Sets the new node equal to the old two nodes
        node3.left = node1
        node3.right = node2
        #Set node3 charecter to smaller of two node
        #Heaps in the new node into the old Heap
        char_nodes_heap.add(node3)
        #print(char_nodes_heap)

            
    #returns the remaining value at the top of the heap
    huff_tree = char_nodes_heap.peek()
    assign_huffTree_binary(huff_tree)

    return (huff_tree)

def assign_binary(Node, par_bin):
    """Recursivly gives all nodes in a huffman tree the values of their binary 
    nodes value
    Args:
        huffman_tree(HuffmanTree): The huffman tree we're going
        create codes for

    Returns:
        None
    """
    Node.bin_code = par_bin

    if (Node.left and Node.right):
        assign_binary(Node.left, Node.bin_code + '0')
        assign_binary(Node.right, Node.bin_code + '1')
        Node.bin_code = None

def assign_huffTree_binary(huff_tree):
    """Calls huff_tree and gives all nodes a binary code 
    for their letter
    """

    assign_binary(huff_tree, "")
    return huff_tree

def create_code(huff_tree):
    """Searches through a huffman tree and finds all the nodes 
    that have a letter tied to them
    """
    
    letters = [None] * 256
    useful = find_usful_nodes(huff_tree)
    for x in useful:
        letters[ord(x.data)] = x.bin_code

    return letters

def find_usful_nodes(Node):
    """Search through nodes recursivly to find all the nodes that have a
    letter tied to them
    """

    if not Node.left and not Node.right:
        return Node

    elif (Node.left and Node.right):
        useful_left = find_usful_nodes(Node.left)
        useful_right = find_usful_nodes(Node.right)

        if type(useful_left) != list: useful_left = [useful_left] 
        if type(useful_right) != list: useful_right = [useful_right] 

        return useful_left + useful_right

def huffman_encode(in_file, out_file):
    """Takes a file and creates a huffman coded binary file from
    the text in the given file
    Args:
        in_file(str): The name of the file to be coded
        out_file(str): The name of the file to put the binary code
        
    Returns:
        None
    """
    #√
    freq = cnt_freq(in_file)
    huff_tree = create_huff_tree(freq)
    #print(huff_tree)
    #print()
    
    #print(huff_tree)
    #print()
    huff_codes = create_code(huff_tree)
    #print(huff_codes)
    #print()
    #print(huff_codes[ord('d')])
    #print(huff_codes[ord('a')])
    #print(huff_codes[ord('f')])
    #print(huff_tree)
    #print(huff_codes[ord('d')])
    file = open(in_file, 'r')
    file_str = file.read()
    bin_str = ""
    #(file_str)
    for l in file_str:
        bin_str += huff_codes[ord(l)]
    file.close()

    file0 = open(out_file, 'w')
    file0.write(bin_str)

def tree_preord(hufftree):
    """Calls the node_preord function for a huffmen tree 
    Args:
        hufftree(HuffmanTree): The tree we're getting ndoes from

    Returns:
        str: A list of pre ordered nodes' data
    """
    nodes = node_preord(hufftree)
    nodes = nodes[:-1]
    return nodes

def node_preord(node):
    """Takes a tree and retursn all leaves' data in preorder 
    Args:
        node(Node): The node we're getting ndoes from

    Returns:
        str: A list of pre ordered nodes' data
    #NOT SURE IF RIGHT CHECK WITH TOSHI
    """

    if node.left is None and node.right is None:
        return ("1-" + str(ord(node.data)) + "-")

    
    #add current node
    nodes = '0' 
    #search through the left nodes
    nodes += node_preord(node.left)
    #search through the right nodes
    nodes += node_preord(node.right)
    #return the finals nodes
    return nodes

def huffman_decode(list_of_freqs, encoded_file, decode_file):
    """Takes a list of frequences and a file with encoded strins on
    it and returns it in decoded text
    Args:
        list_of_freqs(list): The frequencey of the letters in the original file 
        encoded_file(str): Name of where the encoded message is
        decoded_file(str): Name of file where the decoded message
                           will be
    Returns:
        None
    """
    file = open(encoded_file, 'r')
    encoded = file.read()
    file.close()
    file_tree = create_huff_tree(list_of_freqs)
    #print(file_tree)
    file = open(decode_file, 'w')
    decoded = decode(encoded, file_tree)
    file.write(decoded)

def decode(code, huff_tree_node):
    """Takes an encoded list of binary and returns a single string in 
    plain text
    Args:
        code(string): a length of binary code that will be converted
        huff_tree_node(Node):Head value of a binary tree that corr
                             corresponds with the given code
    Returns:
        str: the code variable's strung uncoded
    """
    return_str = ""
    tree_loc = huff_tree_node
    code_sf = ""
    while True:
        #print(code)
        #if we find a leaf
        if tree_loc.left is None and tree_loc.right is None:
            #print(code_sf)
            return_str += tree_loc.data
            tree_loc = huff_tree_node
            code_sf = ""
            if len(code) == 0:
                break
        #if the next node goes left
        elif code[0] == '0':
            code_sf += code[0]
            code = code[1:]
            tree_loc = tree_loc.left
        #if the next node goes right
        elif code[0] == '1':
            code_sf += code[0]
            code = code[1:]
            tree_loc = tree_loc.right
    return return_str



def main():

    file_input_name = input('Name of input file: ')
    file_output_name = input('Name of output file: ')
    print('Encoding...')
    huffman_encode(file_input_name, file_output_name)
    #print('Decoding...')
    #huffman_decode(freqs, 'test'+num+'.out', 'Banks'+num+'decoded.txt')

    
if __name__ == "__main__":
    main()

