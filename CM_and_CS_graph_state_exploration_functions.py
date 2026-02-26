import numpy as np
import sympy
from IPython.core.display import struct
import networkx as nx
import random
from re import L



# Recursive function to create a generator object listing intger partitions.
# (This function was written by Google's generative AI)

def generate_partitions(n, max_val=None):
    if max_val is None:
        max_val = n

    if n == 0:
        yield []
        return

    for i in range(min(max_val, n), 0, -1):
        for p in generate_partitions(n - i, i):
            yield [i] + p


def construct_list_of_multipartite_group_sizes(n,ni_min=2,k_min=3,k_max=7):

  # Initialize an empty list to store the group sizes
  group_sizes_list = []

  # Skip those partitions with less than k_min groups or a group size of ni_min.
  for partition in generate_partitions(n):
    k = len(partition)
    skip = False
    if ((k >= k_min) and (k <= k_max)):
      for i in range(k):
        if partition[i] < ni_min:
          skip = True
      if skip == False:
        group_sizes_list.append(partition)

  return group_sizes_list


def create_product_expression(k):

  # Creata list of variables for n1,...nk
  variable_names = []
  for i in range(k):
    temp_var = "n"+str(i+1)
    variable_names.append(temp_var)

  symbol_objects = [sympy.symbols(name) for name in variable_names]

  # DEBUG:
  #print("Variables names:",variable_names)
  #print("SymPy symbols:",symbol_objects)

  # Create an expression to represent the full expansion of (n1+1)*...*(nk+1)
  product_expression = 1
  for i in range(k):
    product_expression = product_expression * (symbol_objects[i] + 1)

  # DEBUG:
  #print("Expression:",product_expression)
  #print("Expansion:",sympy.expand(product_expression))

  return product_expression


def create_odd_summation_expression(k):

  # Create the fully expanded expression
  product_expression = sympy.expand(create_product_expression(k))

  # DEBUG:
  #print("Fully expanded expression:",product_expression)
  #print("Summands:",product_expression.args)

  # Create a new expression summing just the odd terms.
  # Do this by checking each how many different variables are in each term.
  odd_terms = []
  odd_summation_expression = 0

  for term in product_expression.args:
    # DEBUG
    #print(term.free_symbols)
    if len(term.free_symbols) % 2 == 1:
      odd_terms.append(term)
      odd_summation_expression = odd_summation_expression + term

  # DEBUG
  #print("List of odd product terms:",odd_terms)
  #print("Summation of odd product terms:",odd_summation_expression)

  return odd_summation_expression


def create_even_summation_expression(k):

  # Create the fully expanded expression
  product_expression = sympy.expand(create_product_expression(k))

  # DEBUG:
  #print("Fully expanded expression:",product_expression)
  #print("Summands:",product_expression.args)

  # Create a new expression summing just the even terms.
  # Do this by checking each how many different variables are in each term.
  even_terms = []
  even_summation_expression = 0

  for term in product_expression.args:
    # DEBUG
    #print(term.free_symbols)
    if len(term.free_symbols) % 2 == 0:
      even_terms.append(term)
      even_summation_expression = even_summation_expression + term

  # DEBUG
  #print("List of odd product terms:",even_terms)
  #print("Summation of odd product terms:",even_summation_expression)

  return even_summation_expression


def create_summation_product_expression(k):

  # Creata list of variables for n1,...nk
  variable_names = []
  for i in range(k):
    temp_var = "n"+str(i+1)
    variable_names.append(temp_var)

  symbol_objects = [sympy.symbols(name) for name in variable_names]

  # Nest some loops to create the summation of the products.
  temp_sum = 0
  for j in range(k):
    temp_product = 1
    for i in range(k):
      if i != j:
        temp_product = temp_product * (symbol_objects[i] + 1)
    temp_sum = temp_sum + temp_product

  # DEBUG:
  #print("Final expression:",temp_sum)

  return temp_sum


def evaluate_sum_of_odd_products_formula(list_of_group_sizes):

  # Infer the total number of groups vertices from the list.
  # Also infer the total number of vertices.
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)

  # Create the expression, then evaulate it using the list inputs.
  odd_summation_expression = create_odd_summation_expression(k)
  summation_product_expression = create_summation_product_expression(k)
  combined_expression = odd_summation_expression + summation_product_expression
  free_symbol_list = list(combined_expression.free_symbols)

  # DEBUG
  #print("Odd summation:",odd_summation_expression)
  #print("Summation product:",summation_product_expression)
  #print("Combined expression:",combined_expression)
  #print("Free variables:",free_symbol_list)

  list_of_substitution_pairs = []
  for i in range(k):
    list_of_substitution_pairs.append((free_symbol_list[i],list_of_group_sizes[i]))
  evaluated_expression = combined_expression.subs(list_of_substitution_pairs)

  # DEBUG
  #print("Expression after subsitution",evaluated_expression)

  return evaluated_expression


def evaluate_sum_of_even_products_formula(list_of_group_sizes):

  # Infer the total number of groups vertices from the list.
  # Also infer the total number of vertices.
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)

  # Create the expression, then evaulate it using the list inputs.
  even_summation_expression = create_even_summation_expression(k)
  summation_product_expression = create_summation_product_expression(k)
  combined_expression = even_summation_expression + summation_product_expression
  free_symbol_list = list(combined_expression.free_symbols)

  # DEBUG
  #print("Even summation:",even_summation_expression)
  #print("Summation product:",summation_product_expression)
  #print("Combined expression:",combined_expression)
  #print("Free variables:",free_symbol_list)

  list_of_substitution_pairs = []
  for i in range(k):
    list_of_substitution_pairs.append((free_symbol_list[i],list_of_group_sizes[i]))
  evaluated_expression = combined_expression.subs(list_of_substitution_pairs)

  # DEBUG
  #print("Expression after subsitution",evaluated_expression)

  return evaluated_expression
  
  
