import sys
from pathlib import Path
from typing import List,Tuple,AnyStr
from math import floor
import numpy  as np
import time
sys.path.append(str(Path(__file__).parent.parent))
from utils.txt_to_list_reader import txt_to_list_reader

class ServerPath:
    def __init__(self,source):
        self.source = source
        self.connections =[]

    def connect(self,other_path:ServerPath):
        if other_path not in self.connections:
            self.connections.append(other_path)
    
    def __repr__(self):
        return f"Node({self.source})"

# from problem 7 need to refactor
# def count_unique_paths(root_node):
#     known_paths = {}
    
#     def traversal(current_node):
#         if current_node in known_paths:
#             return known_paths[current_node]
        
#         if not current_node.connections:
#             known_paths[current_node] = 1 
#             return 1
#         total_paths = 0
#         for next_node in current_node.connections:
#             total_paths += traversal(next_node)
        
#         known_paths[current_node] = total_paths
#         return total_paths
    
#     return traversal(root_node)

##part b search:

def count_unique_paths(root_node,required_nodes):
    known_paths = {}
    required_nodes =  frozenset(required_nodes)

    def traversal(current_node,seen_checks):
        if current_node.source in required_nodes:
            current_seen = seen_checks | {current_node.source} #build the set for this path
        else:
            current_seen = seen_checks #no checkpoint added
        
        state = (current_node,current_seen)
        if state in known_paths:
            return known_paths[state]
        
        if not current_node.connections:
            if required_nodes.issubset(current_seen): # if the two check point are a subset we viisted them
                known_paths[state] = 1 
                return 1
            else:
                known_paths[state] = 0
                return 0
        total_paths = 0
        for next_node in current_node.connections:
            total_paths += traversal(next_node,current_seen)
        
        known_paths[state] = total_paths
        return total_paths
    
    return traversal(root_node,frozenset())


def path_counter(clean_paths):
    known_paths = {}
    #create all the nodes
    for source, connections in clean_paths.items():
        new_path = ServerPath(source)
        if source not in known_paths:
            known_paths[source] = new_path
        for connection in connections:
            if connection not in known_paths:
                known_paths[connection]= ServerPath(connection)
    
    #link and create the server paths
    for source, connections in clean_paths.items():
        source_path = known_paths[source]
        for connection in connections:
            connection_path = known_paths[connection]
            source_path.connect(connection_path)
    

    # find the starts and go
    #part B  change 'you' to 'svr'
    if 'svr' in known_paths:
        root = known_paths['svr']
        return count_unique_paths(root,['dac','fft'])
    else:
        return 0

if __name__ == "__main__":
    paths =  txt_to_list_reader("problem-11/real-input.txt")
    paths_clean={}
    for str_paths in paths:
        splits = str_paths.split(":")
        paths_clean[splits[0]] = splits[1].strip().split(" ")
    print(path_counter(paths_clean))
    