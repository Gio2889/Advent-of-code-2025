import sys
from pathlib import Path
from typing import List
from math import floor
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

def password_cracker( inputs: List[str],initial_value: int = 50):
    passwd = 0
    val = initial_value
    prev_val = initial_value
    for turn in inputs:
        side,how_much = turn[0], int(turn[1:])
        extra_clicks = floor(how_much/100) # handles extra clicks for large numbers #PART B extra
        print(f"turn: {side}; much: {how_much}; extra: {extra_clicks}")
        how_much = how_much%100
        if side == 'L':
            val-=how_much
        elif side =='R':
            val+=how_much
        else:
            pass
        if val < 0:
            if prev_val != 0:
                passwd+=1 #PART B extra
            val = 100 + val #val is negative we add
        elif val > 99:
            val = val - 100
            if val != 0:
                passwd+=1 #PART B extra
                #print("-----> click on the right")
        if extra_clicks != 0:
            #print(f"extra clicks {extra_clicks}")
            passwd+=extra_clicks
        if val == 0:
            passwd+=1
            #print("-----> click on 0")
        prev_val = val
    return passwd


if __name__ == "__main__":
    input =  txt_to_list_reader("problem-1/real-input.txt")
    passwd = password_cracker(input)
    print(f"The password is:\n {passwd}")