def determine_LC_orbit_size_for_CM_or_CS(list_of_group_sizes,type):
    
    if (type=="CM"):
        return evaluate_sum_of_even_products_formula(list_of_group_sizes)
    elif (type=="CS"):
        return evaluate_sum_of_odd_products_formula(list_of_group_sizes)
    else:
        print("Please specify LC orbit class type, CM or CS.")


def comparison_formula(k,nj):
  return ((nj-1)*(k-1) + ((nj-2)*(nj-1)/2) - ((k-2)*(k-1)/2))


def sum_minus_one(list_of_group_sizes):
  k = len(list_of_group_sizes)
  sum_total = 0
  for i in range(k):
    sum_total = sum_total + (list_of_group_sizes[i] - 1)
  return sum_total


def sum_minus_one_exclude_min(list_of_group_sizes):
  k = len(list_of_group_sizes)
  nj = min(list_of_group_sizes)
  j = list_of_group_sizes.index(nj)
  sum_total = 0
  for i in range(k):
    if (i != j):
      sum_total = sum_total + (list_of_group_sizes[i] - 1)
  return sum_total


def minimal_edge_count_complete_multipartite_orbit(list_of_group_sizes):

  # Infer the total number of groups vertices from the list.
  # Also infer the total number of vertices and some derived terms.
  k = len(list_of_group_sizes)
  nj = min(list_of_group_sizes)
  comp_value = comparison_formula(k,nj)

  # Initialize a number of the minimal edge count.
  # Also initalize a parameter for the case of the structure.
  min_edge = 0
  structure_case = 0

  if ((k%2 == 0) and (comp_value >= 0)):
    structure_case = 1
    min_edge = (k*(k-1)/2) + sum_minus_one(list_of_group_sizes)
  elif ((k%2 == 0) and (comp_value < 0)):
    structure_case = 2
    min_edge = nj*(k-1) + (nj*(nj-1)/2) + sum_minus_one_exclude_min(list_of_group_sizes)
  elif (k%2 == 1):
    structure_case = 3
    min_edge = nj*(k-1) + sum_minus_one_exclude_min(list_of_group_sizes)

  # Return the minimal edge count and the structure
  return min_edge, structure_case


def minimal_edge_count_and_structure_complete_multipartite_orbit(list_of_group_sizes):

  # Infer the parameters
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)
  nj = min(list_of_group_sizes)
  j = list_of_group_sizes.index(nj)

  # Infer the number of minimal edges and the structure case
  min_edge, structure_case = minimal_edge_count_complete_multipartite_orbit(list_of_group_sizes)

  # Initilize a string to represent the structure case
  #structure_string_list = []
  structure_dict = {}

  if (structure_case == 1):
    #structure_string_list.append("Q0 = c")
    structure_dict["Q0"] = "c"
    for i in range(k):
      #structure_string_list.append("Q"+str(i+1)+" = ss")
      structure_dict["Q"+str(i+1)] = "ss"

  elif (structure_case == 2):
    #tructure_string_list.append("Q0 = sc"+str(j+1))
    structure_dict["Q0"] = "sc"+str(j+1)
    for i in range(k):
      #structure_string_list.append("Q"+str(i+1)+" = ss")
      structure_dict["Q"+str(i+1)] = "ss"
    #structure_string_list[j+1] = "Q"+str(j+1)+" = c"
    structure_dict["Q"+str(j+1)] = "c"

  elif (structure_case == 3):
    #structure_string_list.append("Q0 = sc"+str(j+1))
    structure_dict["Q0"] = "sc"+str(j+1)
    for i in range(k):
      #structure_string_list.append("Q"+str(i+1)+" = ss")
      structure_dict["Q"+str(i+1)] = "ss"
    #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
    structure_dict["Q"+str(j+1)] = "sc"

  return min_edge, structure_dict


def minimal_edge_count_clique_star_orbit(list_of_group_sizes):

  # Infer the total number of groups vertices from the list.
  # Also infer the total number of vertices and some derived terms.
  k = len(list_of_group_sizes)
  nj = min(list_of_group_sizes)
  comp_value = comparison_formula(k,nj)

  # Initialize a number of the minimal edge count.
  # Also initalize a parameter for the case of the structure.
  min_edge = 0
  structure_case = 0

  if (k%2 == 0):
    structure_case = 1
    min_edge = nj*(k-1) + sum_minus_one_exclude_min(list_of_group_sizes)
  elif ((k%2 == 1) and (comp_value >= 0)):
    structure_case = 2
    min_edge = (k*(k-1)/2) + sum_minus_one(list_of_group_sizes)
  elif ((k%2 == 1) and (comp_value < 0)):
    structure_case = 3
    min_edge = nj*(k-1) + (nj*(nj-1)/2) + sum_minus_one_exclude_min(list_of_group_sizes)

  # Return the minimal edge count and the structure
  return min_edge, structure_case


