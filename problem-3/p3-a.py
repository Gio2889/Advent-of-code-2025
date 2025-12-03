import sys
from pathlib import Path
from typing import List
from math import floor
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

def max_jolt(bank):
    curr = None 
    nxt = None
    max_jolts = 0
    n = len(bank)
    for i in range(n):
        curr = bank[i]
        for j in range(i+1,n):
            nxt = bank[j]
            test_num = int(curr+nxt)
            max_jolts = max(max_jolts,test_num)
    return max_jolts

def solution(banks):
    total_joltage = 0
    for bank in banks:
        jolts =  max_jolt(bank)
        total_joltage+=jolts
    return total_joltage


if __name__ == "__main__":
    banks =  txt_to_list_reader("problem-3/real-input.txt")
    result = solution(banks)
    print(f"Result is: {result}")