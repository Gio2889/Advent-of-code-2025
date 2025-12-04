import sys
from pathlib import Path
from typing import List
from math import floor
import numpy  as np
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

def check_neighbors(array,i,j,n,m):
    neighbors_idx = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
    neighbors_count =0
    for neighbors in neighbors_idx:
        ci = neighbors[0] + i
        cj = neighbors[1] + j
        if ci < 0 or ci >= n or cj < 0 or cj >= m:
            #invalid neighbor
            continue
        if array[ci][cj] == "@":
            neighbors_count += 1
    return neighbors_count
            
def count_neighbhors(array : List[List[str]]):
    n,m = len(array),len(array[0])
    visited = {}
    can_be_accessed = 0
    for i in range(n):
        for j in range(m):
            if array[i][j] == '@':
                neighbors = check_neighbors(array,i,j,n,m)
                if neighbors < 4:
                    can_be_accessed +=1
    return can_be_accessed
                



if __name__ == "__main__":
    lines =  txt_to_list_reader("problem-4/real-input.txt")
    array = [[obj for obj in line] for line in lines] # make array 
    print(count_neighbhors(array))