def minimal_edge_count_and_structure_clique_star_orbit(list_of_group_sizes):

  # Infer the parameters
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)
  nj = min(list_of_group_sizes)
  j = list_of_group_sizes.index(nj)

  # Infer the number of minimal edges and the structure case
  min_edge, structure_case = minimal_edge_count_clique_star_orbit(list_of_group_sizes)

  # Initilize a string to represent the structure case
  #structure_string_list = []
  structure_dict = {}

  if (structure_case == 1):
    #structure_string_list.append("Q0 = sc"+str(j+1))
    structure_dict["Q0"] = "sc"+str(j+1)
    for i in range(k):
      #structure_string_list.append("Q"+str(i+1)+" = ss")
      structure_dict["Q"+str(i+1)] = "ss"
    #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
    structure_dict["Q"+str(j+1)] = "sc"

  elif (structure_case == 2):
    #structure_string_list.append("Q0 = c")
    structure_dict["Q0"] = "c"
    for i in range(k):
      #structure_string_list.append("Q"+str(i+1)+" = ss")
      structure_dict["Q"+str(i+1)] = "ss"

  elif (structure_case == 3):
    #structure_string_list.append("Q0 = sc"+str(j+1))
    structure_dict["Q0"] = "sc"+str(j+1)
    for i in range(k):
      #structure_string_list.append("Q"+str(i+1)+" = ss")
      structure_dict["Q"+str(i+1)] = "ss"
    #structure_string_list[j+1] = "Q"+str(j+1)+" = c"
    structure_dict["Q"+str(j+1)] = "c"

  return min_edge, structure_dict


def Delta_G1(list_of_group_sizes):
  # Infer certain parameters
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)
  nj = min(list_of_group_sizes) # the smallest entry
  j = list_of_group_sizes.index(nj) # index of the smallest entry
  list_of_group_sizes_reduced = list_of_group_sizes.copy()
  nj_temp = list_of_group_sizes_reduced.pop(j)
  nt = min(list_of_group_sizes_reduced) # the second smallest entry
  t = list_of_group_sizes.index(nt) # index in the original list
  nl = max(list_of_group_sizes) # the largest entry
  l = list_of_group_sizes.index(nl) # index of the largest entry
  # Note: it's okay if the index matches for some, we actually won't use it.

  # Compute the value of Delta_G_1
  case_list = [
      (nl+k-2),
      max((k-1+nt),(nl-1+nj)),
      max((nj+k-2),(nl-1+nj))
  ]

  delta_G = min(case_list)
  case_index = case_list.index(delta_G)+1

  return (delta_G,case_index)


def Delta_G2(list_of_group_sizes):
  # Infer certain parameters
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)
  nj = min(list_of_group_sizes) # the smallest entry
  j = list_of_group_sizes.index(nj) # index of the smallest entry
  list_of_group_sizes_reduced = list_of_group_sizes.copy()
  nj_temp = list_of_group_sizes_reduced.pop(j)
  nt = min(list_of_group_sizes_reduced) # the second smallest entry
  t = list_of_group_sizes.index(nt) # index in the original list
  nl = max(list_of_group_sizes) # the largest entry
  l = list_of_group_sizes.index(nl) # index of the largest entry
  # Note: it's okay if the index matches for some, we actually won't use it.

  # Compute the value of Delta_G_1
  case_list = [
      (nl+nj+k-3),
      max((k-1),(nl-1+nj)),
      max((nj+nt+k-3),(nl-1+nj))
  ]

  delta_G = min(case_list)
  case_index = case_list.index(delta_G)+1

  return (delta_G,case_index)


def determine_minimal_Delta_G_complete_multipartite(list_of_group_sizes):
  # Infer certain parameters
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)
  nj = min(list_of_group_sizes) # the smallest entry
  j = list_of_group_sizes.index(nj) # index of the smallest entry
  list_of_group_sizes_reduced = list_of_group_sizes.copy()
  nj_temp = list_of_group_sizes_reduced.pop(j)
  nt = min(list_of_group_sizes_reduced) # the second smallest entry
  t = list_of_group_sizes.index(nt) # index in the original list
  if (t == j):
    # If t matches j (possible when nt=nj since it chooses the first index),
    # fix this by shifting t by 1; this is okay because of how sizes are ordered.
    t = t + 1

  # Initilize a string to represent the structure case
  #structure_string_list = []
  structure_dict = {}

  if (k%2 == 0):
    min_Delta_G, structure_case = Delta_G1(list_of_group_sizes)

    if (structure_case == 1):
      #structure_string_list.append("Q0 = c")
      structure_dict["Q0"] = "c"
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"

    elif (structure_case == 2):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
      #structure_string_list[t+1] = "Q"+str(t+1)+" = c"
      structure_dict["Q"+str(j+1)] = "sc"
      structure_dict["Q"+str(t+1)] = "c"

    elif (structure_case == 3):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = c"
      structure_dict["Q"+str(j+1)] = "c"

  elif (k%2 == 1):
    min_Delta_G, structure_case = Delta_G2(list_of_group_sizes)

    if (structure_case == 1):
      #structure_string_list.append("Q0 = c")
      structure_dict["Q0"] = "c"
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
      structure_dict["Q"+str(j+1)] = "sc"

    elif (structure_case == 2):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
      structure_dict["Q"+str(j+1)] = "sc"

    elif (structure_case == 3):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = c"
      #structure_string_list[t+1] = "Q"+str(t+1)+" = c"
      structure_dict["Q"+str(j+1)] = "c"
      structure_dict["Q"+str(t+1)] = "c"

  return min_Delta_G, structure_dict


