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
                elements = [char for char in line[0]]
                if len(elements) == 1: #new gift
                    new_gift = True
                    continue
                else:    
                    if new_gift:
                        for j,symbol in enumerate(elements):
                            if symbol == "#":
                                gift.append((k,j))
                        k+=1
                        if k==3:
                            k=0
                            new_gift =  False
                            gifts[m] = gift
                            m+=1
                            gift = []
            elif len(line) == 2: #space and gift to pack
                space = line[0].split("x")
                x = int(space[0])
                y = int(space[1])
                array_space = (x,y)
                num_gifts = line[1].split(" ")
                num_gifts_clean = [int(num) for num in num_gifts if num]
                spaces.append([array_space,num_gifts_clean])
    return gifts,spaces

class Gift:
    def __init__(self, name, coords):
        self.name = name
        self.base_coords = set(coords)
        #add rotated shapes
        self.orientations = self._generate_orientations()

    def _rotate_point(self, x, y, angle_deg):
        #this only works if shape is arounfd( 0,0)
        if angle_deg == 0: return (x, y)
        if angle_deg == 90: return (-y, x)
        if angle_deg == 180: return (-x, -y)
        if angle_deg == 270: return (y, -x)
        return (x, y)

    def _normalize(self, coords):
        min_x = min(p[0] for p in coords)
        min_y = min(p[1] for p in coords)
        return frozenset((x - min_x, y - min_y) for x, y in coords)

    def _generate_orientations(self):
        variants = {0:self._normalize([(x,y) for x,y in self.base_coords])}
        for angle in [90, 180, 270]:
            rotated = [self._rotate_point(x, y, angle) for x, y in self.base_coords]
            normalized = self._normalize(rotated)
            # Use frozenset to make it hashable/comparable
            variants[angle] = normalized
        return variants

    def get_dimensions(self, angle):
        coords = self.orientations[angle]
        max_x = max(p[0] for p in coords)
        max_y = max(p[1] for p in coords)
        return max_x + 1, max_y + 1

    def __repr__(self):
        return f"Shape({self.name}, orientations={list(self.orientations.keys())})"

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.occupied = set() # Set of (x, y) currently filled

    def can_place(self, shape, angle, start_x, start_y):
        """Checks if a shape fits at the given grid coordinates."""
        coords = shape.orientations[angle]
        w, h = shape.get_dimensions(angle)

        #out of bounds check
        if start_x + w > self.width or start_y + h > self.height:
            return False

        # check for occupied spaces
        for dx, dy in coords:
            if (start_x + dx, start_y + dy) in self.occupied:
                return False
        return True

    def place(self, shape, angle, start_x, start_y):
        for dx, dy in shape.orientations[angle]:
            self.occupied.add((start_x + dx, start_y + dy))
    
    def find_and_place(self, gift):
        for x in range(self.width):
            for y in range(self.height):

                for angle in [0, 90, 180, 270]:
                    if self.can_place(gift, angle, x, y):
                        self.place(gift, angle, x, y)
                        return (x, y, angle) # Success
        return None # Could not fit

def can_we_fit(gifts,space):
    w,h = space[0]
    curr_space = Grid(w,h)
    gift_nums = space[1]
    # print(f"spaces {w,h}")
    # print(f"gift_nums {gift_nums}")
    for i,gift_type in enumerate(gift_nums):
        if gift_type:
            gift = gifts[i] #select the gift
            for j in range(gift_type): # iterate through number of gifts
                curr_gift = Gift(f"Gift_{i}",gift)
                if not curr_space.find_and_place(curr_gift):
                    return False
    return True

def solver(gifts,spaces):
    n=len(spaces)
    count=0
    for space in spaces:
        if can_we_fit(gifts,space):
            count+=1                
    return count



if __name__ == "__main__":
    #gifts,spaces = input_reader("problem-12/test-input.txt")
    gifts,spaces = input_reader("problem-12/real-input.txt")
    fitted_spaces = solver(gifts,spaces)
    print("How many region can fit the gifts?")
    print(fitted_spaces)
