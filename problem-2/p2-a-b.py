import sys
from pathlib import Path
from typing import List
from math import floor
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

def id_checker(ids: List[str]):
    total=0
    known_invalid=set()
    for id_str in ids:
        split_id = id_str.split("-")
        n_l,m_l = len(split_id[0]),len(split_id[1]) #number of digts of the rages
        n,m = int(split_id[0]),int(split_id[1]) #ints for the ranges
        for num in range(n,m+1):
            s=str(num) #turn the number into str for easy managment
            #basic check for reapeting numbers
            all_num = [s[i:i+1] for i in range(0, len(s))]
            if is_invalid(all_num):
                all_num = int(''.join(all_num))
                if all_num not in known_invalid:
                    known_invalid.add(all_num)
                    print(f"Invalid Id: {all_num}")
                    total+=all_num
            
            #j=2 # number of repeating elements #PART A restrict this to 2
            for j in range (2,len(s)+1):# PART B do a loop to check all groupings
                if len(s)%j == 0 and len(s)>j:
                    k=int(len(s)/j)
                    all_num = [s[i:i+k] for i in range(0, len(s), k)]
                    if is_invalid(all_num):
                        all_num = int(''.join(all_num))
                        if all_num not in known_invalid:
                            known_invalid.add(all_num)
                            print(f"Invalid Id: {all_num}")
                            total+=all_num
                else:
                    continue
    return total


def is_invalid(lst : List[str]):
    known = {}
    for x in lst:
        if x in known.keys():
            known[x]+=1
        else:
            known[x]=1  
    # if len(lst) in known.values() and len(lst)==2: #only one type of duplicate PART A
    if len(lst) in known.values() and len(lst)>1: #only one type of duplicate PART B
        return True
    return False


if __name__ == "__main__":
    ids =  txt_to_list_reader("problem-2/real-input.txt")[0].split(",")
    results = id_checker(ids)
    print(f"Result is: {results}")