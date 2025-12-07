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
    max_lens ={}
    num_list= [[num for num in num_str.split(" ") if num.strip()]  for num_str in numbers] 
    matrix = np.array(num_list)
    n,m = matrix.shape
    for i in range(n):
        for j in range(m):
            if i == 0:
                max_lens[j] = len(matrix[i][j])
            else:
                max_lens[j] = max(max_lens[j],len(matrix[i][j]))

    #padding the numbers
    num_list= [[num for num in num_str.split(" ")]  for num_str in numbers]
    matrix=[]
    for i in range(len(num_list)):
        row = num_list[i]
        j=0
        col=0
        pad = ''
        curr_str = ''
        padded_list = []
        while j < len(row):
            if row[j] == '':
                row[j] = 'X' # ivalidate the space
                pad = pad+'0'          
                if curr_str: #number waiting for the pad
                    if len(curr_str+pad) == max_lens[col]: #the padding filled the number;append
                        padded_list.append(curr_str+pad)
                        curr_str = ''
                        pad=''
                        col+=1
                j+=1
            elif len(row[j]) == max_lens[col]: #properly maxed out str 
                padded_list.append(row[j])
                j+=1
                col+=1
            else: # needs padding and not ''
                if pad: # we have a pad ready
                    if not padded_list and len(pad+row[j]) == max_lens[col]:
                        padded_list.append(pad+row[j])
                        pad ='' #reset pad
                    elif padded_list and len(padded_list[-1]) == max_lens[col-1]: # the last entry is fully padded; pad this entry
                        padded_list.append(pad+row[j])
                        pad ='' #reset pad
                        
                    col+=1
                else:
                    curr_str = row[j] #queue up a number to be padded
                j+=1
        matrix.append(padded_list)
    
    #matrix is now properly padded! YAY
    matrix = np.array(matrix)
    #print(matrix)
    ceph_matrix = cephalopod_number_converter(matrix)
    # now we create the proper matrix 
    operations = [ operation for operation in operations.split(" ") if operation.strip()]
    return operations,ceph_matrix

def cephalopod_number_converter(matrix):
    n,m=matrix.shape
    ceph_matrix=[]
    for j in range(m):
        indv_num_matrix = np.array([[int(char) for char in num] for num in matrix[:,j]]).T
        clean_line = []
        for row in indv_num_matrix:
            temp_num = []
            leading = True
            for k,num in enumerate(row):
                if num == 0:
                    continue
                temp_num.append(num)
            clean_line.append(temp_num)
        ceph_matrix.append([ ''.join(str(num) for num in line) for line in clean_line])
    #print(ceph_matrix)
    return ceph_matrix

def apply_operations(operations, matrix):
    n = len(matrix)
    total = 0
    for k,operation in enumerate(operations):
        numbers = matrix[k]
        m =len(numbers)
        # here we need to reform the numbers
        row_total=int(numbers[0])
        if operation == "*":
            for num in numbers[1:]:
                row_total = row_total*int(num)
            #print(f"row total: {row_total}")
        elif operation == "+":
            for num in numbers[1:]:
                row_total = row_total+int(num)
            #print(f"row total: {row_total}")
        total+=row_total
    return total

if __name__ == "__main__":
    ### Cool set of options for printing matrices using matplot lib
    # np.set_printoptions(
    # precision=4,        # Number of decimal places
    # suppress=True,      # Suppress scientific notation for small numbers
    # threshold=10,       # Total elements before truncation
    # edgeitems=10,        # Number of edge items to show when truncated
    # linewidth=80        # Width of output line
    # )
    problems =  txt_to_list_reader("problem-6/real-input.txt",no_strip=True)
    operations,matrix = make_matrix(problems)
    result = apply_operations(operations,matrix)
    print(f"result is: {result}")
