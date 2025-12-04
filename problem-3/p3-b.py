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

#Sample visualization of the table and how its working

# i\j | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13
# ----|------|------|------|------|------|------|------|------|------|------|------|------|------|-----
# 0   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''
# 1(2)| ''   | '2'  | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''
# 2(3)| ''   | '3'  | '23' | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''
# 3(4)| ''   | '4'  | '34' | '234'| ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''
# 4(2)| ''   | '4'  | '42' | '342'|'2342'| ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''   | ''
# 5(3)| ''   | '4'  | '43' | '423'|'3423'|'23423'| ''  | ''   | ''   | ''   | ''   | ''   | ''   | ''
# 6(4)| ''   | '4'  | '44' | '434'|'4234'|'34234'|'234234'| ''   | ''   | ''   | ''   | ''   | ''   | ''
# 7(2)| ''   | '4'  | '44' | '442'|'4342'|'42342'|'342342'|'2342342'| ''   | ''   | ''   | ''   | ''   | ''
# 8(3)| ''   | '4'  | '44' | '443'|'4423'|'43423'|'423423'|'3423423'|'23423423'| ''   | ''   | ''   | ''   | ''
# 9(4)| ''   | '4'  | '44' | '444'|'4434'|'44234'|'434234'|'4234234'|'34234234'|'234234234'| ''   | ''   | ''   | ''
# 10(2)| ''  | '4'  | '44' | '444'|'4442'|'44342'|'442342'|'4342342'|'42342342'|'342342342'|'2342342342'| ''   | ''   | ''
# 11(3)| ''  | '4'  | '44' | '444'|'4443'|'44423'|'443423'|'4423423'|'43423423'|'423423423'|'3423423423'|'23423423423'| ''   | ''
# 12(4)| ''  | '4'  | '44' | '444'|'4444'|'44434'|'444234'|'4434234'|'44234234'|'434234234'|'4234234234'|'34234234234'|'234234234234'| ''
# 13(2)| ''  | '4'  | '44' | '444'|'4444'|'44442'|'444342'|'4442342'|'44342342'|'442342342'|'4342342342'|'42342342342'|'342342342342'| ''
# 14(7)| ''  | '7'  | '47' | '447'|'4447'|'44447'|'444427'|'4443427'|'44423427'|'443423427'|'4423423427'|'43423423427'|'423423423427'| ''
# 15(8)| ''  | '8'  | '78' | '478'|'4478'|'44478'|'444478'|'4444278'|'44434278'|'444234278'|'4434234278'|'44234234278'|'434234234278'| ''



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