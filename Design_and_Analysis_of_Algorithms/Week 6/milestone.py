"""
Graph search algorithms for shortest path
"""

import heapq

def main(): 

    def bellman_ford(graph, start, target):
        pass

    def a_star(graph, start, target):
        """
        manhattan distance: the function returns a float, an estimate of the distance between the node and the goal
        """
        def heuristic(graph, node, goal):
            goal_node = graph[goal]
            n = graph[node]
            goal_x, goal_y = goal_node['pos']
            node_x, node_y = n['pos']

            dx = abs(node_x - goal_x)
            dy = abs(node_y - goal_y)
            # for the best paths, and an admissible heuristic, D is set to the lowest cost between nodes
            D = 0.17
            return D * (dx + dy)

        INF = ((1<<63) - 1) // 2
        parents = { x:x for x in graph }
        """
        The f-score of a vertex, capturing the estimated cost to be sustained to reach the goal from start in a path 
        passing through a certain vertex. Initializes these values to infinity for all vertices but vertex start.
        """
        f_score = { x:INF for x in graph } 
        distances = { x:INF for x in graph } 
        distances[start] = 0 
        f_score[start] = heuristic(graph, start, target)
        PQ = []
        heapq.heappush(PQ, [distances[start], start])

        while(PQ): 
            u = heapq.heappop(PQ) 
            u_id = u[1]

            if target != u_id:
                node = graph[u_id]
                for v in node['nb']:
                    v_id = v[0]
                    v_dist = v[1]
                    if distances[u_id] + v_dist < distances[v_id]:
                        distances[v_id] = distances[u_id] + v_dist
                        parents[v_id] = u_id
                        f_score[v_id] = distances[v_id] + heuristic(graph, v_id, target) 
                        heapq.heappush(PQ, [f_score[v_id], v_id])            

        if distances[target] == INF:
            print("No path.")
        else:
            steps = []
            node = target
            while(True):
                steps.append(str(node))
                if (node==parents[node]):
                    break
                node = parents[node]
            path = steps[::-1]
            print(f"Shortest path: {path}")

    def dijkstra(graph, start, target):
        INF = ((1<<63) - 1) // 2
        parents = { x:x for x in graph }
        distances = { x:INF for x in graph } 
        distances[start] = 0 # distance from start to start
        PQ = []
        heapq.heappush(PQ, [distances[start], start])

        while(PQ): # while queue is not empty
            u = heapq.heappop(PQ) # u = tuple [u_distance, u_id]
            u_id = u[1]

            if target != u_id:
                node = graph[u_id]
                for v in node['nb']:
                    v_id = v[0]
                    w_uv = v[1]
                    if distances[u_id] + w_uv < distances[v_id]:
                        distances[v_id] = distances[u_id] + w_uv
                        parents[v_id] = u_id
                        heapq.heappush(PQ, [distances[v_id], v_id])

        if distances[target] == INF:
            print("No path.")
        else:
            steps = []
            node = target
            while(True):
                steps.append(str(node))
                if (node==parents[node]):
                    break
                node = parents[node]
            path = steps[::-1]
            print(f"Shortest path: {path}")


    graph = {'c': {'pos': (1, 3), 'nb': [('b', 0.32), ('e', 0.17), ('f', 0.91)]},
            'g': {'pos': (2, 1), 'nb': [('d', 0.17), ('e', 0.27), ('h', 0.92)]},
            'i': {'pos': (3, 4), 'nb': [('e', 1.98), ('f', 0.13), ('h', 0.22)]},
            'f': {'pos': (1, 5), 'nb': [('c', 0.91), ('e', 0.33), ('i', 0.13)]},
            'h': {'pos': (3, 6), 'nb': [('e', 0.18), ('g', 0.92), ('i', 0.22)]},
            'd': {'pos': (6, 3), 'nb': [('a', 0.72), ('e', 0.29), ('g', 0.17)]},
            'a': {'pos': (6, 5), 'nb': [('b', 0.95), ('d', 0.72), ('e', 1.75)]},
            'e': {'pos': (4, 3), 'nb': [('a', 1.75), ('b', 0.82), ('c', 0.17), 
                  ('d', 0.29), ('f', 0.33), ('g', 0.27), ('h', 0.18), ('i', 1.98)]},
            'b': {'pos': (5, 6), 'nb': [('a', 0.95), ('c', 0.32), ('e', 0.82)]}}
            
    dijkstra(graph, 'a', 'i')
    a_star(graph, 'a', 'i')


if __name__ == "__main__":
    main()
