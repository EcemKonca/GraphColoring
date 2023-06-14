from tkinter import *
import networkx as nx
from matplotlib import pyplot as plt

graph = nx.Graph()
colors_of_nodes = {}
colors = []

window = Tk()
window.title("Node Entry")
window.geometry("500x250")


def color_entry():
    with open("colors.txt", "r") as file:  # the entry of colors
        for line in file:  # colors are first taken from as text and then converted to list
            colors.append(line.strip('\n'))


def colorable(node):
    for color in colors:  # here is the method of coloring the graph
        if valid(node, color):
            return color


# algorithm starts, two adjacent colors will not be same color
def valid(node, color):
    for neighbor in list(graph.neighbors(node)):
        color_of_neighbor = color
        if color_of_neighbor == colors_of_nodes.get(neighbor):
            return False
    return True


def save_nodes():
    text_file = open("nodes.txt", "w")  # nodes are saved as text
    text_file.write(my_text_box.get(1.0, END))
    text_file.close()


def open_new_window():
    new_window = Toplevel(window)  # Toplevel is used to open new window
    new_window.title("Edge Entry")
    new_window.geometry("500x250")
    my_text_box1 = Text(new_window, height=10, width=40)
    my_text_box1.pack()

    def save_edges():
        text_file = open("edges.txt", "w")  # edges are saved as text
        text_file.write(my_text_box1.get(1.0, END))
        text_file.close()

    save_edges()

    edge = Button(new_window, text="Save Edges", command=save_edges)
    edge.pack()
    color = Button(new_window, text="Select Colors", command=main_process)
    color.pack()


def main_process():
    newest_window = Toplevel(window)
    newest_window.title("Add Colors")
    newest_window.geometry("500x250")
    my_text_box2 = Text(newest_window, height=10, width=40)
    my_text_box2.pack()
    label1 = Label(newest_window, text="Please enter the colors and save for to see colored graph with the algorithm.")
    label1.pack()

    def save_colors():
        text_file = open("colors.txt", "w")
        text_file.write(my_text_box2.get(1.0, END))  # save colors as txt
        text_file.close()
        color_entry()
        save_nodes()
        edges = nx.read_edgelist("edges.txt")  # read graph from a list of edges
        nodes = nx.read_adjlist("nodes.txt")
        graph.add_edges_from(edges.edges())  # adding edges to the graph
        graph.add_nodes_from(nodes)

        nodes = ""
        for letter in nodes:
            nodes = nodes + letter

        new_graph = nx.Graph()
        filled_colors = []
        for node in graph.nodes:
            colors_of_nodes[node] = colorable(node)
            given_color = str(colors_of_nodes[node])
            new_graph.add_node(node, color=given_color, style='filled')
            filled_colors.append(given_color)
            nx.draw_networkx(new_graph, node_color=filled_colors, with_labels=True)
            plt.show()

        new_graph.add_edges_from(edges.edges())

        nx.draw_networkx(graph, node_color=filled_colors, with_labels=True)  # draw graph
        plt.show()

    save_colors = Button(newest_window, text="Save Colors", command=save_colors)
    save_colors.pack()


my_text_box = Text(window, height=10, width=40)
label = Label(window, text="Please enter the nodes and save before edge entry.")
my_text_box.pack()
label.pack()

save_nodes_button = Button(window, text="Save Nodes", command=save_nodes)
save_nodes_button.pack()

open_new_window_button = Button(window, text="Add Edges", command=open_new_window)
open_new_window_button.pack()

window.mainloop()
