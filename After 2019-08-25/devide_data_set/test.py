data_src = []
with open('Corpus/informal_1', 'r', encoding="utf8") as file:
    data_src = ["" + line.strip() + "" for line in file]

informal_list = []

# # for x in data_src:
print(data_src[50000])


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

x = list(divide_chunks(data_src,5000))
print(len(x))

for i in range(len(x)):
    with open(str(i)+'.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(x[i]))
    # for i in data_src:
#
#     index = i.find('>')
#     formal_list.append(i[index+1:].strip())
# print(formal_list)
#
# with open('forml.txt', mode='wt', encoding='utf-8') as myfile:
#     myfile.write('\n'.join(formal_list))
