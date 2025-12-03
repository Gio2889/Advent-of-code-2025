import sys
from pathlib import Path
from typing import List
from math import floor
import numpy as np
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

def max_jolt_dp(bank, k):
    n = len(bank)
    bank_str = [str(x) for x in bank] #number strings to build digits
    
    jolts_table = [['' for _ in range(k+1)] for _ in range(n+1)] # create a table to create the digits

    for i in range(1, n+1): 
        for j in range(1, min(i, k)+1):
            
            keep = jolts_table[i-1][j] #keep empty string
            
            add_num = jolts_table[i-1][j-1] + bank_str[i-1] #add number
            
            if not keep or int(add_num) > int(keep): #if there is no number and adding the next one create a large value we add it
                jolts_table[i][j] = add_num
            else:
                jolts_table[i][j] = keep
    #print(np.array(jolts_table))
    result_str = jolts_table[n][k]
    return int(result_str)



def solution(banks):
    total_joltage = 0
    for bank in banks:
        jolts=  max_jolt_dp(bank,12)
        total_joltage+=jolts
    return total_joltage


if __name__ == "__main__":
    banks =  txt_to_list_reader("problem-3/test-input.txt")
    result = solution(banks)
    print(f"Result is: {result}")