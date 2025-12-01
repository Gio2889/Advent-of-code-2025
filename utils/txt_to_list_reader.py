
def txt_to_list_reader(file_name: str):
    input =[]
    with open(file_name,"r") as f:
        lines = f.readlines()
        [input.append(line.strip()) for line in lines ]
    return input