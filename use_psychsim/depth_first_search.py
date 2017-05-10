
graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B']),
         'F': set(['C'])}


#############################################################################
# non-recursive search, using stack

# def search(graph, start):
#     print '----------------'
#     print "begin " + str(start) 
#     visited, stack = set(), [start]
#     while stack:
#         vertex = stack.pop()
#         if vertex not in visited:
#             print vertex
#             visited.add(vertex)
#             stack.extend(graph[vertex] - visited)
#             
#     print "end " + str(start) + " " + str(visited)
#     return visited

#search(graph, 'A') 

###########################################################################
# stop when goal is found, return true

def dfs_recursive1(graph, start, goal, visited=set()):

    print '----------------'
    print "start: <%s>" % start + " goal: " + str(goal)
    
    visited.add(start)
    print "visited: " + str(visited)
    
    if start == goal:
        print "finish: <%s>" % start + " I found goal!"
        return True
    
    
    neighbors = graph[start] - visited
    print "unvisited neighbors: " + str(neighbors)
    for nb in neighbors:
        print "nb: " + str(nb)
        ret_val = dfs_recursive1(graph, nb, goal, visited)
        if ret_val == True:
            print "finish: <%s>" % start + " I found goal!"
            return True
        
    return False   

#dfs_recursive1(graph, 'A', 'F') 

#########################################################################
# stop when goal is found, return set of visited nodes

def dfs_recursive2(graph, start, goal, visited=set()):

    print '----------------'
    print "start: <%s>" % start + " goal: " + str(goal)

    visited.add(start) 
    print "visited: " + str(visited)
    
    if start == goal:
        print "finish: <%s>" % start + " I found goal!"
        return visited
    
    
    neighbors = graph[start] - visited
    print "unvisited neighbors: " + str(neighbors)
    for nb in neighbors:
        print "nb: " + str(nb)
        ret_val = dfs_recursive2(graph, nb, goal, visited)
        #print "ret_val: " + str(ret_val)
        if goal in ret_val:
            print "finish: <%s>" % start + " My neighbor found goal!"
            return ret_val
        
    return set()    
      
#dfs_recursive2(graph, 'A', 'F')     


def dfs_paths_recursive(graph, start, goal, path=[('', 'A')]):
    print '----------------'
    print "start: <%s>" % start + " goal: " + str(goal)
    
    #path.append(start)
    print "accumulated path: " + str(path)
    
    if start == goal:
        print "finish: <%s>" % start + " I found goal!"
        print "return path: " + str(path)
        return path
    
    
    visited = set([x[1] for x in path])
    neighbors = graph[start] - visited
    
    print "unvisited neighbors: " + str(neighbors)
    for nb in neighbors:
        print "nb: " + str(nb)
        path.append((start, nb))
        ret_path = dfs_paths_recursive(graph, nb, goal, path)
        for pair in ret_path:
            if goal in pair:
                print "finish: <%s>" % start + " My neighbor found goal!"
                print "return path: " + str(ret_path)
                return ret_path
        
    return []
 
dfs_paths_recursive(graph, 'A', 'F')

