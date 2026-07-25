from graph import load_graph_from_json


# TASK 5: RUNNING THE PROGRAM ON JSON GRAPHS
def main():
    # Ask user for filename (simple and safe, no sys.argv)
    filename = input("Enter JSON filename: ")

    try:
        graph = load_graph_from_json(filename)
        path, distance = graph.dijkstra("A", "Z")

        # SAME OUTPUT FORMAT AS BEFORE
        print(f"File: {filename}")
        print(f"Shortest path: {' -> '.join(path)}")
        print(f"Total distance: {distance}")

    except Exception as error:
        print(f"Error while processing {filename}: {error}")


if __name__ == "__main__":
    main()