import heapq
import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
import os

# Load saved theme
if os.path.exists("theme.txt"):
    with open("theme.txt", "r") as f:
        current_theme = f.read().strip()
else:
    current_theme = "light"

# Theme colors
theme_colors = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "entry_bg": "white",
        "button_bg": "#4CAF50",
        "result_fg": "blue"
    },
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "entry_bg": "#4a4a4a",
        "button_bg": "#00b894",
        "result_fg": "#00cec9"
    }
}

def apply_theme():
    colors = theme_colors[current_theme]
    root.configure(bg=colors["bg"])
    main_frame.configure(bg=colors["bg"])
    for widget in main_frame.winfo_children():
        if isinstance(widget, (tk.Label, ttk.Combobox)):
            try:
                widget.configure(background=colors["bg"], foreground=colors["fg"])
            except:
                pass
        elif isinstance(widget, tk.Button):
            widget.configure(bg=colors["button_bg"], fg='white')
        elif isinstance(widget, tk.Label) and widget.cget("textvariable") == str(result_var):
            widget.configure(fg=colors["result_fg"], bg=colors["bg"])

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    with open("theme.txt", "w") as f:
        f.write(current_theme)
    apply_theme()

def dijkstra(graph, start):
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    return distances, previous_nodes

def shortest_path(graph, start, end):
    distances, previous_nodes = dijkstra(graph, start)
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    return path, distances[end]

def find_route():
    start = start_var.get().strip().upper()
    end = end_var.get().strip().upper()

    if start not in network or end not in network:
        messagebox.showwarning("Input Required", "Please select both valid start and end nodes.")
        return

    path, cost = shortest_path(network, start, end)
    result_var.set(f"Shortest Path: {' -> '.join(path)}\nCost: {cost}")
    draw_graph(network, path)

def draw_graph(graph, path=None):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.kamada_kawai_layout(G)
    plt.figure(figsize=(10, 6))
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title("Network Graph with Shortest Path")
    plt.savefig("shortest_path.png")
    plt.show()

def reset_fields():
    start_var.set('')
    end_var.set('')
    start_combo.set('Enter Start Node')
    end_combo.set('Enter End Node')
    result_var.set('')

# Network Graph
network = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'D': 4, 'E': 1},
    'C': {'A': 5, 'F': 3},
    'D': {'B': 4, 'G': 6},
    'E': {'B': 1, 'H': 7, 'F': 2},
    'F': {'C': 3, 'E': 2, 'I': 4},
    'G': {'D': 6, 'J': 3},
    'H': {'E': 7, 'K': 5},
    'I': {'F': 4, 'L': 2},
    'J': {'G': 3, 'M': 4},
    'K': {'H': 5, 'N': 6},
    'L': {'I': 2, 'O': 3},
    'M': {'J': 4, 'P': 2},
    'N': {'K': 6, 'Q': 3},
    'O': {'L': 3, 'R': 5},
    'P': {'M': 2, 'S': 4},
    'Q': {'N': 3, 'T': 6},
    'R': {'O': 5},
    'S': {'P': 4},
    'T': {'Q': 6}
}

# GUI
root = tk.Tk()
root.title("Network Packet Routing")
root.geometry("420x470")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

font_style = ("Segoe UI", 12)

# Start Node
tk.Label(main_frame, text="Start Node:", font=font_style).pack(pady=5)
start_var = tk.StringVar()
start_combo = ttk.Combobox(main_frame, textvariable=start_var, values=list(network.keys()), font=font_style, state="readonly")
start_combo.set("Enter Start Node")
start_combo.pack(pady=5)

# End Node
tk.Label(main_frame, text="End Node:", font=font_style).pack(pady=5)
end_var = tk.StringVar()
end_combo = ttk.Combobox(main_frame, textvariable=end_var, values=list(network.keys()), font=font_style, state="readonly")
end_combo.set("Enter End Node")
end_combo.pack(pady=5)

# Buttons
tk.Button(main_frame, text="Find Route", font=font_style, command=find_route).pack(pady=10)
tk.Button(main_frame, text="Toggle Theme", font=font_style, command=toggle_theme).pack(pady=5)
tk.Button(main_frame, text="Reset", font=font_style, command=reset_fields).pack(pady=5)

# Result
result_var = tk.StringVar()
tk.Label(main_frame, textvariable=result_var, font=font_style, wraplength=360, justify="center").pack(pady=15)

apply_theme()
root.mainloop()
