import numpy as np
import itertools
import matplotlib.pyplot as plt

import networkx as nx
from networkx.generators import *


def local_cmpl(G, v):
    # local complement of G about node v
    neighbors = list(G.neighbors(v)) # list of neighbors of v
    # all the pairs of neighbors
    for pair in itertools.combinations(neighbors, 2):
        a = pair[0]
        b = pair[1]
        if G.has_edge(a,b):
            G.remove_edge(a,b)
        else:
            G.add_edge(a,b)
    return G

def pivot(G, u, v):
    # G * u * v * u
    G = local_cmpl(G, u)
    G = local_cmpl(G, v)
    G = local_cmpl(G, u)
    return G

# simplification with triangle finding algorithm
def simplification(G):
    tri = nx.triangles(G)
    tri = sorted(tri.items(), key=lambda x:x[1])
    tri = list((x, y) for x, y in tri)
    # print(tri)
    # print("INPUT:" + str(G.number_of_edges()))
    for t in tri:
        # print(t)
        latest_num_e = G.number_of_edges()
        # if t[1] == 1 or t[1] == 2:
        #     G = local_cmpl(G, t[0])
        LC = local_cmpl(G, t[0])
        if LC.number_of_edges() > latest_num_e:
            G = local_cmpl(G, t[0])
            # took local complement
    # print("RESULT:" + str(G.number_of_edges()))
    return G

def count_triangles_for_p(n):
    # n: number of nodes
    Gs = [] # graphs
    ps = [] # probabilities
    p = 0
    num_e = []
    nums_tri = []
    for i in range(101):
        ps.append(p)
        G = nx.gnp_random_graph(n=n, p=p, seed=None, directed=False)
        Gs.append(G)
        
        tri = nx.triangles(G)
        num_tri = sum(tri.values()) / 3
        nums_tri.append(num_tri)
        num_e.append(G.number_of_edges())
        p += 0.01
    return Gs, num_e, nums_tri, ps

def clst_coeff(G):
    # Given a graph, return a dict of cluster coefficient of vertices
    tri = nx.triangles(G)
    cs = {}
    for v in G.nodes():
        # calculate c_v
        # c_v = # of triangles of v / (1/2 k_v (k_v - 1)) 
        k_v = G.degree(v)
        
        if k_v <= 1:
            c_v = 0
        else:
            c_v = tri[v] / (1/2 * k_v * (k_v - 1))
        cs[v] = c_v
    return cs


def greedy(G):
    while True: 
        ccs = clst_coeff(G)
        # sorting ccs
        ccs_sorted = sorted(ccs.items(), reverse=True, key=lambda x:x[1])
        ccs_sorted_positive = []
        
        # remove nodes with c = 0
        for cc in ccs_sorted:
            if cc[1] > 0:
                ccs_sorted_positive.append(cc)
            else:
                pass
        if len(ccs_sorted_positive) == 0:
            break
        
        update = False
        for cc in ccs_sorted_positive:
            G_num_e = G.number_of_edges()
            G_star_v = G.copy()
            G_star_v = local_cmpl(G_star_v, cc[0])
            G_star_v_num_e = G_star_v.number_of_edges()
            
            if G_num_e > G_star_v_num_e:
                G = G_star_v
                update = True
            else:
                pass
        if update == False:
            break
        # if there is no positive ccs which reduce the number of edge, break
    return G

def greedy_with_cond(G):
    while True:
        num_update = 0 # update counter
        cond_update = G.number_of_edges() / 3 # update condition
        
        cs = clst_coeff(G)
        # remove nodes with c = 0
        # sorting cs
        cs_sorted = sorted(cs.items(), reverse=True, key=lambda x:x[1])
        
        candidates = [] # candidates to take LC
        for c in cs_sorted:
            if c[1] > 0:
                candidates.append(c) 
            else:
                pass
        for v in candidates:
            G_num_e = G.number_of_edges()
            G_star_v = G.copy()
            G_star_v = local_cmpl(G_star_v, v[0])
            if G_num_e > G_star_v.number_of_edges():
                G = G_star_v
                num_update += 1
            else:
                pass
            if num_update >= cond_update:
                break
            
        if num_update == 0:
            break
        num_update = 0
    return G

def graph_for_n(p, nmax):
    Gs = []
    optimizedGs = []
    original_num_e = []
    optimized_num_e = []
    ns = []
    n = 1
    for i in range(nmax + 1):
        G = nx.gnp_random_graph(n=n, p=p, seed=None, directed=False)
        Gs.append(G)
        original_num_e.append(G.number_of_edges())
        optimizedG = simplification(G)
        optimizedGs.append(optimizedG)
        optimized_num_e.append(G.number_of_edges())
        ns.append(n)
        n += 1
    return Gs, optimizedGs, original_num_e, optimized_num_e, ns


def graph_for_n_greedy(p,nmax):
    Gs = []
    optimizedGs = []
    original_num_e = []
    optimized_num_e = []
    ns = []
    n = 1
    for i in range(nmax + 1):
        G = nx.gnp_random_graph(n=n, p=p, seed=None, directed=False)
        Gs.append(G)
        original_num_e.append(G.number_of_edges())
        # optimizedG = simplification(G)
        optimizedG = greedy(G)
        optimizedGs.append(optimizedG)
        optimized_num_e.append(optimizedG.number_of_edges())
        ns.append(n)
        n += 1
    return Gs, optimizedGs, original_num_e, optimized_num_e, ns

def graph_for_p(n):
    Gs = []
    optimizedGs = []
    original_num_e = []
    optimized_num_e = []
    ps = []
    nums_tri = []
    nums_tri_optimized = []
    p = 0
    for i in range(100):
        ps.append(p)
        G = nx.gnp_random_graph(n=n, p=p, seed=None, directed=False)
        Gs.append(G)
        tri = nx.triangles(G)
        num_tri = sum(tri.values()) / 3
        nums_tri.append(num_tri)
        
        original_num_e.append(G.number_of_edges())
        optimizedG = simplification(G)
        optimizedGs.append(optimizedG)
        optimized_num_e.append(G.number_of_edges())
        
        tri = nx.triangles(optimizedG)
        num_tri = sum(tri.values()) / 3
        nums_tri_optimized.append(num_tri)
        p += 0.01
    return Gs, optimizedGs, original_num_e, optimized_num_e, ps, nums_tri, nums_tri_optimized

def graph_for_p_greedy(n):
    Gs = []
    optimizedGs = []
    original_num_e = []
    optimized_num_e = []
    ps = []
    nums_tri = []
    nums_tri_optimized = []
    p = 0
    for i in range(100):
        ps.append(p)
        G = nx.gnp_random_graph(n=n, p=p, seed=None, directed=False)
        Gs.append(G)
        tri = nx.triangles(G)
        num_tri = sum(tri.values()) / 3
        nums_tri.append(num_tri)
        
        original_num_e.append(G.number_of_edges())
        optimizedG = greedy(G)
        optimizedGs.append(optimizedG)
        optimized_num_e.append(optimizedG.number_of_edges())
        
        tri = nx.triangles(optimizedG)
        num_tri = sum(tri.values()) / 3
        nums_tri_optimized.append(num_tri)
        p += 0.01
    return Gs, optimizedGs, original_num_e, optimized_num_e, ps, nums_tri, nums_tri_optimized