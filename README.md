This notebook is intended as supplemental material for the paper **"Efficient Preparation of Graph States using the Quotient Augmented Strong Split Tree"**.
It contains a Python implementation for many of the equations and simuluations described therein.
These include counting the size of the LC orbit, identifying minimal edge or minimal maximum-vertex-degree graph representatives, computing sequences of local Clifford transformations, generating distance-hereditary graphs, computing the QASST, and reproducing our numerical results.
See the Python notebook file **"CM_and_CS_Graph_LC_Orbits_Tutorial.ipynb"** for a more detailed description and examples.

Please site this research as:\
**(A)**\
@misc{connolly2026efficient,\
      &emsp;&emsp;title={Efficient Preparation of Graph States using the Quotient-Augmented Strong Split Tree},\
      &emsp;&emsp;author={Nicholas Connolly and Shin Nishio and Dan E. Browne and William John Munro and Kae Nemoto},\
      &emsp;&emsp;year={2026},\
      &emsp;&emsp;eprint={2603.23892},\
      &emsp;&emsp;archivePrefix={arXiv},\
      &emsp;&emsp;primaryClass={quant-ph},\
      &emsp;&emsp;url={https://arxiv.org/abs/2603.23892 }\
}\
**(B)**\
@misc{connolly2026local,\
      &emsp;&emsp;title={Local Equivalence Classes of Distance-Hereditary Graphs using Split Decompositions}, \
      &emsp;&emsp;author={Nicholas Connolly and Shin Nishio and Kae Nemoto},\
      &emsp;&emsp;year={2026},\
      &emsp;&emsp;eprint={2602.23825},\
      &emsp;&emsp;archivePrefix={arXiv},\
      &emsp;&emsp;primaryClass={math.CO},\
      &emsp;&emsp;url={https://arxiv.org/abs/2602.23825 }\
}

Summary of functions in the **"CM_and_CS_Graph_LC_Orbits_Tutorial.ipynb"** Python notebook.

* **build_random_CM_or_CS_lc_equivalent_graph(inputs)**\
Build a random graph locally equivalent to a complete multipartite graph or a clique-star as a NetworkX graph object. The user specifies information including the total number of vertices, minimum and maximum numbers of “groups” of vertices, and bounds on the number of quotient graphs. Also outputs a list of group sizes $[n_1,\cdots,n_k]$ and a Python dictionary describing the QASST decomposition.
* **determine_LC_orbit_size_for_CM_or_CS(inputs)**\
Computes the size of $|O(K_{n_1,\cdots,n_k})|$ using Equation 18 of (A) or of $|O(CS^r_{n_1,\cdots,n_k})|$ using Equation 19 of (A).
* **minimal_edge_count_and_structure_complete_multipartite_orbit(inputs)**\
Computes the number of edges in a minimal edge representative of ${\mathcal O}(K_{n_1,\cdots,n_k})$ via Equation 20 of (A), and provides the QASST decomposition of this graph.
* **minimal_edge_count_and_structure_clique_star_orbit(inputs)**\
Computes the number of edges in a minimal edge representative of ${\mathcal O}(CS^r_{n_1,\cdots,n_k})$ via Equation 21 of (A), and provides the QASST decomposition of this graph.
* **determine_minimal_Delta_G_complete_multipartite(inputs)**\
Computes the minimum maximum vertex degree $\Delta(G)$ across all graphs in ${\mathcal O}(K_{n_1,\cdots,n_k})$ by Equation 22 of (A) and gives the QASST decomposition of this graph.
* **determine_minimal_Delta_G_clique_star(inputs)**\
Computes the minimum maximum vertex degree $\Delta(G)$ across all graphs in ${\mathcal O}(CS^r_{n_1,\cdots,n_k})$ by Equation 23 of (A) and gives the QASST decomposition of this graph.
* **compute_split_fuse_parameters_for_complete_multipartite(inputs)**\
Computes the resource requirements for the split-fuse method (number of CZ gates, number of time steps, and number of qubits) based on Equations 5, 6, and 7 of (A) for a graph QASST-equivalent to $K_{n_1,\cdots,n_k}$ (this is the same for the clique-star).
* **find_LC_transformation_for_graph(inputs)**\
Identifies an explicit sequence of local complements that transform either $K_{n_1,\cdots,n_k}$ or $CS^1_{n_1,\cdots,n_k}$ into a target graph. The user must provide a Python dictionary describing the QASST decomposition of the target graph. These formulas are based on results derived in the appendix of (B).
* **primitive_local_complement(G,v)**\
Given a NetworkX graph object $G$ and a choice of vertex $v$, compute a new graph object $c_v(G)$ by applying a primitive local complement on $G$ with respect to $v$.
* **compute_local_Clifford_transformation_and_state(G,LC_seq)**\
Given a NetworkX graph object $G$ and a list of vertex indices, compute a new graph object by applying a sequence of local complements matching these vertices. Also construct a list of Python dictionaries representing the explicit local Clifford transformations corresponding to these. There is one dictionary for each LC operation, with keys matching vertex indices and values matching the local unitary applied to the corresponding qubit.
* **create_random_DH_graph_and_QASST(inputs)**\
Creates a random distance-hereditary graph $G$ as a NetworkX graph object, along with $\textit{QASST}(G)$ as a graph whose vertices are quotient graphs. The user neeeds only specify the number of vertices.
* **generate_and_plot_CM_or_CS_optimization_data(inputs)**\
Runs a numerical simulation comparing the various preparation protocols (naive, heuristic, optimal, or split-fuse) for randomly generated graphs belonging to the LC orbit of a complete multiparite graph or a clique-star, as specified by the user.
The user specifies the minimum and maximum number of qubits, the number of steps in between, and the total number of samples of randomly generated graphs of each type.
Results in a comparison of boxplots like Figure 8 of (A).
* **generate_and_plot_random_DH_optimization_data(inputs)**\
Runs a numerical simulation comparing the various preparation protocols (naive, heuristic, or split-fuse) for randomly generated distance-hereditary graphs.
As in the preceding function, the user specifies the minimum and maximum number of qubits, the number of steps in between, and the total number of samples of randomly generated graphs of each type, and the result is graph comparing boxplots like Figure 8 of (A).
* **generate_and_plot_generic_random_graph_optimization_data(inputs)**\
Runs a numerical simulation comparing the various preparation protocols (naive, heuristic, generalized split-fuse, or heur. + gen. split-fuse) for randomly generated Erdős–Rényi graphs with a specified edge density. As in the preceding two functions, the user specifies the minimum and maximum number of qubits, the number of steps in between, and the total number of samples of randomly generated graphs of each type, and also an edge density. The result is graph comparing boxplots like Figure 9 of (A).
