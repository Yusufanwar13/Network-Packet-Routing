import heapq
import tkinter as tk
from tkinter import messagebox

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
        messagebox.showerror("Error", "Invalid start or end node")
        return
    
    path, cost = shortest_path(network, start, end)
    result_var.set(f"Shortest Path: {' -> '.join(path)}\nCost: {cost}")

# Example network graph (Adjacency list representation)
network = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# GUI Setup
root = tk.Tk()
root.title("Network Packet Routing")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Start Node:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
start_var = tk.StringVar()
tk.Entry(root, textvariable=start_var, font=("Arial", 12)).pack(pady=5)

tk.Label(root, text="End Node:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
end_var = tk.StringVar()
tk.Entry(root, textvariable=end_var, font=("Arial", 12)).pack(pady=5)

tk.Button(root, text="Find Route", font=("Arial", 12), bg="#4CAF50", fg="white", command=find_route).pack(pady=10)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, font=("Arial", 12), bg="#f0f0f0", fg="blue").pack(pady=10)

root.mainloop()