# Note that the cases for the clique-star are identical to those for the
# complete multipartite graph, except reveresed for the parity of k.

def determine_minimal_Delta_G_clique_star(list_of_group_sizes):
  # Infer certain parameters
  k = len(list_of_group_sizes)
  n = sum(list_of_group_sizes)
  nj = min(list_of_group_sizes) # the smallest entry
  j = list_of_group_sizes.index(nj) # index of the smallest entry
  list_of_group_sizes_reduced = list_of_group_sizes.copy()
  nj_temp = list_of_group_sizes_reduced.pop(j)
  nt = min(list_of_group_sizes_reduced) # the second smallest entry
  t = list_of_group_sizes.index(nt) # index in the original list
  if (t == j):
    # If t matches j (possible when nt=nj since it chooses the first index),
    # fix this by shifting t by 1; this is okay because of how sizes are ordered.
    t = t + 1

  # Initilize a string to represent the structure case
  #structure_string_list = []
  structure_dict = {}

  if (k%2 == 1):
    min_Delta_G, structure_case = Delta_G1(list_of_group_sizes)

    if (structure_case == 1):
      #structure_string_list.append("Q0 = c")
      structure_dict["Q0"] = "c"
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"

    elif (structure_case == 2):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
      #structure_string_list[t+1] = "Q"+str(t+1)+" = c"
      structure_dict["Q"+str(j+1)] = "sc"
      structure_dict["Q"+str(t+1)] = "c"

    elif (structure_case == 3):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = c"
      structure_dict["Q"+str(j+1)] = "c"

  elif (k%2 == 0):
    min_Delta_G, structure_case = Delta_G2(list_of_group_sizes)

    if (structure_case == 1):
      #structure_string_list.append("Q0 = c")
      structure_dict["Q0"] = "c"
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
      structure_dict["Q"+str(j+1)] = "sc"

    elif (structure_case == 2):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = sc"
      structure_dict["Q"+str(j+1)] = "sc"

    elif (structure_case == 3):
      #structure_string_list.append("Q0 = sc"+str(j+1))
      structure_dict["Q0"] = "sc"+str(j+1)
      for i in range(k):
        #structure_string_list.append("Q"+str(i+1)+" = ss")
        structure_dict["Q"+str(i+1)] = "ss"
      #structure_string_list[j+1] = "Q"+str(j+1)+" = c"
      #structure_string_list[t+1] = "Q"+str(t+1)+" = c"
      structure_dict["Q"+str(j+1)] = "c"
      structure_dict["Q"+str(t+1)] = "c"

  return min_Delta_G, structure_dict


def compare_minimal_edge_with_split_fuse_complete_multipartite(list_of_group_sizes):

  # Infer some parameters
  n = sum(list_of_group_sizes)
  k = len(list_of_group_sizes)
  split_fuse_count = n + (2*(k+1)) - 3

  decomposition_obj = minimal_edge_count_and_structure_complete_multipartite_orbit(list_of_group_sizes)
  min_edge = decomposition_obj[0]

  if (split_fuse_count < min_edge):
    print("Better split-fuse found! SF=",split_fuse_count,", min_edge=",min_edge)
    print(list_of_group_sizes)
    print(decomposition_obj[1])

  return None



def compare_minimal_edge_with_split_fuse_clique_star(list_of_group_sizes):

  # Infer some parameters
  n = sum(list_of_group_sizes)
  k = len(list_of_group_sizes)
  split_fuse_count = n + (2*(k+1)) - 3

  decomposition_obj = minimal_edge_count_and_structure_clique_star_orbit(list_of_group_sizes)
  min_edge = decomposition_obj[0]

  if (split_fuse_count < min_edge):
    print("Better split-fuse found! SF=",split_fuse_count,", min_edge=",min_edge)
    print(list_of_group_sizes)
    print(decomposition_obj[1])

  return None


def compute_split_fuse_parameters_for_complete_multipartite(list_of_group_sizes):

  # Infer base parameters
  n = sum(list_of_group_sizes)
  k = len(list_of_group_sizes)

  total_CZ = n + (2*(k+1)) - 3
  total_time_steps = 1 + max(k,max(list_of_group_sizes)+1)
  qubit_count = n + (2*(k+1)) - 2
  aux_qubits = qubit_count - n

  #print("Group Sizes:",list_of_group_sizes)
  #print("CZs: "+str(total_CZ)+
  #      "\ntime steps: "+str(total_time_steps)+
  #      "\nqubits: "+str(qubit_count)+
  #      " aux: "+str(aux_qubits)+"\n"
  #      )

  return total_CZ, total_time_steps, qubit_count, aux_qubits


# Function to write down a human-readable composition of LC transformation.
# Keeping with function-composition right-to-left notation, we reverse the list.
# Use the letter "o" in place of function composition symbol.

def write_pretty_LC_transformation(LC_class,LC_transformation_list):

  # Initialize an empty string to write down the transformation as a composition.
  LC_trans_string = ""
  if (LC_class == "CM"):
    print("LC transformation from Kn1,...,nk to graph:")
    for i in reversed(LC_transformation_list):
      LC_trans_string = LC_trans_string + "c"+str(i)+ " o "

  elif (LC_class == "CS"):
    print("LC transformation from CS^1n1,...,nk to graph:")
    for i in reversed(LC_transformation_list):
      LC_trans_string = LC_trans_string + "c"+str(i)+ " o "


  # Return the string, clipping the last three unneeded symbols.
  return LC_trans_string[:-3]


