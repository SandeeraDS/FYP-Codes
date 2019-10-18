import re

name = "   sande er " \
       "dddsds sds sds sdd                   dsdsd ddsd      dsds     "

name2 = "   sande er " \
       "dddsds sds sds sdd                   dsdsd ddsd      dsdsa"

name3 = "   BCVFE | sande er " \
       "dddsds sds sds sdd      2   ..       3   dsdsd ddsd  ?    dsdsA1"

newString1 = "".join(name.split())
newString2 = "".join(name2.split())

newAlphabet =  "".join(re.findall("[a-zA-Z]+", name3.lower()))
#
# print(newString1)
# print(newString2)
print(newAlphabet)


# print(name.strip())

print(newAlphabet != newString2)