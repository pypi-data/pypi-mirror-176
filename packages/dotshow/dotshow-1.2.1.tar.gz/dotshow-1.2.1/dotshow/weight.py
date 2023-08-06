def weight_match(weight, gray):
    if gray:
        weight = 255 - weight
        
    if weight > 240:
        return "₩"
    elif weight > 220:
        return "N"
    elif weight > 200:
        return "B"
    elif weight > 180:
        return "H"
    elif weight > 160:
        return "O"
    elif weight > 140:
        return "U"
    elif weight > 120:
        return "C"
    elif weight > 100:
        return "L"
    elif weight > 90:
        return "o"
    elif weight > 70:
        return "i"
    elif weight > 50:
        return ":"
    elif weight > 20:
        return "."
    else:
        return " "

def color_match(weight):
    return f"\033[38;2;{weight[2]};{weight[1]};{weight[0]}m▒\033[0m"