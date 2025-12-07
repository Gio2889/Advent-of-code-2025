
def txt_to_list_reader(file_name: str, no_strip=False):
    input =[]
    with open(file_name,"r") as f:
        lines = f.readlines()
        if no_strip:
            [input.append(line.replace('\n', '')) for line in lines ]
        else:
            [input.append(line.strip()) for line in lines ]
    return input