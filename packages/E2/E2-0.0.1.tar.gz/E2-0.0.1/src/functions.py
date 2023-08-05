def read_content(filename:str):
    f = open("demofile.txt", "r")
    return f.read()
    
def read_lines(filename:str):
    arr = []
    f = open("demofile.txt", "r")
    for x in f:
        arr.append(x)
    return arr
