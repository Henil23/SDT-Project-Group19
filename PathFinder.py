from collections import deque  # Importing deque for efficient queue implementation
from functools import lru_cache  # Importing lru_cache for memoization

# Define the PathFinding class
class PathFinding:
    def __init__(self, game):
        self.game = game  # Reference to the game object
        self.map = game.map.mini_map  # Reference to the mini-map of the game
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]  # Possible movement directions
        self.graph = {}  # Initialize graph for pathfinding
        self.GetGraph()  # Generate the graph based on the mini-map

    @lru_cache  # Memoization for caching pathfinding results
    def GetPath(self, start, goal):
        self.visited = self.BreadthFirst(start, goal, self.graph)  # Perform breadth-first search
        path = [goal]  # Initialize path with the goal node
        step = self.visited.get(goal, start)  # Start from the goal node and backtrack to find the path

        # Backtrack to construct the path
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]  # Return the last node in the path (usually the starting point)

    # Breadth-first search algorithm to find the shortest path
    def BreadthFirst(self, start, goal, graph):
        queue = deque([start])  # Initialize queue with the starting node
        visited = {start: None}  # Dictionary to keep track of visited nodes and their predecessors

        while queue:
            cur_node = queue.popleft()  # Dequeue the current node from the queue
            if cur_node == goal:  # If the current node is the goal, break the loop
                break
            next_nodes = graph[cur_node]  # Get the neighbors of the current node from the graph

            # Iterate over the neighbors of the current node
            for next_node in next_nodes:
                # Check if the neighbor is not visited and not occupied by an NPC
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)  # Enqueue the neighbor node
                    visited[next_node] = cur_node  # Mark the neighbor node as visited and set its predecessor
        return visited  # Return the visited dictionary containing the shortest path

    # Method to generate the graph based on the mini-map
    def GetGraph(self):
        for y, row in enumerate(self.map):  # Iterate over each row in the mini-map
            for x, col in enumerate(row):  # Iterate over each column in the row
                if not col:  # If the cell is not occupied (0 represents empty space)
                    # Add the current cell to the graph and get its neighbors
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    # Method to get the neighboring nodes of a given cell
    def get_next_nodes(self, x, y):
        # Generate a list of neighboring nodes based on possible movement directions
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]
