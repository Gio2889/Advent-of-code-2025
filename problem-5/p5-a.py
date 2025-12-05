import sys
from pathlib import Path
from typing import List
from math import floor
import numpy  as np
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

#### good thought but number are too big ###
def split_inventory(inventory):
    dict_type = "ranges"
    ranges = []
    #ranges ={}
    ids = []
    k = 1
    for item in inventory:
        if not item:
            dict_type ="ids"
            continue
        # if dict_type == "ranges":
        #     nums=item.split("-")
        #     ranges[k] = [num for num in range(int(nums[0]),int(nums[-1])+1)]
        #     k+=1
        if dict_type == "ranges":
            ranges.append(item)
        else:
            ids.append(item)
    return ranges,ids

# def is_fresh(ranges,ids):
#     fresh =[]
#     fresh_ids = set()
#     for _,fresh_set in ranges.items():
#         fresh_ids = fresh_ids| set(fresh_set)
#     for ingridient_id in ids:
#         if int(ingridient_id) in fresh_ids:
#             fresh.append(True)
#         else:
#             fresh.append(False)
#     return sum(fresh)

def is_in_range(ranges,id_str):
    possible_ranges = []
    for pos_range in ranges:
        nums=pos_range.split("-")
        low,high = nums[0],nums[-1]
        if len(id_str) < len(low) or len(id_str) > len(high):
            continue
        else:
            possible_ranges.append((low,high))
    for low,high in possible_ranges:
        n,l,h =len(id_str), len(low), len(high)

        if n < l or n > h: # fully out 
            continue
        
        if n == l and id_str < low: # similar to low but check to see if its higher
            continue
        
        if n == h and id_str > high: # similar to high but chek if its lower
            continue
        
        if l < n < h: # it between; easy fit 
            return True
        
        if n == l == h and low <= id_str <= high: # full check, len matches low and high
            return True
        
        # matches a range but 
        if n == l and l < h and id_str >= low:
            return True
        if n == h and l < h and id_str <= high:
            return True
    
    return False


def is_fresh(ranges,ids):
    fresh =[]
    for ingredient_id in ids:
        if is_in_range(ranges,ingredient_id):
            fresh.append(True)
        else:
            fresh.append(False)
    return sum(fresh)

######################################

if __name__ == "__main__":
    inventory =  txt_to_list_reader("problem-5/test-input.txt")
    #print(inventory)
    ranges,ids = split_inventory(inventory)
    print(ranges[:5])
    print(ids[:5])
    print(is_fresh(ranges,ids))