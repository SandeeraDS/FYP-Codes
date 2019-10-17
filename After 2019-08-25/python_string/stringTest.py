name = "   sande er " \
       "dddsds sds sds sdd                   dsdsd ddsd      dsds     "

name2 = "   sande er " \
       "dddsds sds sds sdd                   dsdsd ddsd      dsdsa"
newString1 = "".join(name.split())
newString2 = "".join(name2.split())

print(newString1)
print(newString2)

# print(name.strip())

print(newString1 != newString2)