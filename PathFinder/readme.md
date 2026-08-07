# PathFinder - Dijkstra's Shortest Path Algorithm

An object-oriented Python implementation of Dijkstra's Algorithm for calculating shortest paths and minimum distances across weighted undirected graph models.

---

## 🌟 Key Features

* 🗺️ **Object-Oriented Graph Representation:** Built with custom `Graph` and `Edge` class abstractions.
* 📍 **Dijkstra's Shortest Path Algorithm:** Calculates minimum total distance and reconstructs step-by-step shortest paths between source and destination vertices (e.g., `"A"` to `"Z"`).
* 📁 **JSON Graph Loading:** Dynamically loads graph datasets (`graph_1.jsn` through `graph_5.jsn`, `my_graph.jsn`).
* 🖥️ **Interactive Menu CLI:** Allows selecting different graph datasets and displaying distance outputs in the terminal.
* ⚡ **Zero External Dependencies:** Built entirely using standard Python 3 modules (`json`, `sys`, `pathlib`).

---

## 📁 Project Structure

```text
PathFinder/
├── main.py            # CLI entry point for graph selection & path calculation
├── graph.py           # Graph, Edge classes, Dijkstra implementation & JSON parser
├── graph_1.jsn        # Benchmark Graph Dataset 1
├── graph_2.jsn        # Benchmark Graph Dataset 2
├── graph_3.jsn        # Benchmark Graph Dataset 3
├── graph_4.jsn        # Benchmark Graph Dataset 4
├── graph_5.jsn        # Benchmark Graph Dataset 5
├── my_graph.jsn       # Custom Graph Dataset
├── requirements.txt   # Dependency notice (Standard Library)
└── readme.md          # Project documentation
```

---

## 🛠️ Setup & Execution

1. **Prerequisites:**
   Python 3.8+ (No external third-party packages required).

2. **Run PathFinder:**
   ```bash
   python main.py
   ```

---

## 📋 Requirements (`requirements.txt`)

This project relies exclusively on standard Python modules (`json`, `sys`, `pathlib`). No `pip install` steps are necessary.

---

## 👨‍💻 Author

**Manan Arora**
