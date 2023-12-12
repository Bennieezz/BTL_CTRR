import networkx as nx
import pandas as pd
import numpy as np
from pyvis.network import Network
from scipy.sparse import coo_matrix, csr_matrix
from IPython.display import display, HTML


def count_triangles(matrix):
    return (matrix == 2).nnz / 3


def list_triangle(num):
    # If the numbers of triangles is greater than 100 then print the message for not printing the list
    # else print the list of triangles base on the matrix 'c'
    if num <= 100:
        global c, vertex_list, edge_list
        row_indices_, col_indices_ = c.nonzero()
        # Create a coordinate list base on the row and column indices of locations in the matrix c
        # where the value is equal to 2
        target_indices = [(row, col) for row, col in zip(row_indices_, col_indices_) if
                          c[row, col] == 2]
        triangle_set = set()
        for temp in target_indices:
            vertex = vertex_list[temp[0]]
            edge = edge_list[temp[1]]
            triangle = tuple(sorted((vertex, *edge)))
            triangle_set.add(triangle)
        print(f"\nAnd the triangle list is\n {list(triangle_set)} \n")
    else:
        print("There are more than 100 triangles, so I won't print it to keep it clear.\n")


def to_adjacency_matrix():
    global col_indices, row_indices, num_vertex
    # Create a data list of 1 in the size of row/col indices
    # Create an adjacent_matrix using spare matrix for optimise the memory
    adjacent_matrix = coo_matrix(([1] * len(row_indices), (row_indices, col_indices)), shape=(num_vertex, num_vertex), dtype=np.uint8)
    return adjacent_matrix.tocsr()


def to_incidence_matrix():
    global edge_list, num_edge, num_vertex, edge_dict, col_indices
    temp_list = edge_list
    temp_list.extend(edge_list)
    # Use an edge_dictionary for mapping the index of the values in the list
    temp_list = [edge_dict.get(item, None) for item in temp_list]

    # Create an incidence matrix using spare matrix for optimise the memory
    in_matrix = coo_matrix(([1] * len(col_indices), (col_indices, temp_list)),
                           shape=(num_vertex, num_edge),
                           dtype=np.uint8)
    del temp_list
    return in_matrix.tocsr()


def top_node_with_most_triangle(matrix, set_vertex):
    if set_vertex:
        global num_edge
        temp = coo_matrix(([1] * num_edge, (range(num_edge), [0] * num_edge)), shape=(num_edge, 1)).tocsr()
        # Filtering the matrix and only keep the elements with value 2
        matrix = matrix.multiply(matrix == 2)
        # Replace all occurrences of 2 with 1
        matrix.data[matrix.data == 2] = 1
        matrix = matrix.dot(temp)
        # Convert spare matrix into 1-dimension array
        node_list = list(zip(set_vertex, matrix[:, 0].toarray().ravel()))
        node_list.sort(key=lambda x: (x[1], x[0]), reverse=True)
        print("Top 5 nodes with most triangles")
        for index in range(5):
            temp = node_list[index]
            if temp[1] > 1:
                print("Node", temp[0], "has", int(temp[1]), "triangles.")
            else:
                print("Node", temp[0], "has", int(temp[1]), "triangle.")
        print(" ")


def read_file():
    val = input("How many lines do you want to read from the file: ")
    val = int(val)
    global edge_list, row_indices, col_indices, vertex_list, vertex_dict, edge_dict, net
    data = pd.read_csv('E:/TÀI LIỆU BK/BTL_CTRR/roadNet-CA_adj.tsv',
                       delimiter='\t',
                       comment='#',
                       header=None,
                       names=['From_Node', 'To_Node'],
                       nrows=val)
    print(data)
    # Convert both column 0 and 1 into a list and add it to "row_indices" list
    # For "vertex_list", sorted the list "row_indices" and convert it into a set
    # so that it would automatically delete all duplicated.
    # Finally, convert it back into a list which is "vertex_list" for later use
    row_indices = data.iloc[:, 0].tolist()
    row_indices.extend(data.iloc[:, 1].tolist())
    vertex_list = list(set(sorted(row_indices)))
    # Create "vertex_dict" which is a dictionary mapped values of "vertex_list" to their positions
    vertex_dict = {value: index for index, value in enumerate(vertex_list)}

    # For "col_indices", do the opposite of the row_indices which is first added the list of column 1 then column 0
    col_indices = data.iloc[:, 1].tolist()
    col_indices.extend(data.iloc[:, 0].tolist())
    row_indices = [vertex_dict.get(item, None) for item in row_indices]
    col_indices = [vertex_dict.get(item, None) for item in col_indices]

    # Create an edge list which a 2-tuples from column "From NodeId" and column "To NodeId" of the dataset
    edge_list = list(zip(data['From_Node'], data['To_Node']))
    temp = sorted(list(edge_list), key=lambda x: (x[0], x[1]))
    edge_dict = {value: index for index, value in enumerate(temp)}
    del temp, data


edge_list, row_indices, col_indices, vertex_list = [], [], [], []
vertex_dict, edge_dict = {}, {}
read_file()
num_vertex = len(vertex_list)
num_edge = len(edge_list)
adjacency_matrix = to_adjacency_matrix()
incidence_matrix = to_incidence_matrix()
del row_indices, col_indices
c = adjacency_matrix.dot(incidence_matrix)      # Calculate matrix C
print("Undirected graph has", num_vertex, "nodes and", num_edge, "edges.")
num_triangle = int(count_triangles(c))
print("The graph has", num_triangle, "triangles.")
list_triangle(num_triangle)
top_node_with_most_triangle(c, vertex_list)

# Draw the graph with edges from .tsv file
net = Network(
    notebook=True,
    cdn_resources="remote",
    bgcolor="#222222",
    font_color="750px",
    height="750px",
    width="100%",
    select_menu=True,
    filter_menu=True
)
G = nx.Graph()
G.add_edges_from(edge_list)
print("k-truss for undirected graph: ")
k_truss_graph = nx.k_truss(G, 3)
print(k_truss_graph)
# Create a network of pyvis from networkx
net.from_nx(G)
display(HTML(net.generate_html()))
# Save the html file of the graph by the name "networkx-pyvis.html"
net.save_graph("networkx-pyvis.html")
HTML(filename="networkx-pyvis.html")
