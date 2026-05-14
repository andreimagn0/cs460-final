"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Andrei Dominic Magno
Student ID: 129948062

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    - **Why a single shortest-path run from S is not enough:**
    A single shortest-path run from S would only consider the cheapest cost from the start to each chamber, but it does not consider the best order of which chambers to visit.

    - **What decision remains after all inter-location costs are known:**
    The decision that remains after all inter-location costs are known is to figure out the sequence of visting relic chambers that minimize total travel cost.

    - **Why this requires a search over orders (one sentence):**
    This requires a search over orders because the total travel cost depends on the visiting order of chambers, not just on shortest path between chambers.

    TODO
    """
    return "TODO"


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """
    sources = set()
    sources.add(spawn)
    for relic in relics:
        sources.add(relic)
    return list(sources)


def run_dijkstra(graph, source):
    import heapq
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0

    pq = []
    heapq.heappush(pq, (0, source))
    while pq:
        (current_distance, current_node)= heapq.heappop(pq)
        if current_distance > dist[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            if current_distance + weight < dist[neighbor]:
                dist[neighbor] = current_distance + weight
                heapq.heappush(pq, (dist[neighbor], neighbor))
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    sources = select_sources(spawn, relics, exit_node)

    dist_table = {}

    for source in sources:
        dist_table[source] = run_dijkstra(graph, source)

    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    Once a node has been finalized in S, dist[v] is guaranteed to be the shortest-path distance from x to v and will not change.

    For nodes not in S, dist[u] is the current best-so-far shortest path from x to u using finalized nodes, and may still be updated if a better path is discovered.

    Before iteration 1, S is empty, so the condition for finalized nodes holds. Since the source x has dist[x] = 0 as the shortest path is itself, and all other nodes have distance infinity since no other paths have been discovered, the invariant holds. 

    At each iteration, you pick the node with the smallest current distance. Any alternative path must either go through a node with an equal to or larger than distance, and adding nonnegative edge weights cannot result in a lower total cost. Therefore, no shortest path exists, and finalizing the min-dist node can be done safely.

    At termination, S contains all reachable nodes from x, and for each node v in S, dist[v] represents the guaranteed shortest-path distance from x to v. Nodes that are not in S are unreachable from x and have distance infinity.  

    Correct shortest-path distances guarantee optimal routing decisions, ensuring the planner chooses the minimium-cost path every time.


    TODO
    """
    return "TODO"


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    ### Why Greedy Fails

    > State the failure mode. Then give a concrete counter-example using specific node names
    > or costs (you may use the illustration example from the spec). Three to five bullets.

    - **The failure mode:** Greedy only considers cheapest local cost, not best order of chambers to visit.
    - **Counter-example setup:**

    **Entrance:** S | **Relic chambers:** B, C, D | **Exit:** T

    | From \ To | B   | C   | D   | T   |
    |-----------|-----|-----|-----|-----|
    | S         | 1   | 2   | 2   | --  |
    | B         | --  | 4   | 5   | 1   |
    | C         | 2   | --  | 1   | 1   |
    | D         | 1   | 2   | --  | 1   |

    - **What greedy picks:** S -> B -> C -> D -> T; total fuel = 1 + 4 + 1 + 1 = **7**
    - **What optimal picks:** S -> C -> D -> B -> T; total fuel = 2 + 1 + 1 + 1 = **5**
    - **Why greedy loses:** Greedy loses because it only considers cheapest next chamber at each step, but the local choice can lead to a suboptimal global path.

    ### What the Algorithm Must Explore
    > One bullet. Must use the word "order."

    The algorithm must explore different orders of chambers to visit to find minimum total cost.

    TODO
    """
    return "TODO"


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    best = [float("inf"), []]

    relics_remaining = set(relics)
    relics_visited_order = []

    _explore(dist_table, spawn, relics_remaining, relics_visited_order, 0, exit_node, best)

    return (best[0], best[1])

    
    pass


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    if not relics_remaining:
        if dist_table[current_loc][exit_node] == float("inf"):
            return
        final_cost = cost_so_far + dist_table[current_loc][exit_node]

        if final_cost < best[0]:
            best[0] = final_cost
            best[1] = list(relics_visited_order)
        return

    if cost_so_far >= best[0]: # This pruning condition is safe because it future steps from cost_so_far 
        return                 # can only increase costs since edge weights are nonnegative. This is also
                               # why >= is valid instead of >, since the route cost can only increase from that point.
        
    
    
    for relic in list(relics_remaining):
        if dist_table[current_loc][relic] == float("inf"):
            continue
        step_cost = cost_so_far + dist_table[current_loc][relic]

        relics_remaining.remove(relic)
        relics_visited_order.append(relic)

        _explore(dist_table, relic, relics_remaining, relics_visited_order, step_cost, exit_node, best)

        relics_visited_order.pop()
        relics_remaining.add(relic)



# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    we are trying to calculate total cost for each algorithm
    compare each total cost with remaining total cost
    we calculate total cost by using a recursive function to check each layer of the graph and their distances
    return the minimum cost and ordered relic list
    we store these when we unwrap the recursive stack 
    base case: when the current node is the exit node, return 0
    """

    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
