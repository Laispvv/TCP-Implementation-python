def build_dict(string_list):
    i = 0
    result = {}
    
    while (i < len(string_list)):
        result[string_list[i][0].strip()] = string_list[i][1].strip()
        i += 1
    
    return result

def destroy_dict(string_dict):
    result = ""

    for key, value in string_dict.items():
        if key == string_dict.keys()[-1]:
            result += f"{key}:{value}"
        else:
            result += f"{key}:{value},"

    return result