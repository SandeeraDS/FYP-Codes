import Models.unique_frame_detail_dict as dict
import Models.unique_frame_detail as obj


class dict_ops:

    def __init__(self):
        pass

    def add_to_dict_from_figure(self, frame_postion, time_stamp):
        dict.frame_dict.update({frame_postion:obj.frame_detail(frame_postion, False, None, True, time_stamp)})

    def add_to_dict_from_text_extract(self, frame_postion, content, time_stamp):

        if dict.frame_dict.__contains__(frame_postion):
            dict.frame_dict.update({frame_postion: obj.frame_detail(frame_postion, True, content, True, time_stamp)})
        else:
            dict.frame_dict.update({frame_postion: obj.frame_detail(frame_postion, True, content, False, time_stamp)})

    def view_dict(self):

        for key in dict.frame_dict:
            print(dict.frame_dict[key].frame_postion, end=" ")
            print(dict.frame_dict[key].content_availability, end=" ")
            # print(dict.frame_dict[key].content, end=" ")
            print(dict.frame_dict[key].figure, end=" ")
            print(dict.frame_dict[key].timestamp)
            print("-----------------------------------------------------------")
