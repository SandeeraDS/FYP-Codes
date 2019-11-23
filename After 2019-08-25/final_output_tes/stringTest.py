import numpy as np
f = open("6.txt", "r")

content1 = f.read()
print(content1)
print("----------------------------")
f = open("7.txt", "r")

content2 = f.read()
print(content2)
print("----------------------------")
print("----------------------------")
splitA = list(content1.split("\n"))
splitB = list(content2.split("\n"))

for line in splitA:
    if line in splitB:
        splitB.remove(line)

new_string = "\n".join(splitB)
print(new_string.strip())
