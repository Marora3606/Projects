# PathFinder — Dijkstra's Shortest Path

An object-oriented implementation of Dijkstra's algorithm over weighted
undirected graphs loaded from JSON. Computes both the minimum distance and the
reconstructed path between two vertices, with input validation for the
conditions the algorithm actually requires.

Standard library only — no third-party packages.

---

## 🌟 What it does

* 🗺️ **Graph model** — `Graph` and `Edge` classes built from JSON triples of the
  form `[from, to, weight]`.
* 📍 **Dijkstra with path reconstruction** — tracks a `previous` pointer per
  vertex so the route itself can be rebuilt, not just the total distance.
* ✅ **Precondition validation** — rejects negative or missing edge weights
  before running. Dijkstra is only correct on non-negative weights; a negative
  edge can make an already-finalised vertex reachable more cheaply, and the
  algorithm never revisits it.
* ⏹️ **Early termination** — stops as soon as the destination is finalised
  rather than exhausting the whole graph.
* 📁 **Six datasets** — `graph_1.jsn` … `graph_5.jsn` plus `my_graph.jsn`,
  selectable from an interactive menu.

---

## ⚙️ How it works

```
1. Set distance[start] = 0, every other vertex = infinity
2. While unvisited vertices remain:
     a. pick the unvisited vertex with the smallest known distance
     b. stop if that distance is infinity (remaining vertices unreachable)
     c. mark it visited; stop early if it is the destination
     d. for each neighbour, if distance[current] + weight < distance[neighbour],
        update the distance and record current as the neighbour's predecessor
3. Walk the predecessor chain backwards from the destination to rebuild the path
```

Step 2d is **edge relaxation** — the core operation of the algorithm.

### Complexity

This implementation scans the unvisited set linearly to find the minimum
(step 2a), giving **O(V²)** overall.

Replacing that scan with a binary heap (`heapq`) yields **O((V + E) log V)**,
which is much faster on large sparse graphs. On the small graphs here the
difference is not measurable, and the linear scan is easier to read — but the
heap version is the standard implementation and worth knowing.

---

## 📁 Structure

```text
PathFinder/
├── main.py            # CLI entry point
├── graph.py           # Graph and Edge classes, dijkstra(), JSON loader
├── graph_1.jsn        # Test graph 1
├── graph_2.jsn        # ...
├── graph_3.jsn
├── graph_4.jsn
├── graph_5.jsn
├── my_graph.jsn       # Custom graph
├── requirements.txt   # (standard library only)
└── readme.md
```

### Graph file format

```json
[["A", "B", 4], ["B", "C", 3], ["A", "C", 9]]
```

Each triple is `[vertex, vertex, weight]`. Edges are undirected — both
directions are added.

---

## 🔧 Setup

```bash
cd PathFinder
python main.py
```

Requires **Python 3.8+**. No dependencies to install.

Pick a graph from the menu; the program prints the shortest path from `A` to `Z`
and its total distance.

---

## ⚠️ Known limitations

- **O(V²) rather than O((V+E) log V)** — see the complexity note above.
- **Source and destination are hardcoded** to `"A"` and `"Z"`. Accepting them as
  arguments would make the tool general.
- **Undirected only.** Directed graphs would need the edge list built one way.
- **No tests.** `dijkstra()` is a pure function over a small input and would be
  straightforward to test — including the negative-weight rejection path.
- **No visualisation.** Paths are printed as text.

---

## 📝 Context

Originally submitted as university coursework (CST1450, Middlesex University
Dubai).

---

## 👨‍💻 Author

**Manan Arora**