# Function to classify a graph based on its quotient graph decomposition.
# Also finds a transformation to/from the complete multipartite or clique-star.
# Requires the list of group sizes and a dictionary of their structure.
# For k groups of vertices n1,...,nk, there must be k+1 quotient graphs Q0,Q1,...,Qk.
# The dictionary of quotient graph structures must have keys "Q0", "Q1", etc.
# The values in these must be "c" or "sc1", "sc2," etc. for "Q0"
# For the remaining quotient graphs, they must be "c", "sc", or "ss".
# Assumes the a correct split decomposition (that all splits are strong).

# Input:
# list_of_group_sizes: the sizes of groups of vertices
# dict_of_quotient_graphs: the structure of each quotient graph

# Output:
# LC equivalence class representative (complete multipartite or clique-star)
# A transformation from the representative to the input graph
# A transformation from the input graph to the representative

def find_LC_transformation_for_graph(list_of_group_sizes,dict_of_quotient_graphs):

  # Infer some parameters
  n = sum(list_of_group_sizes)
  k = len(list_of_group_sizes)

  # Intialize a paramter to track where Q0 points, if not c.
  # Also initialize an empty string to determine the equivalence class.
  center_point_index = 0
  LC_class = ""

  if (len(dict_of_quotient_graphs) != (k+1)):
    print("ERROR: mismatched length of inputs, should be k+1 quotient graphs")
    return
  for (key,value) in dict_of_quotient_graphs.items():
    if (key == "Q0"):
      if ((value != "c") and (value[0:2] != "sc")):
        print("ERROR: Q0 must be c or sci")
        return
      elif (value[0:2] == "sc"):
        center_point_index = int(value[2:])
    else:
      if ((value != "c") and (value != "sc") and (value != "ss")):
        print("ERROR: Qi quotient graphs must be c, sc, or ss")
        return

    # Infer the indices of the vertices based on their groups.
    # Start from 1, and increase sequentially.
    dict_of_vertex_indices = dict()
    last_index = 0
    for (key,value) in dict_of_quotient_graphs.items():
      dict_of_vertex_indices[key] = []
      ni_index = int(key[1:])
      if (ni_index == 0):
        ni_size = 0
      else:
        ni_size = list_of_group_sizes[ni_index-1]
      for i in range(ni_size):
        last_index += 1
        dict_of_vertex_indices[key].append(last_index)

    # DEBUG
    #print("Dictionary of vertex indices")
    #print(dict_of_vertex_indices)

    # Count the number of quotient graphs which are ss
    ss_count = 0
    ss_index_set_I = set()
    for (key,value) in dict_of_quotient_graphs.items():
      if (value == "ss"):
        ss_count += 1
        ss_index_set_I.add(int(key[1:]))

    # DEBUG
    #print(ss_count, ss_index_set_I)

    # Initialize a list to track the LC transformations.
    # This is a list of functions to compose, starting from the first entry.
    LC_transformation_list = []

    # Break into cases based on the structure of Q0,Q1,...,Qk
    if (dict_of_quotient_graphs["Q0"] == "c"):
      # Case 1: Q0 is c
      if (len(ss_index_set_I)%2 == 0):
        # Even length implies complete multipartite case
        print("Graph is LC equivalent to complete multipartite.")
        LC_class = "CM"
        temp_I = ss_index_set_I.copy()
        while (len(temp_I) > 0):
          index1 = temp_I.pop()
          index2 = temp_I.pop()
          v1 = dict_of_vertex_indices["Q"+str(index1)][0]
          v2 = dict_of_vertex_indices["Q"+str(index2)][0]
          edge_pivot = [v1,v2,v1]
          LC_transformation_list = LC_transformation_list + edge_pivot

      else:
        # Odd length implies clique-star case
        print("Graph is LC equivalent to clique-star.")
        LC_class = "CS"
        temp_I = ss_index_set_I.copy()

        # By default, the clique-center has index 1
        # Remove this from the set of indices (if it's there)
        clique_center_index = 1
        clique_center_v = dict_of_vertex_indices["Q"+str(clique_center_index)][0]
        temp_I.remove(clique_center_index)
        while (len(temp_I) > 0):
          index1 = temp_I.pop()
          v1 = dict_of_vertex_indices["Q"+str(index1)][0]
          LC_transformation_list.append(v1)
        # Force the last transformation to use the center index.
        LC_transformation_list.append(clique_center_v)

    elif (dict_of_quotient_graphs["Q0"][0:2] == "sc"):

      # Infer a vertex in the center and remove it from I
      center_index = int(dict_of_quotient_graphs["Q0"][2:])
      center_type = dict_of_quotient_graphs["Q"+str(center_index)]
      center_v = dict_of_vertex_indices["Q"+str(center_index)][0]

      # DEBUG
      #print(center_index,center_type)

      if (center_type == "sc"):
        # Case 2: Qj is sc
        if (len(ss_index_set_I)%2 == 0):
          # Even length implies complete multipartite case
          print("Graph is LC equivalent to complete multipartite.")
          LC_class = "CM"
          LC_transformation_list.append(center_v)
          temp_I = ss_index_set_I.copy()
          while (len(temp_I) > 0):
            index1 = temp_I.pop()
            v1 = dict_of_vertex_indices["Q"+str(index1)][0]
            LC_transformation_list.append(v1)

        else:
          # Odd length implies clique-star case
          print("Graph is LC equivalent to clique-star.")
          LC_class = "CS"
          # If j != 1, use an edge pivot to shift the clique-center.
          if (center_index != 1):
            v1 = dict_of_vertex_indices["Q1"][0]
            v2 = dict_of_vertex_indices["Q"+str(center_index)][0]
            edge_pivot = [v1,v2,v1]
            LC_transformation_list = LC_transformation_list + edge_pivot

          temp_I = ss_index_set_I.copy()
          while (len(temp_I) > 0):
            index1 = temp_I.pop()
            v1 = dict_of_vertex_indices["Q"+str(index1)][0]
            LC_transformation_list.append(v1)


      elif (center_type == "c"):
        # Case 3: Qj is c
        if (len(ss_index_set_I)%2 == 1):
          # Odd length implies multipartite case
          print("Graph is LC equivalent to complete multipartite.")
          LC_class = "CM"
          LC_transformation_list.append(center_v)
          temp_I = ss_index_set_I.copy()
          while (len(temp_I) > 0):
            index1 = temp_I.pop()
            v1 = dict_of_vertex_indices["Q"+str(index1)][0]
            LC_transformation_list.append(v1)

        else:
          # Even length implies clique-star case
          print("Graph is LC equivalent to clique-star.")
          LC_class = "CS"
          # If j != 1, use an edge pivot to shift the clique-center.
          if (center_index != 1):
            v1 = dict_of_vertex_indices["Q1"][0]
            v2 = dict_of_vertex_indices["Q"+str(center_index)][0]
            edge_pivot = [v1,v2,v1]
            LC_transformation_list = LC_transformation_list + edge_pivot

          temp_I = ss_index_set_I.copy()
          while (len(temp_I) > 0):
            index1 = temp_I.pop()
            v1 = dict_of_vertex_indices["Q"+str(index1)][0]
            LC_transformation_list.append(v1)

    # Write down the LC transformation in a human readable format
    write_pretty_LC_transformation(LC_class,LC_transformation_list)

    return LC_class, LC_transformation_list


