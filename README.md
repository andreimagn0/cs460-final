# The Torchbearer

**Student Name:** Andrei Dominic Magno
**Student ID:** 129948062
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single shortest-path run from S would only consider the cheapest cost from the start to each chamber, but it does not consider the best order of which chambers to visit.

- **What decision remains after all inter-location costs are known:**
The decision that remains after all inter-location costs are known is to figure out the sequence of visting relic chambers that minimize total travel cost.

- **Why this requires a search over orders (one sentence):**
This requires a search over orders because the total travel cost depends on the visiting order of chambers, not just on shortest path between chambers.
---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Spawn (S) | Needed to compute the shortest cost from S to each possible relic |
| Relics | Needed to compute the shortest cost from each relic to the next possible relic or the exit node |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | 2-D Dictionary |
| What the keys represent | Outer Key = source node, Inner Key = destination node |
| What the values represent | Cheapest travel cost from source to destination |
| Lookup time complexity | Dictionary lookup time |
| Why O(1) lookup is possible | Dictionaries in Python use hashing |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** 1 spawn + k relics = O(k)
- **Cost per run:** Single shortest-path run costs O(m log n)
- **Total complexity:** Number of Dijkstra runs + Cost per run = O(k) * O(m log n) = O(k * m log n)
- **Justification (one line):** We run Dijkstra for each source node, and each run costs O(m log n).

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
Once a node has been finalized in S, dist[v] is guaranteed to be the shortest-path distance from x to v and will not change.

- **For nodes not yet finalized (not in S):**
For nodes not in S, dist[u] is the current best-so-far shortest path from x to u using finalized nodes, and may still be updated if a better path is discovered.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
Before iteration 1, S is empty, so the condition for finalized nodes holds. Since the source x has dist[x] = 0 as the shortest path is itself, and all other nodes have distance infinity since no other paths have been discovered, the invariant holds. 

- **Maintenance : why finalizing the min-dist node is always correct:**
At each iteration, you pick the node with the smallest current distance. Any alternative path must either go through a node with an equal to or larger than distance, and adding nonnegative edge weights cannot result in a lower total cost. Therefore, no shortest path exists, and finalizing the min-dist node can be done safely.

- **Termination : what the invariant guarantees when the algorithm ends:**
At termination, S contains all reachable nodes from x, and for each node v in S, dist[v] represents the guaranteed shortest-path distance from x to v. Nodes that are not in S are unreachable from x and have distance infinity.  

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.
Correct shortest-path distances guarantee optimal routing decisions, ensuring the planner chooses the minimium-cost path every time.

---

## Part 4: Search Design

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

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
