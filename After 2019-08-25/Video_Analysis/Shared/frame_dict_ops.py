import Models.unique_frame_detail_dict as dict
import Models.unique_frame_detail as obj


class dict_ops:
    # constructor
    def __init__(self):
        pass

    # method
    def add_to_dict_from_figure(self, frame_position, time_stamp):
        dict.frame_dict.update({frame_position: obj.frame_detail(frame_position, False, None, True, time_stamp)})

    # method
    def add_to_dict_from_text_extract(self, frame_position, content, time_stamp):

        if dict.frame_dict.__contains__(frame_position):
            dict.frame_dict.update({frame_position: obj.frame_detail(frame_position, True, content, True, time_stamp)})
        else:
            dict.frame_dict.update({frame_position: obj.frame_detail(frame_position, True, content, False, time_stamp)})

    # method
    def view_dict(self):

        for key in dict.frame_dict:
            print(dict.frame_dict[key].frame_position, end=" ")
            print(dict.frame_dict[key].content_availability, end=" ")
            # print(dict.frame_dict[key].content, end=" ")
            print(dict.frame_dict[key].figure, end=" ")
            print(dict.frame_dict[key].timestamp)
            print("-----------------------------------------------------------")
