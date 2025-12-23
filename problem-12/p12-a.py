import numpy as np
def input_reader(file_str):
    gifts={}
    spaces = []
    with open(file_str,'r') as f:
        lines = f.readlines()
        k = 0
        m=0
        gift = []
        new_gift =False
        for line in lines:
            line = line.strip().split(":")
            line = [item for item in line if item]
            if len(line) == 1: #new gift or gift shape line 
                print(f"new gift on line {line}")
                elements = [char for char in line[0]]
                if len(elements) == 1: #new gift
                    new_gift = True
                    continue
                else:    
                    if new_gift:
                        gift.append(elements)
                        k+=1
                        if k==3:
                            k=0
                            new_gift =  False
                            gifts[m]=np.array(gift)
                            m+=1
                            gift = []
            elif len(line) == 2: #space and gift to pack
                space = line[0].split("x")
                x = int(space[0])
                y = int(space[1])
                array_space = np.array([['.' for _ in range(y)]for _ in range(x)])
                num_gifts = line[1].split(" ")
                num_gifts_clean = [int(num) for num in num_gifts if num]
                spaces.append([array_space,num_gifts_clean])

    return gifts,space

def solver(gifts,spaces):
    space = spaces[0]
    gift_nums = spaces[1]
    for i,gift_type in enumerate(gift_nums):
        if gift_type:
            gift = gifts[i]
            for j in range(gift_type):
                


input_reader("problem-12/test-input.txt")