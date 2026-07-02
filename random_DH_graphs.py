import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sns
import random


# Functions to specify the new edges added for a pendant vertex, true twin, or false twin.
# Takes a graph as input, along with the name of the old twin and new twin vertices.
# Identifies the new edges of the new twin based on the old twin.
# Returns these edges as a list.

def pendant_vertex_edges(G,old_twin,new_twin):
  new_edges = [(old_twin,new_twin)]
  return new_edges

def true_twin_edges(G,old_twin,new_twin):
  new_edges = []
  for neighbor in G.neighbors(old_twin):
    new_edges.append((neighbor,new_twin))
  new_edges.append((old_twin,new_twin))
  return new_edges

def false_twin_edges(G,old_twin,new_twin):
  new_edges = []
  for neighbor in G.neighbors(old_twin):
    new_edges.append((neighbor,new_twin))
  return new_edges


# Function to recgonize whether an input graph is complete (c), star-center (sc), or star-spoke (ss).
# For the star cases, this is with respect to a specified vertex index.
# If a graph is none of these cases, return "other".

def quotient_graph_type(G,vertex_index):

  # Infer the graph parameters
  num_vertices = len(G.nodes())
  num_edges = len(G.edges())

  # Initialize a classfication
  graph_type = "other"

  # Determine complete-ness or star-ness by checking the number of edges.
  # It could also be a non-star tree, but that shouldn't occur in DH case.
  num_complete_edges = (num_vertices * (num_vertices - 1) / 2)
  num_star_edges = (num_vertices - 1)

  if num_edges == num_complete_edges:
    # Complete case
    graph_type = "c"
  elif (num_edges == num_star_edges):
    # Star case (more properly, tree case)
    if (G.degree(vertex_index) == num_edges):
      # Vertex is the center of a star
      graph_type = "sc"
    elif (G.degree(vertex_index) == 1):
      # Vertex is a leaf; assuming this graph is a star, it's a spoke
      graph_type = "ss"

  return graph_type


# Function to construct a random distance-hereditary graph as a NetworkX graph object.
# Also construct the QASST of this graph.
# We will represent the nodes in the QASST as NetworkX graph objects.
# We track the insertion order of these graphs in a separate list since they may be updated.
# User specifies the number of vertices.
# Only 1 possibility if 1 or 2 vertices.

