
graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B']),
         'F': set(['C'])}


#############################################################################
# non-recursive dfs, using stack

def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        print stack
        vertex = stack.pop()
        if vertex not in visited:
            print vertex
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        print stack
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            print next
            if next == goal:
                return path + [next]
            else:
                stack.append((next, path + [next]))
                
def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        print queue
        vertex = queue.pop(0)
        if vertex not in visited:
            print vertex
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)       
    return visited
 
def dfs2(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print visited
    for next in graph[start] - visited:
        print next
        dfs2(graph, next, visited)
    return visited

def dfs2_paths(graph, start, ):
                

                

if __name__ == '__main__':
    #dfs(graph, 'A') 
    #dfs_recursive(graph, 'A', 'F')
    #dfs_paths_recursive(graph, 'A', 'F')
    
    #p = dfs_paths(graph, 'A', 'F')
    #print p
    dfs2(graph, 'A')



