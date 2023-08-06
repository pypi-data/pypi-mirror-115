import json
import cv2
import csv
import time
import numpy as np
import sys
import math
import argparse


# This function is to change frame count to time in millisecond
def frame_count_to_time(frame_count_input, frame_rate_input):
    return (frame_count_input / frame_rate_input) * 1000


# This function is to read string to convert boolean value
def str_to_bool(input_bool_string):
    if str(input_bool_string).lower().strip() == "true":
        return True
    else:
        return False


# This function is to display the process progressing
def print_percent_done(index_input, total, bar_len=50, title_input='Please wait'):
    percent_done = (index_input + 1) / total * 100
    percent_done_round = round(percent_done, 1)

    done = int(round(percent_done_round / (100 / bar_len)))
    togo = bar_len - done

    done_str = '█' * done
    togo_str = '░' * togo

    sys.stdout.write(f'\r{title_input}: [{done_str}{togo_str}] {percent_done_round}% done')


# This function is to change color string to color tuple value
def change_string_to_color_tuple(input_string):
    if "(" in input_string and ")" in input_string:
        color_value_array = input_string.replace("(", "").replace(")", "").split(",")
        output_color_tuple = tuple(float(index) for index in color_value_array)
        return output_color_tuple
    elif input_string.lower() == "red":
        output_color_tuple = (0, 0, 250)
        return output_color_tuple
    elif input_string.lower() == "green":
        output_color_tuple = (0, 250, 0)
        return output_color_tuple
    elif input_string.lower() == "blue":
        output_color_tuple = (250, 0, 0)
        return output_color_tuple
    elif input_string.lower() == "yellow":
        output_color_tuple = (0, 250, 250)
        return output_color_tuple
    elif input_string.lower() == "black":
        output_color_tuple = (0, 0, 0)
        return output_color_tuple
    elif input_string.lower() == "white":
        output_color_tuple = (250, 250, 250)
        return output_color_tuple
    elif input_string.lower() == "magenta":
        output_color_tuple = (250, 0, 250)
        return output_color_tuple
    elif "#" in input_string.lower():
        value = input_string.lstrip('#')
        lv = len(value)
        if lv == 6:
            try:
                tem_arr = tuple(int(value[xx:xx + lv // 3], 16) for xx in range(0, lv, lv // 3))
                return tem_arr[::-1]
            except ValueError as e:
                print(e)
                raise
        else:
            print(f"The length of input hex string must be 6 character. But it is {lv}.")
            raise
    else:
        print(f"Input string {input_string} is not a valid color string input.")
        print("It can be red, green, blue, black, white or magenta.")
        print("It also can be hex color code.")
        pass


# This function is to get the positions in parent axes array
def get_position_of_parent(search_string_input, axes_array_input):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(axes_array_input):
        if val["name"] == search_string_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_string_input} can not be found!")

    return return_idx


# This function is to get the positions in given array
def get_position(search_input, array_in):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(array_in):
        if val == search_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_input} can not be found!")

    return return_idx


# This function is to get index value from horizontal to vertical labelling
def get_vertical_position(frame_width_input, frame_height_input, put_text_input,
                          x_input, y_input, color_search_input, font_input, thick_input):
    # width = height and height = width when we rotate the image
    f_w = frame_height_input
    f_h = frame_width_input
    tem_image = np.zeros([int(f_w), int(f_h), 3], dtype=np.uint8)
    x_edit = int(frame_height_input - y_input)
    y_edit = x_input
    co_ord_input = (x_edit, y_edit)
    cv2.putText(tem_image, put_text_input, co_ord_input, cv2.FONT_HERSHEY_SIMPLEX, font_input,
                color_search_input, thick_input)
    out_image = cv2.rotate(tem_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    color_index_output = np.where(np.all(out_image == color_search_input, axis=-1))

    return color_index_output


# This function is to get the color index in given image
def get_color_position(image_input, color_in):
    color_index_output = np.where(np.all(image_input == color_in, axis=-1))

    return color_index_output


# This function is to create the data array in order to draw lines in graph
def get_data_array(csv_data_input, t_data_input, y_data_input,
                   filter_input=False, filter_by_input=None):
    if filter_input:
        filter_name, filter_value = str(filter_by_input).split("=")
        filter_value = int(filter_value)
        data_array_output = []
        row_count = 0
        with open(csv_data_input, "r") as csv_file:
            csv_reader = (csv.reader(csv_file, delimiter=','))
            header_array = next(csv_reader)
            t_pos = get_position(t_data_input, header_array)
            y_pos = get_position(y_data_input, header_array)
            f_pos = get_position(filter_name, header_array)

            for row in csv_reader:
                if row_count == 0:
                    row_count += 1
                    pass
                else:
                    filter_check = int(row[f_pos])
                    if filter_check == filter_value:
                        time_value = float(row[t_pos]) * 1000
                        y_value = float(row[y_pos])
                        data_array_output.append([time_value, y_value])

        return data_array_output
    else:
        data_array_output = []
        row_count = 0
        with open(csv_data_input, "r") as csv_file:
            csv_reader = (csv.reader(csv_file, delimiter=','))
            header_array = next(csv_reader)
            t_pos = get_position(t_data_input, header_array)
            y_pos = get_position(y_data_input, header_array)

            for row in csv_reader:
                if row_count == 0:
                    row_count += 1
                    pass
                elif row_count == 1:
                    time_value = float(row[t_pos]) * 1000
                    y_value = float(row[y_pos])
                    data_array_output.append([time_value, y_value])

        return data_array_output


# This function is to change the given number to scaled value
def number_to_scale(lower_limit_input, upper_limit_input, box_height_input, number_input):
    total_limit = upper_limit_input - lower_limit_input
    number_in_total = number_input - lower_limit_input
    number_output = int(box_height_input * (number_in_total / total_limit))

    return number_output


# This function is to check whether there must be zero line or not
def need_to_display_zero_line(low_limit, up_limit):
    if low_limit < 0 < up_limit:
        return True
    else:
        return False


# This function is to produce average value from array
def get_value_from_array(data_arr_input, low_li, up_li):
    new_arr = data_arr_input[:]
    length_array = len(new_arr)
    if length_array == 1:
        val = new_arr[0]
        return val
    elif length_array == 0:
        val = [((low_li + up_li) / 2), "nothing"]
        return val
    else:
        avg_time = sum(new_arr[0]) / len(new_arr[0])
        avg_value = sum(new_arr[1]) / len(new_arr[1])
        val = [avg_time, avg_value]
        return val


def main():
    parser = argparse.ArgumentParser(prog='vinset',
                                     description='VINSET package.')
    parser.add_argument('--version', action='version', version='2.0.4'),
    parser.add_argument("-i", dest="input_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="input mp4 file", metavar="filename.mp4")
    parser.add_argument("-o", dest="output_filename", required=True, type=argparse.FileType('w'), default=sys.stdout,
                        help="output mp4 file", metavar="filename.mp4")
    parser.add_argument("-c", dest="config_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="config json file", metavar="filename.json")

    args = parser.parse_args()
    input_file = args.input_filename.name
    output_file = args.output_filename.name
    config_file = args.config_filename.name

    if str(input_file).endswith(".mp4"):
        print("Input file name:", input_file)
    else:
        print("Input file must be mp4.")
    if str(output_file).endswith(".mp4"):
        print("Output file name:", output_file)
    else:
        print("Output file must be mp4.")
    if str(config_file).endswith(".json"):
        print("Config file name:", config_file)
    else:
        print("Config file must be json.")

    data = None
    draw_able = True
    try:
        f = open(config_file)
        data = json.load(f)
        print(f"{config_file} is loaded successfully by json.")
    except ValueError:
        draw_able = False
        print(f"{config_file} cannot be loaded by json.")

    if draw_able and data:
        axes_array = data["axes"]
        series_array = data["series"]
        csv_data = data["csv_data"]
        display_able = str_to_bool(str(data["display"]))

        input_video = cv2.VideoCapture(input_file)
        frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("Frame width:", frame_width)
        frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Frame height:", frame_height)
        frame_rate = input_video.get(cv2.CAP_PROP_FPS)
        print("Frame rate:", frame_rate)
        frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Frame count:", frame_count)

        draw_data_array = []
        max_video_length = math.ceil(frame_count_to_time(frame_count, frame_rate))

        for info in series_array:
            search_string = info["parent_axes"]
            parent_index = get_position_of_parent(search_string, axes_array)
            if parent_index is not None:
                axes_info = axes_array[parent_index]
                axes_pos = axes_info["position"]
                # axes_pos_x = axes_pos["x"]
                # axes_pos_y = axes_pos["y"]
                axes_pos_w = axes_pos["width"]
                # axes_pos_h = axes_pos["height"]
                series_name = info["name"]
                display_type = info["display_type"]
                t_limit = info["t-limit"]
                t_w = t_limit["width"]
                t_data = info["t_data"]
                y_data = info["y_data"]
                info_filter = str_to_bool(str(info["filter"]))
                filter_by = None
                if info_filter:
                    filter_by = info["filterBy"]
                if str(display_type).lower() == "pen":
                    if info_filter:
                        data_arr = get_data_array(csv_data, t_data, y_data, info_filter, filter_by)
                    else:
                        data_arr = get_data_array(csv_data, t_data, y_data)
                    series_data_array = []
                    time_interval_for_data = round(1000 / (axes_pos_w / t_w), 2)
                    number_of_time_interval = math.ceil(max_video_length / time_interval_for_data)
                    lower_range = 0
                    upper_range = round((lower_range + time_interval_for_data), 2)
                    for i in range(1, (number_of_time_interval + 1), 1):
                        raw_data_array = []
                        # input_data = None
                        for data in data_arr:
                            if lower_range <= data[0] < upper_range:
                                raw_data_array.append(data)
                        input_data = get_value_from_array(raw_data_array, lower_range, upper_range)
                        raw_data_array.clear()
                        series_data_array.append([upper_range, input_data])
                        lower_range = upper_range
                        upper_range = round((upper_range + time_interval_for_data), 2)
                    draw_data_array.append([series_name, display_type, series_data_array])

                elif str(display_type).lower() == "refresh":
                    if info_filter:
                        data_arr = get_data_array(csv_data, t_data, y_data, info_filter, filter_by)
                    else:
                        data_arr = get_data_array(csv_data, t_data, y_data)
                    series_data_array = []
                    time_interval_for_data = round(1000 / (axes_pos_w / t_w), 4)
                    number_of_time_interval = math.ceil(max_video_length / time_interval_for_data)
                    lower_range = 0
                    upper_range = round((lower_range + time_interval_for_data), 2)
                    width_check = int(t_w) * 1000
                    box_data_array = []
                    for i in range(1, (number_of_time_interval + 1), 1):
                        raw_data_array = []
                        # input_data = None
                        for data in data_arr:
                            if lower_range <= data[0] < upper_range:
                                raw_data_array.append(data)
                        input_data = get_value_from_array(raw_data_array, lower_range, upper_range)
                        box_data_array.append(input_data)
                        if max_video_length <= width_check:
                            if i == (number_of_time_interval - 1):
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                        else:
                            if upper_range >= width_check:
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                                box_data_array.clear()
                                width_check += (int(t_w) * 1000)
                        lower_range = upper_range
                        upper_range = round((upper_range + time_interval_for_data), 2)
                    draw_data_array.append([series_name, display_type, series_data_array])

        ret, frame = input_video.read()
        raw_image = None
        if ret:
            raw_image = frame
            raw_image.fill(0)
        box_color_array = []
        line_color_array = []

        for info in series_array:
            search_string = info["parent_axes"]
            parent_index = get_position_of_parent(search_string, axes_array)
            if parent_index is not None:
                axes_info = axes_array[parent_index]
                box_color = change_string_to_color_tuple(axes_info["box_color"])
                box_color_array.append(box_color)
                axes_pos = axes_info["position"]
                box_title = axes_info["box_title"]
                title_font = float(axes_info["box_title_font_scale"])
                box_thickness = int(axes_info["box_thickness"])
                axes_pos_x = axes_pos["x"]
                axes_pos_y = axes_pos["y"]
                axes_pos_w = axes_pos["width"]
                axes_pos_h = axes_pos["height"]
                t_limit = info["t-limit"]
                t_w = t_limit["width"]
                t_name = info["t_label"]
                y_name = info["y_label"]
                label_thickness = int(info["label_thickness"])
                label_font_scale = float(info["label_font_scale"])
                line_color = info["line_color"]
                line_color_array.append(change_string_to_color_tuple(line_color))
                raw_image = cv2.rectangle(raw_image, (axes_pos_x, axes_pos_y),
                                          ((axes_pos_x + axes_pos_w), (axes_pos_y + axes_pos_h)),
                                          box_color, box_thickness)
                offset_value = 30
                box_title_length = len(box_title)
                title_x = int(axes_pos_x) + int(axes_pos_w / 2) - (5 * box_title_length)
                title_y = int(axes_pos_y) - int(offset_value / 2)
                cv2.putText(raw_image, box_title, (title_x, title_y), cv2.FONT_HERSHEY_SIMPLEX, title_font,
                            box_color, box_thickness)
                t_name_length = len(t_name)
                t_label_x = int(axes_pos_x) + int(axes_pos_w / 2) - (5 * t_name_length)
                t_label_y = int(axes_pos_y) + int(axes_pos_h) + offset_value
                cv2.putText(raw_image, t_name, (t_label_x, t_label_y), cv2.FONT_HERSHEY_SIMPLEX, label_font_scale,
                            box_color, label_thickness)
                y_name_length = len(y_name)
                y_label_x_input = axes_pos_x - offset_value + 10
                y_label_y_input = axes_pos_y - (int(axes_pos_h / 2) + offset_value) + (1 * y_name_length)
                ver_color_index_array = get_vertical_position(frame_width, frame_height, y_name,
                                                              y_label_x_input, y_label_y_input,
                                                              box_color, label_font_scale, label_thickness)
                for item in zip(ver_color_index_array[0], ver_color_index_array[1]):
                    item_tuple = tuple(item)
                    raw_image[item_tuple[0], item_tuple[1]] = box_color

                x_scale_interval_width = int(axes_pos_w / t_w)
                # start_point_x_scale = axes_pos_x
                # x_scale_level = axes_pos_y + axes_pos_h
                height_of_scale = 5

                for i in range(0, t_w):
                    space_value = i * x_scale_interval_width
                    # end_point_x_scale_level = start_point_x_scale - height_of_scale
                    cv2.line(raw_image, (axes_pos_x + space_value,
                                         axes_pos_h + axes_pos_y),
                             (axes_pos_x + space_value,
                              axes_pos_h + axes_pos_y - height_of_scale),
                             box_color, box_thickness)

        draw_index_arr = []
        for color in box_color_array:
            draw_index = get_color_position(raw_image, color)
            draw_index_arr.append(draw_index)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        v_writer = cv2.VideoWriter(output_file, fourcc, int(frame_rate), (int(frame_width), int(frame_height)))
        whole_t = time.time()
        count = 0

        while True:

            # start_tt = time.time()
            ret, frame = input_video.read()
            # end_tt = time.time()
            print_percent_done(count, frame_count)
            check_timer = frame_count_to_time(count, frame_rate)

            if ret:
                for info in series_array:
                    search_string = info["parent_axes"]
                    parent_index = get_position_of_parent(search_string, axes_array)
                    if parent_index is not None:
                        axes_info = axes_array[parent_index]
                        axes_pos = axes_info["position"]
                        x = axes_pos["x"]
                        y = axes_pos["y"]
                        w = axes_pos["width"]
                        h = axes_pos["height"]
                        axes_bg = axes_info["background"]
                        bg_fill = axes_bg["fill"]
                        color_input = change_string_to_color_tuple(bg_fill)
                        bg_opacity = axes_bg["opacity"]
                        overlay_frame = frame.copy()
                        boundary_space = 50
                        cv2.rectangle(overlay_frame,
                                      (x - boundary_space, y - boundary_space),
                                      (x + w + boundary_space,
                                       y + h + boundary_space),
                                      color_input, -1)
                        frame = cv2.addWeighted(overlay_frame, bg_opacity,
                                                frame, 1 - bg_opacity, 0)
                for i, d_index in enumerate(draw_index_arr):
                    for item in zip(d_index[0], d_index[1]):
                        item_tuple = tuple(item)
                        frame[item_tuple[0], item_tuple[1]] = box_color_array[i]

                clone_frame = np.copy(frame)

                for i, info in enumerate(series_array):
                    display_arr = draw_data_array[i][2]
                    # info_name = info["name"]
                    search_str = info["parent_axes"]
                    pointer_info = info["pointer_value"]
                    need_to_draw_pointer = bool(pointer_info["Enabled"])
                    line_thickness = int(info["line_thickness"])
                    zero_display = str_to_bool(str(info["zero_line_display"]))
                    zero_line_thick = 0
                    if zero_display:
                        zero_line_thick = int(info["zero_line_thickness"])
                    show_type = str(info["display_type"])
                    info_y_limit = info["y-limit"]
                    info_limits = info_y_limit["limits"]
                    lower_limit = int(info_limits["lower"])
                    upper_limit = int(info_limits["upper"])
                    zero_display = need_to_display_zero_line(lower_limit, upper_limit)
                    info_t_limit = info["t-limit"]
                    t_width = info_t_limit["width"]
                    pointer_color = None
                    pointer_radius = None
                    if need_to_draw_pointer:
                        pointer_color = change_string_to_color_tuple(pointer_info["Color"])
                        pointer_radius = pointer_info["Radius"]
                    parent_index = get_position_of_parent(search_str, axes_array)
                    axes_info = axes_array[parent_index]
                    if show_type == "pen" and parent_index is not None:
                        pass
                        # ax_pos = axes_info["position"]
                        # ax_x = ax_pos["x"]
                        # ax_y = ax_pos["y"]
                        # ax_w = ax_pos["width"]
                        # ax_h = ax_pos["height"]
                        # zero_line_start_x = ax_x
                        # zero_line_y_scale = int(number_to_scale(lower_limit, upper_limit, ax_h, 0))
                        # zero_line_y = int(ax_y + ax_h - zero_line_y_scale)
                        # zero_line_end_x = ax_x + ax_w
                        # time_in_pixel_value = round((t_width / ax_w), 2)
                        # start_x = ax_x
                        # start_y = ax_y + int(ax_h / 2)
                        # # first_step = 0
                        # value_to_draw = False
                        # step = 1
                        # end_x = 0
                        # end_y = 0
                        # len_array = len(display_arr)
                        # if len_array > 0:
                        # for ind, number in enumerate(display_arr):
                        #     if zero_display:
                        #         cv2.line(clone_frame, (zero_line_start_x, zero_line_y),
                        #                  (zero_line_end_x, zero_line_y),
                        #                  line_color_array[i], zero_line_thick)
                        #     if math.isnan(number[1]):
                        #         start_x = 0
                        #         start_y = 0
                        #         value_to_draw = False
                        #         pass
                        #     else:
                        #         if not value_to_draw:
                        #             scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, number[1])
                        #             scaled_step = int(number[0] / time_in_pixel_value)
                        #             start_x = ax_x + scaled_step
                        #             start_y = int(ax_y + ax_h - scaled_num)
                        #             value_to_draw = True
                        #         else:
                        #             scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, number[1])
                        #             scaled_step = int(number[0] / time_in_pixel_value)
                        #             end_x = ax_x + scaled_step
                        #             end_y = int(ax_y + ax_h - scaled_num)
                        #             cv2.line(clone_frame, (start_x, start_y), (end_x, end_y),
                        #                      line_color_array[i], line_thickness, cv2.LINE_AA)
                        #             if need_to_draw_pointer and ind == len_array - 1:
                        #                 cv2.circle(clone_frame, (end_x, end_y), pointer_radius, pointer_color, -1)
                        #             start_x = end_x
                        #             start_y = end_y

                    elif show_type == "refresh" and parent_index is not None:
                        ax_pos = axes_info["position"]
                        ax_x = ax_pos["x"]
                        ax_y = ax_pos["y"]
                        ax_w = ax_pos["width"]
                        ax_h = ax_pos["height"]
                        zero_line_start_x = ax_x
                        zero_line_y_scale = int(number_to_scale(lower_limit, upper_limit, ax_h, 0))
                        zero_line_y = int(ax_y + ax_h - zero_line_y_scale)
                        zero_line_end_x = ax_x + ax_w
                        time_in_pixel_value = round((t_width / ax_w), 4)
                        # time_interval_for_data = round(1 / (ax_w / t_width), 4)
                        start_x = ax_x
                        start_y = 0
                        value_to_draw = False
                        display_count = int(check_timer / (t_width * 1000))
                        total_display_count = int(max_video_length / (t_width * 1000))
                        # end_x = 0
                        # end_y = 0
                        final_display_arr = display_arr[display_count][1]

                        if len(final_display_arr) > 0:
                            for ind, num in enumerate(final_display_arr):
                                if zero_display:
                                    cv2.line(clone_frame, (zero_line_start_x, zero_line_y),
                                             (zero_line_end_x, zero_line_y),
                                             line_color_array[i], zero_line_thick)
                                if type(num[1]) == str:
                                    pass

                                elif math.isnan(num[1]):
                                    value_to_draw = False

                                else:
                                    if not value_to_draw:
                                        scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                        scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                        start_x = ax_x + scaled_step - (display_count * ax_w)
                                        start_y = int(ax_y + ax_h - scaled_num)
                                        value_to_draw = True
                                    else:
                                        scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                        scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                        if display_count != total_display_count and ind == (len(final_display_arr) - 1):
                                            end_x = ax_x + ax_w
                                        else:
                                            end_x = ax_x + scaled_step - (display_count * ax_w)
                                        end_y = int(ax_y + ax_h - scaled_num)
                                        cv2.line(clone_frame, (start_x, start_y), (end_x, end_y),
                                                 line_color_array[i], line_thickness, cv2.LINE_AA)
                                        if need_to_draw_pointer and round(num[0], 2) == round(check_timer, 2):
                                            cv2.circle(clone_frame,
                                                       (end_x, end_y), pointer_radius, pointer_color, -1)
                                        start_x = end_x
                                        start_y = end_y

                for info in series_array:
                    search_string = info["parent_axes"]
                    parent_index = get_position_of_parent(search_string, axes_array)
                    if parent_index is not None:
                        axes_info = axes_array[parent_index]
                        axes_pos = axes_info["position"]
                        x = axes_pos["x"]
                        y = axes_pos["y"]
                        w = axes_pos["width"]
                        h = axes_pos["height"]
                        cropped_image = clone_frame[y:(y + h), x:(x + w)]
                        frame[y:(y + h), x:(x + w)] = cropped_image

                if display_able:
                    cv2.imshow("Frame", frame)
                    # cv2.imshow("F", clone_frame)
                # vsr_t = time.time()
                v_writer.write(frame)
                # vso_t = time.time()
                count += 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                end_whole_t = time.time()
                print("\r")
                print(f"The whole process took {round((end_whole_t - whole_t), 4)} seconds.")
                print(f"{output_file} is successfully produced.")
                print("Thank you for using VINSET")
                break

        input_video.release()
        v_writer.release()
        cv2.destroyAllWindows()
