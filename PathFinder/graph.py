# =============================================================
# Module: graph.py
# Project Area: PathFinder
# Purpose: Implements the runtime logic for this project component.
# Notes: Keep this file focused on one responsibility so future
# maintenance remains straightforward.
# =============================================================

import json
import sys
from pathlib import Path


class Edge:
    """
    Represents one undirected edge between two vertices.
    """
    def __init__(self, v1, v2, weight=None):
        self.v1 = str(v1)
        self.v2 = str(v2)
        self.weight = None if weight is None else float(weight)

    def connects(self, a, b):
        # Check if this edge connects vertices a and b in either direction (undirected)
        return (self.v1 == a and self.v2 == b) or (self.v1 == b and self.v2 == a)


# TASK 1: GRAPH CLASS
class Graph:
    """
    Graph represented by a list of Edge objects.
    """
    def __init__(self):
        self.edges = []

    def add_edge(self, v1, v2, weight=None):
        v1 = str(v1)
        v2 = str(v2)

        # A graph edge must connect two different vertices.
        if v1 == v2:
            raise ValueError("An edge cannot connect a vertex to itself.")

        # Prevent duplicate undirected edges such as A-B and B-A.
        for edge in self.edges:
            if edge.connects(v1, v2):
                raise ValueError(f"Duplicate edge between {v1} and {v2} is not allowed.")

        self.edges.append(Edge(v1, v2, weight))

    def list_vertices(self):
        # Collect all unique vertices from all edges and return sorted
        vertices = set()
        for edge in self.edges:
            vertices.add(edge.v1)
            vertices.add(edge.v2)
        return sorted(vertices)

    def are_adjacent(self, v1, v2):
        # Check if there is a direct edge between two vertices
        for edge in self.edges:
            if edge.connects(v1, v2):
                return True
        return False

    def neighbours(self, vertex):
        # Find all vertices adjacent to the given vertex
        result = []
        for edge in self.edges:
            if edge.v1 == vertex:
                result.append(edge.v2)
            elif edge.v2 == vertex:
                result.append(edge.v1)
        return sorted(result)

    def weighted_neighbours(self, vertex):
        # Find all adjacent vertices and their distances (weights) from the given vertex
        result = []
        for edge in self.edges:
            if edge.v1 == vertex:
                result.append((edge.v2, edge.weight))
            elif edge.v2 == vertex:
                result.append((edge.v1, edge.weight))
        return result

    # TASK 4: DIJKSTRA'S ALGORITHM
    def dijkstra(self, start, end):
        """
        Finds the shortest path between start and end vertices.
        Returns (path, distance).
        """
        # Normalize the caller-supplied vertex names so the graph can compare
        # them safely across all input shapes.
        start = str(start)
        end = str(end)

        vertices = self.list_vertices()

        if start not in vertices or end not in vertices:
            raise ValueError("Start or end vertex is not in the graph.")

        # Dijkstra's algorithm only works if all edges have valid non-negative distances.
        for edge in self.edges:
            if edge.weight is None:
                raise ValueError("Dijkstra's algorithm requires every edge to have a distance.")
            if edge.weight < 0:
                raise ValueError("Dijkstra's algorithm requires non-negative distances.")

        # Initialize: distances from start to all vertices
        distances = {}
        previous = {}  # Track the previous vertex in the shortest path
        for vertex in vertices:
            distances[vertex] = float("inf")
            previous[vertex] = None

        unvisited = set(vertices)
        distances[start] = 0.0  # Distance to start vertex is zero

        while unvisited:
            # Choose the unvisited vertex with the smallest known distance.
            current_vertex = None
            smallest_distance = float("inf")

            for vertex in unvisited:
                if distances[vertex] < smallest_distance:
                    smallest_distance = distances[vertex]
                    current_vertex = vertex

            # Stop if no unvisited vertex has a finite distance
            if current_vertex is None or distances[current_vertex] == float("inf"):
                break

            unvisited.remove(current_vertex)

            # Early termination if we reached the destination
            if current_vertex == end:
                break

            # Relax edges: update distances to neighbouring vertices if a shorter route is found.
            for neighbour, weight in self.weighted_neighbours(current_vertex):
                if neighbour in unvisited:
                    # Try the route through the current vertex and record it only
                    # when it is better than the already-known path.
                    new_distance = distances[current_vertex] + weight
                    if new_distance < distances[neighbour]:
                        distances[neighbour] = new_distance
                        previous[neighbour] = current_vertex  # Remember the path

        if distances[end] == float("inf"):
            raise ValueError(f"No path exists between {start} and {end}.")

        # Reconstruct the shortest path by backtracking through the previous vertices
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()  # Reverse to get path from start to end

        return path, distances[end]


