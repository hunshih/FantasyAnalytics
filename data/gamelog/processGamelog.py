import os
import re

def clean(str):
    cleanString = re.sub('\W+','', str)
    return cleanString

def combine(ary):
    output = ""
    size = len(ary)
    count = 1
    for item in ary:
        output += item;
        if count < size:
            output += ","
        count += 1
    output += "\n"
    return output

def process():
    target = open("perflog.csv", "w")
    dirFiles = os.listdir('.') #list of directory files
    dirFiles.sort() #good initial sort but doesnt sort numerically very well
    sorted(dirFiles) #sort numerically in ascending order
    for filename in dirFiles:
        if filename.endswith(".csv"): 
            #print(filename)
            yearMatch = re.search('.*_(\d{4}).csv', filename)
            if yearMatch:
                year = yearMatch.group(1)
                with open(filename, "r") as lines:
                    lineNum = 0
                    for line in lines:
                        if lineNum < 1:
                            lineNum += 1
                            continue
                        else:
                            data = line.split(',')
                            output = [year, data[1], clean(data[2]), data[9]]
                            target.write(combine(output))
                            lineNum += 1


def main():
    process()


main()	