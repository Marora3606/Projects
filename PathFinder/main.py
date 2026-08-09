# =============================================================
# Module: main.py
# Project Area: PathFinder
# Purpose: Implements the runtime logic for this project component.
# Notes: Keep this file focused on one responsibility so future
# maintenance remains straightforward.
# =============================================================

from graph import load_graph_from_json, select_graph_filename


# TASK 5: RUNNING THE PROGRAM ON JSON GRAPHS
def main():
    while True:
        try:
            filename = select_graph_filename()
            if filename is None:
                print("Goodbye!")
                break

            graph = load_graph_from_json(filename)
            path, distance = graph.dijkstra("A", "Z")

            print(f"File: {filename}")
            print(f"Shortest path: {' -> '.join(path)}")
            print(f"Total distance: {distance}")

        except Exception as error:
            print(f"Error while processing the selected graph: {error}")

        print()


if __name__ == "__main__":
    main()