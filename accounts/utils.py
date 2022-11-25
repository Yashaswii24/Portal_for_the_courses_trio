import math, random 
"""With the size of the number of digits and list of existing codes it generates a new code which is used as course code
"""  
def generate_class_code(total_digits,existing_codes) :  
    digits = ''.join([str(i) for i in range(0,10)])
    code = ""  
    while True:
        for i in range(total_digits) : 
            code += digits[math.floor(random.random() * 10)] 
        if code not in existing_codes:
            print('Code not in existing codes')
            break
    return code 