
import itertools
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
            print(line)
            joltage= line.pop().strip().strip("{").strip("}")
            joltage = [int(jolt) for jolt in joltage.split(",")]
            parsed_data["joltage"][i] = joltage
            lights = line.pop(0).strip("[").strip("]")
            parsed_data["lights"][i] = lights
            buttons = []
            print(joltage)
            print(lights)
            for button in line:
                buttns = [int(circ) for circ in button.strip("(").strip(")").split(",")]
                buttons.append(tuple(buttns))
            parsed_data["buttons"][i] = tuple(buttons)
            #for button in line.split(","):
    return parsed_data
def solver(parsed_data):
    n = len(parsed_data["lights"])
    total_min_presses = 0
    results = {}
    for i in range(n):
        lights_str = parsed_data["lights"][i]
        buttons = parsed_data["buttons"][i]
        
        num_lights = len(lights_str)
        num_buttons = len(buttons)

        #target vector
        b = [1 if char == '#' else 0 for char in lights_str]
        
        #coefficient matrix
        button_cols = []
        for btn_indices in buttons:
            col = [0] * num_lights
            for idx in btn_indices:
                if 0 <= idx < num_lights:
                    col[idx] = 1
            button_cols.append(col)

        matrix = []
        for r in range(num_lights):
            row = [button_cols[c][r] for c in range(num_buttons)]
            row.append(b[r])
            matrix.append(row)
        #reduce matrix
        pivot_row = 0
        pivot_cols = [] 
        
        num_rows = len(matrix)
        num_cols = len(matrix[0]) - 1 

        for c in range(num_cols):
            if pivot_row >= num_rows:
                break

            row_with_one = -1
            for r in range(pivot_row, num_rows):
                if matrix[r][c] == 1:
                    row_with_one = r
                    break
            
            if row_with_one == -1:
                continue 

            # Swap rows to bring the 1 to the pivot position
            matrix[pivot_row], matrix[row_with_one] = matrix[row_with_one], matrix[pivot_row]

            for r in range(num_rows):
                if r != pivot_row and matrix[r][c] == 1:
                    # XOR row r with pivot_row
                    matrix[r] = [x ^ y for x, y in zip(matrix[r], matrix[pivot_row])]

            pivot_cols.append(c)
            pivot_row += 1
        

        possible = True
        for r in range(num_rows):
            if all(val == 0 for val in matrix[r][:-1]) and matrix[r][-1] == 1:
                possible = False
                break
        
        if not possible:
            print(f"Machine {i}: No solution possible.")
            results[i] = None
            continue

        free_cols = [c for c in range(num_cols) if c not in pivot_cols]
        min_presses = float('inf')
        best_solution = None

        for free_vals in itertools.product([0, 1], repeat=len(free_cols)):
            assignment = {col: val for col, val in zip(free_cols, free_vals)}
            current_x = [0] * num_buttons
            
            for f_idx, val in assignment.items():
                current_x[f_idx] = val

            for r_idx, c_idx in enumerate(pivot_cols):
                row = matrix[r_idx]
                target = row[-1]
                interaction = 0
                for f in free_cols:
                    if row[f] == 1:
                        interaction ^= current_x[f]
                current_x[c_idx] = target ^ interaction

            current_presses = sum(current_x)
            
            if current_presses < min_presses:
                min_presses = current_presses
                best_solution = current_x

        results[i] = min_presses
        if min_presses != float('inf'):
            total_min_presses += min_presses
            print(f"Machine {i}: Min Presses {min_presses} | Config: {best_solution}")

    return total_min_presses
if __name__ == "__main__":
    data = input_reader("problem-10/test-input.txt")
    print(solver(data))