def create_random_DH_graph_and_QASST(num_vertices):

  # Initialize an empty graph for the DH graph and its QASST.
  G = nx.Graph()
  G_qasst = nx.Graph()

  # Make a list to track the insertion order of the nodes.
  # Arbitrarily add an empty graph entry to this list to get around the 0-index issue.
  # I want the list index to match the quotient graph index, which is 1-indexed.
  node_insertion_order_list = [nx.Graph()]

  if (num_vertices == 1):
    # If the user wants a random graph with 1 vertex... give them that.
    G.add_node(1)
    Q1 = G.copy()
    G_qasst.add_node(Q1)
    node_insertion_order_list.append(Q1)
    return G, G_qasst
  else:
    G.add_node(1)
    G.add_node(2)
    G.add_edge(1,2)
    Q1 = G.copy()
    G_qasst.add_node(Q1)
    node_insertion_order_list.append(Q1)
    if (num_vertices == 2):
      return G, G_qasst

    # In the specical case for 3 vertices, there should still only be a single quotient graph.
    # Handle this case separately.
    old_twin = random.choice(list(G.nodes()))
    G.add_node(3)
    # The edges are determined by three cases, chosen at random:
    # the new vertex is a pendant, true twin, or false twin of old_twin.
    # Choose a random integer 1, 2, or 3 and add edges accordingly.
    twin_case = random.randint(1,3)
    if (twin_case == 1):
      new_edges = pendant_vertex_edges(G,old_twin,3)
    elif (twin_case == 2):
      new_edges = false_twin_edges(G,old_twin,3)
    elif (twin_case == 3):
      new_edges = true_twin_edges(G,old_twin,3)

    # Add the edges to the graph accordinly
    G.add_edges_from(new_edges)
    Q1_new = G.copy()
    G_qasst = nx.relabel_nodes(G_qasst, {Q1:Q1_new}, copy=True)
    node_insertion_order_list[1] = Q1_new

    # In the special case we only want a 3 vertex graph, return this now.
    if (num_vertices == 3):
      return G, G_qasst

    # Iterate through the number of vertices and add an edge for each.
    # Also evolve the QASST.
    for i in range(4,num_vertices+1):
      # Choose one of the existing nodes to be "twinned"
      old_twin = random.choice(list(G.nodes()))

      # DEBUG
      #print("Node Insertion Order List:",node_insertion_order_list)

      # Loop through the graphs in the QASST and identify the graph containing old_twin
      for quotient_graph in G_qasst.nodes():
        if old_twin in quotient_graph.nodes():
          Q_old = quotient_graph
          for inserted_graph in node_insertion_order_list:
            if nx.utils.graphs_equal(Q_old,inserted_graph):
              Q_old_index = node_insertion_order_list.index(inserted_graph)
          #DEBUG
          #print("Q_old: vertices",Q_old.nodes(),"edges",Q_old.edges())
          break

      # Count the existing number of quotient graphs, in case we add a new one.
      num_quotient_graphs = len(G_qasst.nodes())

      # Add the new_twin vertex to the graph.
      G.add_node(i)

      # There are several possibilities for the QASST evolution, so involving splitting a quotient graph.
      # In this case, the new split quotient graph has three possibile types.
      # Create graph objects representing these options
      # Intialize a split node based on the index of the old quotient graph.
      new_split_node = "s"+str(Q_old_index)
      old_split_node = "s"+str(num_quotient_graphs+1)

      # Type 1
      Q2_type1 = nx.Graph()
      Q2_type1.add_nodes_from([old_twin,i,new_split_node])
      Q2_type1.add_edges_from([(old_twin,i),(old_twin,new_split_node)])

      # Type 2
      Q2_type2 = nx.Graph()
      Q2_type2.add_nodes_from([old_twin,i,new_split_node])
      Q2_type2.add_edges_from([(new_split_node,old_twin),(new_split_node,i)])

      # Type 3
      Q2_type3 = nx.Graph()
      Q2_type3.add_nodes_from([old_twin,i,new_split_node])
      Q2_type3.add_edges_from([(new_split_node,old_twin),(new_split_node,i),(old_twin,i)])


      # The edges are determined by three cases, chosen at random:
      # the new vertex is a pendant, true twin, or false twin of old_twin.
      # Choose a random integer 1, 2, or 3 and add edges accordingly.
      twin_case = random.randint(1,3)
      if (twin_case == 1):
        new_edges = pendant_vertex_edges(G,old_twin,i)
      elif (twin_case == 2):
        new_edges = false_twin_edges(G,old_twin,i)
      elif (twin_case == 3):
        new_edges = true_twin_edges(G,old_twin,i)

      # Add the edges to the graph accordinly
      G.add_edges_from(new_edges)

      # Evolve the QASST accordingly.
      # This depends on the structure of Q_old quotient graph and the type of twin.
      Q_old_type = quotient_graph_type(Q_old,old_twin)

      # DEBUG
      #print("Iteration ",i,": Q_old_type is",Q_old_type,"; new_twin",i,"is type",twin_case,"of old_twin",old_twin)

      if (Q_old_type == "c"):
        # Q_old is complete:
        if (twin_case == 1):
          # new_twin i is a pendant vertex of old_twin
          # Create a Q1 quotient graph, replacing old_twin by old_split_node
          Q1_new = nx.relabel_nodes(Q_old, {old_twin:old_split_node}, copy=True)
          # Replace Q_old in the QASST by Q1_new via relabling.
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
          # Add the new Q2_type1 quotient graph and add an edge to the QASST.
          Q2_new = Q2_type1.copy()
          G_qasst.add_node(Q2_new)
          G_qasst.add_edge(Q1_new,Q2_new)
          node_insertion_order_list.append(Q2_new)
        elif (twin_case == 2):
          # new_twin i is a false twin of old_twin
          # Create a Q1 quotient graph, replacing old_twin by old_split_node
          Q1_new = nx.relabel_nodes(Q_old, {old_twin:old_split_node}, copy=True)
          # Replace Q_old in the QASST by Q1_new via relabling.
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
          # Add the new Q2_type2 quotient graph and add an edge to the QASST.
          Q2_new = Q2_type2.copy()
          G_qasst.add_node(Q2_new)
          G_qasst.add_edge(Q1_new,Q2_new)
          node_insertion_order_list.append(Q2_new)
        elif (twin_case == 3):
          # new_twin i is a true twin of old_twin
          # Simply add a new node and fully connect to old_twin and its neighbors.
          Q1_new = Q_old.copy()
          Q1_new.add_node(i)
          # DEBUG:
          #print("Neighbors of old twin:",set(Q_old.neighbors(old_twin)))
          for neighbor in Q_old.neighbors(old_twin):
            Q1_new.add_edge(i,neighbor)
            # DEBUG
            #print("Added edge (",i,",",neighbor,")")
          Q1_new.add_edge(i,old_twin)
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
      elif (Q_old_type == "sc"):
        # Q_old is star-center w.r.t. old_twin
        if (twin_case == 1):
          # new_twin i is a pendant vertex of old_twin
          # Just add a new node to Q_old and a single edge connected to old_twin.
          Q1_new = Q_old.copy()
          Q1_new.add_node(i)
          Q1_new.add_edge(i,old_twin)
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
        elif (twin_case == 2):
          # new_twin i is a false twin of old_twin
          # Create a Q1 quotient graph, replacing old_twin by old_split_node
          Q1_new = nx.relabel_nodes(Q_old, {old_twin:old_split_node}, copy=True)
          # Replace Q_old in the QASST by Q1_new via relabling.
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
          # Add the new Q2_type2 quotient graph and add an edge to the QASST.
          Q2_new = Q2_type2.copy()
          G_qasst.add_node(Q2_new)
          G_qasst.add_edge(Q1_new,Q2_new)
          node_insertion_order_list.append(Q2_new)
        elif (twin_case == 3):
          # new_twin i is a true twin of old_twin
          # Create a Q1 quotient graph, replacing old_twin by old_split_node
          Q1_new = nx.relabel_nodes(Q_old, {old_twin:old_split_node}, copy=True)
          # Replace Q_old in the QASST by Q1_new via relabling.
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
          # Add the new Q2_type3 quotient graph and add an edge to the QASST.
          Q2_new = Q2_type3.copy()
          G_qasst.add_node(Q2_new)
          G_qasst.add_edge(Q1_new,Q2_new)
          node_insertion_order_list.append(Q2_new)
      elif (Q_old_type == "ss"):
        # Q_old is star-spoke w.r.t. old_twin
        if (twin_case == 1):
          # new_twin i is a pendant vertex of old_twin
          # Create a Q1 quotient graph, replacing old_twin by old_split_node
          Q1_new = nx.relabel_nodes(Q_old, {old_twin:old_split_node}, copy=True)
          # Replace Q_old in the QASST by Q1_new via relabling.
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
          # Add the new Q2_type1 quotient graph and add an edge to the QASST.
          Q2_new = Q2_type1.copy()
          G_qasst.add_node(Q2_new)
          G_qasst.add_edge(Q1_new,Q2_new)
          node_insertion_order_list.append(Q2_new)
        elif (twin_case == 2):
          # new_twin i is a false twin of old_twin
          # Simply add a new node and fully connect to the neighbors of old_twin.
          Q1_new = Q_old.copy()
          Q1_new.add_node(i)
          for neighbor in Q_old.neighbors(old_twin):
            Q1_new.add_edge(i,neighbor)
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
        elif (twin_case == 3):
          # new_twin i is a true twin of old_twin
          # Create a Q1 quotient graph, replacing old_twin by old_split_node
          Q1_new = nx.relabel_nodes(Q_old, {old_twin:old_split_node}, copy=True)
          # Replace Q_old in the QASST by Q1_new via relabling.
          G_qasst = nx.relabel_nodes(G_qasst, {Q_old:Q1_new}, copy=True)
          node_insertion_order_list[Q_old_index] = Q1_new
          # Add the new Q2_type3 quotient graph and add an edge to the QASST.
          Q2_new = Q2_type3.copy()
          G_qasst.add_node(Q2_new)
          G_qasst.add_edge(Q1_new,Q2_new)
          node_insertion_order_list.append(Q2_new)

    return G, G_qasst

