import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def input_reader(file_str):
    parsed_data = {
        "lights": {},
        "buttons": {},
        "joltage": {}
    }
    with open(file_str,"r") as f:
        lines = f.readlines()
        n =  len(lines)
        for i in range(n):
            line = lines[i].split(" ")
            joltage= line.pop().strip().strip("{").strip("}")
            joltage = [int(jolt) for jolt in joltage.split(",")]
            parsed_data["joltage"][i] = joltage
            lights = line.pop(0).strip("[").strip("]")
            parsed_data["lights"][i] = lights
            buttons = []
            for button in line:
                buttns = [int(circ) for circ in button.strip("(").strip(")").split(",")]
                buttons.append(tuple(buttns))
            parsed_data["buttons"][i] = tuple(buttons)
            #for button in line.split(","):
    return parsed_data

def solve_joltage_sum(parsed_data):
    total_min_presses = 0

    n = len(parsed_data["joltage"]) 
    
    for i in range(n):
        target_b = np.array(parsed_data["joltage"][i]) 
        buttons = parsed_data["buttons"][i]
        num_rows = len(target_b)
        num_buttons = len(buttons)
        
        A = np.zeros((num_rows, num_buttons))
        for col_idx, btn_indices in enumerate(buttons):
            for row_idx in btn_indices:
                if row_idx < num_rows:
                    A[row_idx, col_idx] = 1

        #print(A)
    
        c = np.ones(num_buttons)
        #print(c)    
        constraints = LinearConstraint(A, target_b, target_b)
        integrality = np.ones(num_buttons)
        #IDK how to this optimization without an MILP :(
        res = milp(c=c, constraints=constraints, integrality=integrality)

        if res.success:
            presses = np.round(res.x).astype(int)
            if np.array_equal(A @ presses, target_b):
                local_sum = np.sum(presses)
                total_min_presses += local_sum
            else:
                print(f"Machine {i}: Solver failed")
        else:
            print(f"Machine {i}: No valid solution")

    return total_min_presses




if __name__ == "__main__":
    data = input_reader("problem-10/real-input.txt")
    print(solve_joltage_sum(data))