import sys
from pathlib import Path
from typing import List
from math import floor
import numpy  as np
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

class Junction_Box():
    def __init__(self, x,y,z):
        self.x=x
        self.y=y
        self.z=z
        self.connected =  False
        self.connections = []

    def __repr__(self):
        return f"Junction_Box({self.x},{self.y},{self.z})"

    def coords(self):
        return self.x,self.y,self.z

    def distance(self,box: Junction_Box):
        return np.sqrt((box.x-self.x)**2 + (box.y-self.y)**2 + (box.z-self.z)**2)

    def connect(self,box: Junction_Box):
        if box not in self.connections:
            self.connections.append(box)
            self.connected = True
        if self not in box.connections:
            box.connections.append(self)
            box.connected = True
    
def count_clusters(boxes : List[Junction_Box]):
    visited = set()
    clusters = []
    
    def depth_search(box):
        stack = [box]
        cluster_members = []
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                cluster_members.append(current)
                for neighbor in current.connections:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return cluster_members
    
    for box in boxes:
        if box not in visited:
            cluster_member = depth_search(box)
            clusters.append(cluster_member)
    
    return len(clusters),clusters

def print_clusters(clusters: List[List[Junction_Box]]):
    """Prints detailed information about each cluster and returns unique sizes in order"""
    print("\n" + "="*60)
    print("CLUSTER DETAILS:")
    print("="*60)


    # for looking at allt he connections  
    # for i, cluster in enumerate(clusters, 1):
    #     print(f"\nCluster {i} (Size: {len(cluster)} boxes):")
    #     print("-" * 40)
        
    #     for j, box in enumerate(cluster, 1):
    #         connections_list = [f"({conn.x},{conn.y},{conn.z})" for conn in box.connections]
    #         print(f"  Box {j}: ({box.x},{box.y},{box.z})")
    #         print(f"    Connections: {connections_list}")
    
    print("\n" + "="*60)
    print(f"Total clusters: {len(clusters)}")
    
    cluster_sizes = [len(cluster) for cluster in clusters]
    
    unique_sizes = sorted(set(cluster_sizes), reverse=True)
    
    print("\nCluster size distribution:")
    size_counts = {}
    for cluster in clusters:
        size = len(cluster)
        size_counts[size] = size_counts.get(size, 0) + 1
    
    for size in sorted(size_counts.keys()):
        print(f"  Size {size}: {size_counts[size]} cluster(s)")
    
    # Print unique sizes in order
    print(f"\nUnique cluster sizes (descending order): {unique_sizes}")
    
    # Calculate answer
    if len(unique_sizes) >= 3:
        product = unique_sizes[0] * unique_sizes[1] * unique_sizes[2]
        print(f"\nMultiplication of three largest unique sizes:")
        print(f"  {unique_sizes[0]} × {unique_sizes[1]} × {unique_sizes[2]} = {product}")
    elif len(unique_sizes) > 0:
        print(f"\nOnly {len(unique_sizes)} unique cluster size(s) available.")
        if len(unique_sizes) == 2:
            product = unique_sizes[0] * unique_sizes[1]
            print(f"Multiplication of two largest unique sizes:")
            print(f"  {unique_sizes[0]} × {unique_sizes[1]} = {product}")
        else:  # len(unique_sizes) == 1
            print(f"Only one unique size: {unique_sizes[0]}")
    else:
        print("\nNo clusters found.")
    
    isolated = sum(1 for cluster in clusters if len(cluster) == 1)
    if isolated > 0:
        print(f"\nNote: {isolated} isolated box(es) found")
    return unique_sizes

def get_circuits(coords):
    num_coords = []
    for coord_set in coords:
        temp_coords = [ int(num) for num in coord_set.split(",")]
        num_coords.append(Junction_Box(temp_coords[0],temp_coords[1],temp_coords[2]))

    
    n=len(num_coords)
    pairs = [] #better to keep a single list
    # create a matrix with the distances:
    #matrix = np.array([[ np.inf for _ in range(n)] for _ in range(n)])
    for i in range(n):
        for j in range(n):
                if i==j or i>j: #compute only half of the distances
                    continue
                else:
                    dist = num_coords[i].distance(num_coords[j])
                    pairs.append((dist, i, j))

    pairs.sort(key=lambda x: x[0]) # sort by ditance
    print(f"Generated {len(pairs)} unique pairs, sorted by distance")
    for dist,i,j in pairs:
        box1 = num_coords[i]
        box2 = num_coords[j]
        #if not box1.connected or not box2.connected:
        box1.connect(box2) #connect 1 -> 2
        ############### part B
        cluster_count, clusters = count_clusters(num_coords)
        if cluster_count==1:
            print(box1.x,box2.x,box1.x*box2.x)
            break
        ##################################
    #part A 
    #cluster_count, clusters = count_clusters(num_coords)
    #################################################
    print_clusters(clusters)

    ###################################################################
    # Matrix implementation (SCRATCHED)
    # smallest_element = -99999999 
    # while smallest_element != np.inf:
    #     smallest_element = np.min(matrix)
    #     indices_of_smallest = np.where(matrix == smallest_element)
    #     i = indices_of_smallest[0][0]
    #     j = indices_of_smallest[1][0]
    #     box1 = num_coords[i]
    #     box2 = num_coords[j]
    #     if not box1.connected or not box2.connected:
    #         box1.connect(box2) #connect 1 -> 2
        #box2.connect(box1) #conenct 2 -> 1
        # print(f"{num_coords[i].coords()} connecter to {num_coords[j].coords()}")
        # print(f"{num_coords[0].coords()} connections: { [box.coords() for box in num_coords[i].connections ]}")
        #atrix[i,j] = np.inf
    

    
    
if __name__ == "__main__":
    ### Cool set of options for printing matrices using matplot lib
    np.set_printoptions(
    precision=4,        # Number of decimal places
    suppress=True,      # Suppress scientific notation for small numbers
    threshold=15,       # Total elements before truncation
    edgeitems=15,        # Number of edge items to show when truncated
    linewidth=150        # Width of output line
    )
    box_coords =  txt_to_list_reader("problem-8/real-input.txt")
    get_circuits(box_coords)