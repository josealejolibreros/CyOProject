import os

def read_file(path):
    with open(path) as file:
        dict = {
            "m" : 0,
            "TC" : [], #Duration of each Parcela
            "P" : 0,
            "U" : []} #Utilities matrix
        lineCounter = 0
        for line in file:
            if(lineCounter == 0):
                dict["P"] = int(line)
            elif(lineCounter == 1):
                dict["TC"] = str_to_list(line)
            elif(lineCounter == 2):
                dict["m"] = int(line)
            else:
                dict["U"].append(str_to_list(line))
            lineCounter += 1
        return dict

def str_to_list(string):
    string = str(string).strip()
    list = string.split(" ")
    
    for i in range(len(list)):
        list[i] = int(list[i])

    return list

if __name__ == "__main__":
    path_to_file = os.path.dirname(os.path.realpath(__file__)) + "\\test.txt"
    print(path_to_file)
    read_file(path_to_file)