# A function to compute the graph obtained after a "type-II fusion".
# Takes two graph objects as input, and a node from each graph to fuse on.
# Outputs a new graph object obtained by fully joining the neighbors of one node
# to the neihghbors of the other, and then deleting the two nodes in question.
# The nodes in each input graph should have unique labels (no labels in common);
# these labels will be inhereted by the new graph.

def type_II_fusion(G1,v1,G2,v2):

  # Intialize a graph object using all of the nodes and edges from G1 and G2.
  # Note that G1 and G2 must not have overalapping label names for nodes.
  G_fuse = nx.Graph()
  G_fuse.add_nodes_from(G1)
  G_fuse.add_edges_from(G1.edges)
  G_fuse.add_nodes_from(G2)
  G_fuse.add_edges_from(G2.edges)

  # Iterate through the neighbors of v1,
  # then add and edge to each neighbor of v2.
  for nb1 in list(G_fuse.neighbors(v1)):
    for nb2 in list(G_fuse.neighbors(v2)):
      G_fuse.add_edge(nb1,nb2)

  # Finally, delete the two fusion nodes
  G_fuse.remove_node(v1)
  G_fuse.remove_node(v2)

  return G_fuse


# Function to build the QASST representation of a CM or CS graph.
# This is based on list of group sizes and a dictionary describing
# the structure of each quotient graph ("c", "sc", "ss", or "sci").
# Returns a graph-labeled tree for the QASST as output.
# This is a Networkx graph whose nodes are graphs.

