import os

def read_file(path):
    with open(path) as file:
        dict = {
            "m" : 0,
            "T" : [], #Duration of each Parcela
            "P" : 0,
            "U" : []} #Utilities matrix
        lineCounter = 0
        for line in file:
            if(lineCounter == 0):
                dict["m"] = int(line)
            elif(lineCounter == 1):
                dict["T"] = str_to_list(line)
            elif(lineCounter == 2):
                dict["P"] = int(line)
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


