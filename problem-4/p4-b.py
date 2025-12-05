import sys
from pathlib import Path
from typing import List
from math import floor
import numpy  as np
import matplotlib.pyplot as plt
from PIL import Image
import copy
import os
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

def check_state(array : List[List[str]]):
    queued = []
    n,m = len(array),len(array[0])
    for i in range(n):
        for j in range(m):
            if array[i][j] == '@':
                neighbors = check_neighbors(array,i,j,n,m)
                if neighbors < 4:
                    queued.append((i,j))
    return queued

def count_neighbhors(array : List[List[str]]):
    n,m = len(array),len(array[0])
    removed = 0
    array_curr = array.copy()
    array_storage =[copy.deepcopy(array_curr)]
    while True:
        #check current state and makes removal
        queued = check_state(array_curr)
        if not queued:
            #no states to remove; we are done. Rerturnt he total
            return removed,array_storage

        while queued:
            # while we have elements edit the state
            element = queued.pop()
            ci,cj = element[0],element[1]
            array_curr[ci][cj] = '.'
            removed+=1
        array_storage.append(copy.deepcopy(array_curr)) # store the array

def make_numerical(array):
    n,m = len(array),len(array[0])
    n,m = len(array),len(array[0])
    for i in range(n):
        for j in range(m):
            if array[i][j] == '@':
                array[i][j]=1
            else:
                array[i][j]=0
    
    return np.array(array)

def make_image(array,k,width):
    plt.imshow(array, cmap='viridis') 
    #plt.colorbar(label='Value') 
    plt.axis('off')
    plt.title(f'State {k}')
    plt.savefig(f"problem-4/figures/state_{k:0{width}d}.png",dpi=800)
    plt.close()

def make_gif(image_folder, output_filename="problem-4/figures/state_progress.gif", duration=500, loop=0):
    images = []
    filenames = sorted([os.path.join(image_folder, f) 
                       for f in os.listdir(image_folder) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
    
    if not filenames:
        print("No images found in the specified folder.")
        return
    
    try:
        for filename in filenames:
            images.append(Image.open(filename))
        
        last_image = images[-1]

        
        images = images + [last_image] * (5 - 1)

        images[0].save(
            output_filename,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=loop,
            optimize=True)
        print(f"GIF '{output_filename}' created successfully!")
        
    except Exception as e:
        print(f"Error creating GIF: {e}")
   
def visualize_states(arrays):
    numerical_arrays=[]
    
    for array in arrays:
        numerical_arrays.append(make_numerical(array))
    total_states = len(numerical_arrays)
    width = len(str(total_states-1)) if total_states > 1 else 1    
    for k,array in enumerate(numerical_arrays):
        make_image(array,k,width)
    make_gif("problem-4/figures")



if __name__ == "__main__":
    ### Cool set of options for printing matrices using matplot lib
    # np.set_printoptions(
    # precision=4,        # Number of decimal places
    # suppress=True,      # Suppress scientific notation for small numbers
    # threshold=10,       # Total elements before truncation
    # edgeitems=10,        # Number of edge items to show when truncated
    # linewidth=80        # Width of output line
    # )
    lines =  txt_to_list_reader("problem-4/real-input.txt")
    array = [[obj for obj in line] for line in lines] # make array 
    removed,arrays = count_neighbhors(array)
    print(f"Rolls removed: {removed}")
    visualize_states(arrays)