def construct_CM_or_CS_QASST(list_of_group_sizes,quotient_graph_dict):

  # Infer the number of quotient graphs (add 1 for the central graph)
  k = len(list_of_group_sizes) + 1
  
  # Initialize a dictionary for the QASST graph objects.
  # Also intialize a Networkx graph object for the QASST.
  qasst_dict = {}
  qasst = nx.Graph()

  # Initialize a variable to count leaf-nodes.
  leaf_node_count = 0

  # Iterate through the dictionary of quotient graph structures.
  # Construct a graph for each, using the key as the graph name.
  for (key,value) in quotient_graph_dict.items():
    # DEBUG
    #print(key, value)

    # Intialize a quotient graph oject.
    # This will be stored later in a dictionary.
    Q = nx.Graph()

    # Infer the index of the quotient graph by stripping off the Q.
    # The structure is determined by the value.
    Qindex = int(key[1:])
    Qstruct = value

    # In the special case where the index is 0, this is the central quotient.
    # We handle this case separately, then build the others.
    if (Qindex == 0):
      # Initialize nodes for all the spoke quotient graphs.
      for i in range(1,k):
        Q.add_node("s"+str(i))
      # Build the central quotient graph depending on the cases.
      if (Qstruct == "c"):
        # Complete graph case; add all edges.
        for v1 in Q.nodes:
          for v2 in Q.nodes:
            # Add all pairs of nodes, exluding self loops.
            # As a set, ading the same edge twice doesn't hurt anything.
            if (v1 != v2):
              Q.add_edge(v1,v2)
      else:
        # If Q0 is not complete, it points towards some Qi, indicated as "sci".
        # Infer the direction it points by stripping off the digit.
        c_dir = int(Qstruct[2:])
        vc = "s"+str(c_dir)
        # This index gives the center of the star.
        # Attach all other nodes to this one.
        for v in Q.nodes:
          if (v != vc):
            Q.add_edge(vc,v)

    else:
      # Build the spoke quotient graph depending on the cases.
      # Add a single split node "s0".
      Q.add_node("s0")

      # Infer the number of leaf nodes from the list of group sizes.
      # Add a node for each of these.
      num_Q_leaf_nodes = list_of_group_sizes[Qindex-1]
      for i in range(num_Q_leaf_nodes):
        # Count starting from 1.
        leaf_node_count += 1
        Q.add_node(leaf_node_count)

      # Three are three cases for edges, depending on the structure of Qi.
      if (Qstruct == "c"):
        # Build a complete graph.
        for v1 in Q.nodes:
          for v2 in Q.nodes:
            # Add all pairs of nodes, exluding self loops.
            # As a set, ading the same edge twice doesn't hurt anything.
            if (v1 != v2):
              Q.add_edge(v1,v2)

      elif (Qstruct == "sc"):
        # Build a star graph with the split-node as center.
        for v in Q.nodes:
          if (v != "s0"):
            Q.add_edge("s0",v)

      elif (Qstruct == "ss"):
        # Build a star graph with a leaf-node as center.
        # By default, we will choose the last indexed leaf-node.
        # Any other choice is isomorphic by relabling.
        for v in Q.nodes:
          if (v != leaf_node_count):
            Q.add_edge(leaf_node_count,v)

    
    # Add the quotient graph to the dictionary and qasst graph
    qasst_dict[key] = Q
    qasst.add_node(Q)

  # Next, build a Nextworkx graph object with these quotients as vertices.
  # Use "Q0" as central node, attach an edge to every "Qi".
  for (key,value) in qasst_dict.items():
    # Only add edge when the key is not "Q0".
    if (key != "Q0"):
      qasst.add_edge(qasst_dict["Q0"],qasst_dict[key])

  return qasst_dict, qasst


# Function to fuse all the quotient graphs together for a CM or CS QASST.
# This is defined for something QASST-equivalent to a complete multipartite.
# The QASST consists of central Q0 and spokes Q1,...,Qk.
# Takes a QASST dictioanry as input.
# Return a Networkx graph as output.

def fuse_CM_or_CS_qasst(qasst_dict):

  # Initialize a graph as the central quasst.
  G = qasst_dict["Q0"]

  # Loop through all quotient graphs except Q0.
  for (key,value) in qasst_dict.items():
    if (key != "Q0"):
      # Infer the parameters of the graphs
      Qindex = int(key[1:])
      v1 = "s"+str(Qindex)
      Qi = value
      v2 = "s0"

      # Fuse Q0 and Qi
      G = type_II_fusion(G,v1,Qi,v2)

  return G


# Function to build a randomized QASST for a CM or CS graph.
# Specify the number of vertices n and the LC type ("CM" or "CS").
# Return a list of group sizes and QASST dictionary.

def build_random_CM_or_CS_lc_equivalent_qasst_dict(n,type,ni_min=2,k_min=3,k_max=7):

  # Initialize a QASST dictionary.
  qasst_dict = {}

  # First, generate all integer partitions.
  list_of_int_partitions = construct_list_of_multipartite_group_sizes(n,ni_min,k_min,k_max)

  # Select one of these entries at random
  # Randomly permute the entries in this partition.
  int_part = random.choice(list_of_int_partitions)
  random.shuffle(int_part)
  
  # DEBUG
  #print(int_part)

  # Infer the number of groups
  k = len(int_part)

  # Find a random even subset of vertices and odd subset of vertices.
  index_list = list(range(1,k+1))
  
  rand_odd_int = random.randrange(1, k, 2)
  I_odd = set(random.sample(index_list,rand_odd_int))

  # For Q0, choose to be c or sci at random.
  Q0_case = random.randint(0,k)
  if (Q0_case == 0):
    qasst_dict["Q0"] = "c"
  else:
    qasst_dict["Q0"] = "sc"+str(Q0_case)

  if ((Q0_case == 0) and (type == "CM")):
    # CM CASE 1
    # Choose a random even-size subset
    index_set = set(index_list)
    rand_even_int = random.randrange(0, k+1, 2)
    I_even = set(random.sample(list(index_set),rand_even_int))
    I_even_C = index_set.difference(I_even)
    
    # Quotients in this set are ss; outside are sc.
    for i in I_even:
      qasst_dict["Q"+str(i)] = "ss"
    for i in I_even_C:
      qasst_dict["Q"+str(i)] = "sc"

  elif ((Q0_case != 0) and (type == "CM")):
    # CM CASE 2(j) and 3(j)
    index_set = set(index_list)
    index_set.remove(Q0_case)
    I_len = rand_int = random.randint(0,k-1)
    I = set(random.sample(list(index_set),I_len))
    I_C = index_set.difference(I)
    
    if ((I_len%2)==0):
      # CM Case 2(j)
      # Qj is sc, Qi in I is ss, Qi in I_C is c
      qasst_dict["Q"+str(Q0_case)] = "sc"
      for i in I:
        qasst_dict["Q"+str(i)] = "ss"
      for i in I_C:
        qasst_dict["Q"+str(i)] = "c"
    elif ((I_len%2)==1):
      # CM Case 3(j)
      # Qj is c, Qi in I is ss, Qi in I_C is c
      qasst_dict["Q"+str(Q0_case)] = "c"
      for i in I:
        qasst_dict["Q"+str(i)] = "ss"
      for i in I_C:
        qasst_dict["Q"+str(i)] = "c"
    
  elif ((Q0_case == 0) and (type == "CS")):
    # CS CASE 1
    # Choose a random odd-size subset
    index_set = set(index_list)
    rand_odd_int = random.randrange(1, k+1, 2)
    I_odd = set(random.sample(list(index_set),rand_odd_int))
    I_odd_C = index_set.difference(I_odd)
    
    # Quotients in this set are ss; outside are sc.
    for i in I_odd:
      qasst_dict["Q"+str(i)] = "ss"
    for i in I_odd_C:
      qasst_dict["Q"+str(i)] = "sc"

  elif ((Q0_case != 0) and (type == "CS")):
    # CS CASE 2(j) and 3(j)
    index_set = set(index_list)
    index_set.remove(Q0_case)
    I_len = rand_int = random.randint(0,k-1)
    I = set(random.sample(list(index_set),I_len))
    I_C = index_set.difference(I)

    if ((I_len%2)==1):
      # CS Case 2(j)
      # Qj is sc, Qi in I is ss, Qi in I_C is c
      qasst_dict["Q"+str(Q0_case)] = "sc"
      for i in I:
        qasst_dict["Q"+str(i)] = "ss"
      for i in I_C:
        qasst_dict["Q"+str(i)] = "c"
    elif ((I_len%2)==0):
      # CS Case 3(j)
      # Qj is c, Qi in I is ss, Qi in I_C is c
      qasst_dict["Q"+str(Q0_case)] = "c"
      for i in I:
        qasst_dict["Q"+str(i)] = "ss"
      for i in I_C:
        qasst_dict["Q"+str(i)] = "c"

  # Return the list of group sizes and QASST structure dictionary.
  return int_part, qasst_dict


