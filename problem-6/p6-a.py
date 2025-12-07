import sys
from pathlib import Path
from typing import List
from math import floor
import numpy  as np
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

def make_matrix(problems):
    operations = problems[-1]
    numbers = problems[:-1]
    num_list = []
    #spell it out its easier to track; one liner below
    for nums in numbers:
        temp_num =[]
        for num in nums.split(" "):
            if num.strip():
                temp_num.append(int(num))
        num_list.append(temp_num)

    # num_list= [[int(num) for num in num_str.split(" ") if num.strip()]  for num_str in numbers] 
    matrix = np.array(num_list)
    operations = [ operation for operation in operations.split(" ") if operation.strip()]
    return operations,matrix

def apply_operations(operations, matrix):
    print(matrix)
    matrix_t = matrix.T
    n,m = matrix_t.shape
    total = 0
    for k,operation in enumerate(operations):
        numbers = matrix_t[k]
        row_total=numbers[0] 
        if operation == "*":
            for num in numbers[1:]:
                row_total = row_total*num
            #print(f"row total: {row_total}")
        elif operation == "+":
            for num in numbers[1:]:
                row_total = row_total+num
            #print(f"row total: {row_total}")
        total+=row_total
    return total

if __name__ == "__main__":
    ### Cool set of options for printing matrices using matplot lib
    np.set_printoptions(
    precision=4,        # Number of decimal places
    suppress=True,      # Suppress scientific notation for small numbers
    threshold=10,       # Total elements before truncation
    edgeitems=10,        # Number of edge items to show when truncated
    linewidth=80        # Width of output line
    )
    problems =  txt_to_list_reader("problem-6/real-input.txt")
    operations,matrix = make_matrix(problems)
    result = apply_operations(operations,matrix)
    if result != 3263827+234:
        print("NOOOOOOO!") 
    print(f"result is: {result}")
