import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.txt_to_list_reader import txt_to_list_reader

def compare_numbers(a, b):
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def add_one(num_str):
    num = list(num_str)
    carry = 1
    
    for i in range(len(num) - 1, -1, -1): # go backwards 
        digit = int(num[i]) + carry
        if digit == 10:
            num[i] = '0'
            carry = 1
        else:
            num[i] = str(digit)
            carry = 0
            break
    
    if carry:
        return '1' + ''.join(num)
    return ''.join(num)

def sub_numbers(a, b):
    max_len = max(len(a), len(b))
    #have to pad the number so they are the same len
    a_padded = a.zfill(max_len)
    b_padded = b.zfill(max_len)
    
    result = []
    borrow = 0
    
    for i in range(max_len - 1, -1, -1):
        digit_a = int(a_padded[i])
        digit_b = int(b_padded[i])
        
        digit_a -= borrow
        if digit_a < digit_b:
            digit_a += 10
            borrow = 1
        else:
            borrow = 0
        
        result.append(str(digit_a - digit_b))
    
    # Remove leading zeros
    result_str = ''.join(reversed(result)).lstrip('0')
    return result_str if result_str else '0'

def add_numbers(a, b):
    max_len = max(len(a), len(b))
    a_padded = a.zfill(max_len)
    b_padded = b.zfill(max_len)
    
    result = []
    carry = 0
    
    for i in range(max_len - 1, -1, -1):
        digit_sum = int(a_padded[i]) + int(b_padded[i]) + carry
        result.append(str(digit_sum % 10))
        carry = digit_sum // 10
    
    if carry:
        result.append(str(carry))
    
    return ''.join(reversed(result))

def merge_ranges(ranges):    
    parsed_ranges = []
    for r in ranges:
        low, high = r.split('-')
        parsed_ranges.append((low, high))
    
    parsed_ranges.sort(key=lambda x: (len(x[0]), x[0]))
    print(parsed_ranges)
    merged = []
    current_low, current_high = parsed_ranges[0]
    
    for low, high in parsed_ranges[1:]:

        current_high_plus_one = add_one(current_high)
        
        #compare and merge
        if compare_numbers(low, current_high_plus_one) <= 0:
            if compare_numbers(high, current_high) > 0:
                current_high = high
        else:
            # No overlap
            merged.append((current_low, current_high))
            current_low, current_high = low, high
    
    merged.append((current_low, current_high))
    return merged

def count_items_in_ranges(ranges):
    merged = merge_ranges(ranges)
    #print(merged)
    total = '0'
    
    for low, high in merged:
        diff = sub_numbers(high, low)  
        count = add_one(diff)  # add one cause range is inclusive
        total = add_numbers(total, count)
    
    return total



def split_inventory(inventory):
    dict_type = "ranges"
    ranges = []
    #ranges ={}
    ids = []
    k = 1
    for item in inventory:
        if not item:
            dict_type ="ids"
            continue
        # if dict_type == "ranges":
        #     nums=item.split("-")
        #     ranges[k] = [num for num in range(int(nums[0]),int(nums[-1])+1)]
        #     k+=1
        if dict_type == "ranges":
            nums=item.split("-")
            ranges.append((int(nums[0]),int(nums[1])))
        else:
            ids.append(item)
    return ranges,ids

if __name__ == "__main__":
    inventory =  txt_to_list_reader("problem-5/real-input.txt")
    #print(inventory)
    ranges,ids = split_inventory(inventory)
    print(count_items_in_ranges(ranges))