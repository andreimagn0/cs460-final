# The Torchbearer

**Student Name:** Andrei Dominic Magno
**Student ID:** 129948062
**Course:** CS 460 – Algorithms | Spring 2026
---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single shortest-path run from S would only consider the cheapest cost from the start to each chamber, but it does not consider the best order of which chambers to visit.

- **What decision remains after all inter-location costs are known:**
The decision that remains after all inter-location costs are known is to figure out the sequence of visting relic chambers that minimize total travel cost.

- **Why this requires a search over orders (one sentence):**
This requires a search over orders because the total travel cost depends on the visiting order of chambers, not just on shortest path between chambers.
---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Spawn (S) | Needed to compute the shortest cost from S to each possible relic |
| Relics | Needed to compute the shortest cost from each relic to the next possible relic or the exit node |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | 2-D Dictionary |
| What the keys represent | Outer Key = source node, Inner Key = destination node |
| What the values represent | Cheapest travel cost from source to destination |
| Lookup time complexity | Dictionary lookup time |
| Why O(1) lookup is possible | Dictionaries in Python use hashing |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** 1 spawn + k relics = O(k)
- **Cost per run:** Single shortest-path run costs O(m log n)
- **Total complexity:** Number of Dijkstra runs + Cost per run = O(k) * O(m log n) = O(k * m log n)
- **Justification (one line):** We run Dijkstra for each source node, and each run costs O(m log n).

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
Once a node has been finalized in S, dist[v] is guaranteed to be the shortest-path distance from x to v and will not change.

- **For nodes not yet finalized (not in S):**
For nodes not in S, dist[u] is the current best-so-far shortest path from x to u using finalized nodes, and may still be updated if a better path is discovered.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
Before iteration 1, S is empty, so the condition for finalized nodes holds. Since the source x has dist[x] = 0 as the shortest path is itself, and all other nodes have distance infinity since no other paths have been discovered, the invariant holds. 

- **Maintenance : why finalizing the min-dist node is always correct:**
At each iteration, you pick the node with the smallest current distance. Any alternative path must either go through a node with an equal to or larger than distance, and adding nonnegative edge weights cannot result in a lower total cost. Therefore, no shortest path exists, and finalizing the min-dist node can be done safely.

- **Termination : what the invariant guarantees when the algorithm ends:**
At termination, S contains all reachable nodes from x, and for each node v in S, dist[v] represents the guaranteed shortest-path distance from x to v. Nodes that are not in S are unreachable from x and have distance infinity.  

### Part 3c: Why This Matters for the Route Planner

Correct shortest-path distances guarantee optimal routing decisions, ensuring the planner chooses the minimium-cost path every time.

---

## Part 4: Search Design

### Why Greedy Fails

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

The algorithm must explore different orders of chambers to visit to find minimum total cost.

---

## Part 5: State and Search Space

### Part 5a: State Representation


| Component                | Variable name in code | Data type | Description                                     |
|---                       |---                    |---        |---                                              |
| Current location         | current_loc           | Node      | Stores the current node                         |
| Relics already collected | relics_remaining      | Set[Node] | Stores set of relics that have not been visited |
| Fuel cost so far         | cost_so_far           | Float     | Stores the fuel cost so far at the current node |

### Part 5b: Data Structure for Visited Relics

| Property                                    | Your answer       |
|---                                          |---                |
| Data structure chosen                       | set[Node]        |
| Operation: check if relic already collected | Time complexity: O(1)  |
| Operation: mark a relic as collected        | Time complexity: O(1) |
| Operation: unmark a relic (backtrack)       | Time complexity: O(1) |
| Why this structure fits                     | Sets are mutable and have fast add/remove |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!  relic orders considered
- **Why:** Search may need to explore all possible paths to find the mininum cost.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** the current minimum cost so far for the route
- **When it is used:** if cost_so_far is greater than or equal to the current best cost
- **What it allows the algorithm to skip:** Skips unnecessary recursive calls since the current travel cost is higher than the current cost

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** current location, current total cost, relics remaining
- **What the lower bound accounts for:** the minimum additional cost required for the current route
- **Why it never overestimates:** The current route cannot beat the best route and it cannot avoid adding additional cost
The current route will either be on par or more than the best

### Part 6c: Pruning Correctness

Future steps from cost_so_far can only increase costs since edge weights are nonnegative
Pruning checks the lower bound, since the route cost can only increase from that point
        

---

## References

- https://www.geeksforgeeks.org/dsa/introduction-to-branch-and-bound-data-structures-and-algorithms-tutorial/
- https://www.youtube.com/watch?v=m1Fjdnj_Mds 
- Lecture Notes
