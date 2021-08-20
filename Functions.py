def build_dict(string_list):
    i = 0
    result = {}
    string_list = string_list.split(",")
    string_list = list(map(lambda x : x.split(":"), string_list))
    while (i < len(string_list)):
        result[string_list[i][0].strip()] = string_list[i][1].strip()
        i += 1
    return result

def destroy_dict(string_dict):
    result = ""

    for key, value in string_dict.items():
        if key == list(string_dict.keys())[-1]:
            result += f"{key}:{value}"
        else:
            result += f"{key}:{value},"

    return result