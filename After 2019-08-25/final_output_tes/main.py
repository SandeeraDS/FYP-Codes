import frame_details

frame_dict = {}
print(bool(frame_dict))

frame_dict = {"main Topic": [1, 2, 3, 4], "subtopic": [1, 2, 3, 4]}
print(bool(frame_dict))
print(len(frame_dict))
frame_dict.update({"subtopic_2": [5, 6, 7, 8]})


value = frame_dict["subtopic_2"]
value.append(56)
print(value)

print(list(frame_dict.keys())[-1])


# a = 'testing this is working. testing this is working 1.'
# b = 'testing this is working. testing this is working 1. testing this is working 2'
#
#
# # splitA = set(a.split("."))
# # splitB = set(b.split("."))
# #
# # diff = splitB.difference(splitA)
# # diff = ", ".join(diff)
# # print(diff)