# TASK 2: BUILD GRAPH FROM TRIPLES
def build_graph_from_triples(triples):
    """
    Takes a list of triples (A, B, W) and returns a Graph.
    """
    graph = Graph()
    for triple in triples:
        if len(triple) != 3:
            raise ValueError("Each triple must contain exactly three items: (A, B, W).")
        a, b, w = triple
        if not graph.are_adjacent(a, b):# Checking if the vertices are adjacent or not, if not, adding an edge with the given weight 
            graph.add_edge(a, b, w)
    return graph


# TASK 3: LOAD GRAPH FROM JSON
def load_graph_from_json(filename):
    """
    Reads triples from a JSON file and returns the Graph.
    """
    path = Path(filename)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    with path.open("r", encoding="utf-8") as file:
        triples = json.load(file)
    return build_graph_from_triples(triples)


def select_graph_filename():
    """Prompt the user to choose one of the available graph JSON files."""
    graph_dir = Path(__file__).resolve().parent
    available_graphs = []

    for path in graph_dir.glob("*.jsn"):
        if path.name.startswith("graph_") or path.name == "my_graph.jsn":
            available_graphs.append(path.name)

    available_graphs = sorted(
        available_graphs,
        key=lambda name: (
            0 if name == "my_graph.jsn" else 1,
            int(name.replace("graph_", "").replace(".jsn", "")) if name.startswith("graph_") else 999,
        ),
    )

    if not available_graphs:
        raise FileNotFoundError("No graph JSON files were found in the PathFinder folder.")

    print("Available graphs:")
    for index, name in enumerate(available_graphs, start=1):
        print(f"{index}. {name}")
    print("0. Exit")

    while True:
        choice = input("Which graph do you want to run? Enter a number, filename, or 'exit': ").strip()

        if not choice or choice.lower() in {"q", "quit", "exit"}:
            return None

        if choice.isdigit():
            index = int(choice)
            if index == 0:
                return None
            if 1 <= index <= len(available_graphs):
                return available_graphs[index - 1]
            print(f"Please enter a number between 1 and {len(available_graphs)}.")
            continue

        filename = choice if choice.endswith(".jsn") else f"{choice}.jsn"
        if (graph_dir / filename).exists():
            return filename

        print(f"Graph file '{filename}' was not found.")


def main():
    """Run a sample shortest-path calculation when executed directly."""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        graph = load_graph_from_json(filename)
        path, distance = graph.dijkstra("A", "Z")
        print(f"File: {filename}")
        print(f"Shortest path: {' -> '.join(path)}")
        print(f"Total distance: {distance}")
        return

    while True:
        filename = select_graph_filename()
        if filename is None:
            print("Goodbye!")
            break

        try:
            graph = load_graph_from_json(filename)
            path, distance = graph.dijkstra("A", "Z")
            print(f"File: {filename}")
            print(f"Shortest path: {' -> '.join(path)}")
            print(f"Total distance: {distance}")
        except Exception as error:
            print(f"Error while processing {filename}: {error}")

        print()


if __name__ == "__main__":
    main()