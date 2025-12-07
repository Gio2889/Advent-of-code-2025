import sys
from pathlib import Path
from typing import List
from math import floor
import numpy  as np
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

# def to_check_from_current(grid,ci,cj,di,dj):
#     to_check = []
#     if grid[ci,cj] == 'S':
class Beam:
    def __init__(self, i,j,name='Beam'):
        self.i = i
        self.j = j
        self.name = name
        self.next_beams = []

    def add_beam(self,beam):
        if beam not in self.next_beams:
            self.next_beams.append(beam)

def count_total_beams(beam, visited=None):
    if visited is None:
        visited = set()
        
    if beam in visited:
        return 0
    
    visited.add(beam)
    
    count = 1 # count THIS beam
    for child in beam.next_beams:
        count += count_total_beams(child, visited)
    return count

######### PART B HERE #############
def count_unique_paths(root):
    known_paths = {}
    
    def traversal(beam):
        if beam in known_paths:
            return known_paths[beam]
        
        if not beam.next_beams: #isolated beam; only one way here
            known_paths[beam] = 1 
            return 1
        
        total_paths = 0
        for next_beam in beam.next_beams:
            total_paths += traversal(next_beam)
        
        known_paths[beam] = total_paths
        return total_paths
    
    return traversal(root)
################################################
def get_tachy_paths(tachy_lines):
    tachy_map = np.array([[space for space in line] for line in tachy_line])
    # print(tachy_map)
    # print(tachy_map.shape)
    n,m = tachy_map.shape
    to_check =[]
    splits = 0
    break_outer = False
    for i in range(n):
        if break_outer:
            break
        for j in range(m):
            if tachy_map[i,j]=='S':
                #root =  Beam(i,j,"Start") #create the beam here
                to_check.append((i+1,j,None))
                break_outer = True
                break
    root = None
    known_beams = {}
    known_spliters ={}
    known_merges ={}
    current_beam = None
    while to_check:
        #print(to_check)
        ci,cj,parent_beam = to_check.pop()

        if (ci,cj) in known_beams:
            current_beam = known_beams[(ci,cj)] #use the beam already at that position
            #link to previous beam (parent) then break
            parent_beam.add_beam(current_beam)
            continue    

        current_beam = Beam(ci, cj)
        known_beams[(ci,cj)] = current_beam

        if root is None:
            root = current_beam
            root.name = 'Start'
    
        if parent_beam:
            parent_beam.add_beam(current_beam)

        if tachy_map[ci,cj] == '.' or tachy_map[ci,cj] == '|':
            tachy_map[ci,cj] = '|' #update value for path

            
            #check arround paths for splitters
            for near in [(0,1),(0,-1),(1,0),(-1,0)]:
                di = ci +near[0]
                dj = cj +near[1]
                if di < 0 or di >= n or dj < 0 or dj >= m:
                    continue
                if tachy_map[di,dj]=='^' and di > ci: #append spliter to the queue; ONLY IF IF GETTING HIT BY A BEAM!
                    to_check.append((di,dj,current_beam))
                elif tachy_map[di,dj]=='.' and di > ci: #space is empty and is BELOW the beam
                    to_check.append((di,dj,current_beam))
                elif tachy_map[di,dj] == '|' and di > ci: # we connect to an exisiting beam
                    if (ci,cj) not in known_merges:
                        known_merges[(ci,cj)]=(ci,cj)
                    to_check.append((di,dj,current_beam))
                
        elif tachy_map[ci,cj] == '^': # append the two path on each side of the spliter to the queue
            current_beam.name = "Splitter"
            if (ci,cj) not in known_spliters:
                known_spliters[ci,cj]=(ci,cj)
                to_check.append((ci,cj+1,current_beam)) #right side 
                to_check.append((ci,cj-1,current_beam)) #left side
                tachy_map[ci,cj] ='+' #paint over to know it got counted
            else:
                tachy_map[ci,cj] ='&' #paint to signify double count

    num_beams = count_total_beams(root)
    splits = len(known_spliters)
    merges = len(known_merges)
    unique_paths = count_unique_paths(root)
    return num_beams,splits,merges,unique_paths
            

if __name__ == "__main__":
    tachy_line =  txt_to_list_reader("problem-7/real-input.txt")
    paths,splits,merges,unique_paths = get_tachy_paths(tachy_line)
    print(f"The number of paths is {paths} by spliting the beam {splits} times with {merges} merges and {unique_paths} paths")