# Function to construct a random CM or CS LC-equivalent graph.
# Based on choosing random group-sizes and random QASST.
# Specify the number of vertices n and the LC type ("CM" or "CS").
# Return a Networkx graph object, the group sizes, and the quotient graph dictionary.

def build_random_CM_or_CS_lc_equivalent_graph(n,type,ni_min=2,k_min=3,k_max=7):

  # Call the function to choose random group sizes and quotient graphs.
  list_of_group_sizes, quotient_graph_dict = build_random_CM_or_CS_lc_equivalent_qasst_dict(n,type,ni_min,k_min,k_max)

  # Construct a dictionary of quotient graphs (qasst_dict) and the QASST.
  qasst_dict, qasst = construct_CM_or_CS_QASST(list_of_group_sizes,quotient_graph_dict)

  # Fuse the QASST into a graph.
  G = fuse_CM_or_CS_qasst(qasst_dict)

  # Return this graph, the group sizes, and the quotient graph sturcture dictionary.
  return G, list_of_group_sizes, quotient_graph_dict


# Function to compute a primitive local complement
# (That is, LC with respect to a single vertex v)
# Takes a Networkx graph and a specified vertex as input.
# Returns a Netowrkx graph as output (the LC of G wrt v).

def primitive_local_complement(G,v):

  # Error message in case v is not a vertex of G
  if ((v in G.nodes)==False):
    print("ERROR: v does not appear to be a vertex of G.")
    return 0

  # Make a copy of G to modify
  LCv_G = G.copy()

  # Infer the set of neighbors of v
  v_neighbors = set(LCv_G.neighbors(v))

  # DEBUG
  #print(v_neighbors)

  # Loop through pairs of neighbors and check connectivity.
  for v1 in v_neighbors:
    for v2 in v_neighbors:
      # Exclude the same index twice.
      if( v1 != v2 ):
        # Complement the edge
        # Check the connectivity in G, but update in LCv_G.
        # This way, we don't worry about double counting, but unfortunately
        # we do have the check the edge hasn't already been remvoed or get an error.
        if (((v1,v2) in G.edges) == True):
          if (((v1,v2) in LCv_G.edges) == True):
            LCv_G.remove_edge(v1,v2)
        else:
          LCv_G.add_edge(v1,v2)
  
  # Return the modified graph
  return LCv_G


# Function to compute the local Clifford transformation from a sequence of LCs.
# Takes a graph (state) and sequence of LC operations as input.
# Returns the final graph and a dictionary of local Clifford operations as output.

def compute_local_Clifford_transformation_and_state(G,LC_seq):

  # Infer the set of vertices for this graph (state).
  vertex_set = set(G.nodes)

  # Initialize a graph to be transformed
  # Initialize a list of dictionaries of local Clifford transformations
  G_transformed = G.copy()
  list_of_local_Clifford_dicts = []

  for u in LC_seq:
    u_neighbors = set(G_transformed.neighbors(u))
    local_Clifford_dict = {}

    # Compute the local clifford transformation
    for v in vertex_set:
      if (v==u):
        local_Clifford_dict[v] = "X(-pi/4)"
      elif (v in u_neighbors):
        local_Clifford_dict[v] = "Z(pi/4)"
      else:
        local_Clifford_dict[v] = "I"
    
    # Append to the list of dictionaries.
    list_of_local_Clifford_dicts.append(local_Clifford_dict)

    # Replace the intermediate graph with its next transformation
    G_transformed = primitive_local_complement(G_transformed,u)

  # Return the final transformed graph and the local Clifford list of dicts.
  return G_transformed, list_of_local_Clifford_dicts

