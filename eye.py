import geometry
import constants as _constant
import cv2 as cv
import numpy as np
from scipy.spatial import distance as dist


def get_blinking_ratio(points, landmarks, frame):
    left_point = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
    right_point = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
    center_top = geometry.midpoint(landmarks.part(points[1]), landmarks.part(points[2]))
    center_bottom = geometry.midpoint(landmarks.part(points[4]), landmarks.part(points[5]))

    cv.drawMarker(frame, geometry.midpoint(landmarks.part(points[0]),landmarks.part(points[3])), _constant.green, cv.MARKER_CROSS, 2, 3)
    # horizontal_line = cv.line(frame, left_point, right_point, _constant.green, 2)
    # vertical_line = cv.line(frame, center_top, center_bottom, _constant.green, 2)

    horizontal_dis = geometry.distance_btw_points(left_point, right_point)
    vertical_dis = geometry.distance_btw_points(center_top, center_bottom)

    ratio = horizontal_dis / vertical_dis

    return ratio


def get_gaze_ratio(points, landmarks, frame, gray):
    eye_region = get_eye_region(points, landmarks)

    # mask
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)

    # eye mask
    cv.polylines(mask, [eye_region], True, _constant.white, 2)
    cv.fillPoly(mask, [eye_region], _constant.white)
    eye_mask = cv. bitwise_and(gray, gray, mask=mask)

    # show eye
    eye_frame = min_max_frame(eye_region, frame)
    # eye_frame = cv.resize(eye_frame, None, fx=5, fy=5)

    # threshod binary of eye
    gray_eye = min_max_frame(eye_region, eye_mask)
    _, threshold_eye = cv.threshold(gray_eye, 63, 255, cv.THRESH_BINARY)
    name = "Left"
    if points == _constant.left_eye:
        name = "Right"
    cv.imshow(name, threshold_eye)

    # gazing eye
    height, width = threshold_eye.shape
    first_half_threshold = threshold_eye[0:height, 0: int(width / 2)]
    first_half_white = cv.countNonZero(first_half_threshold)
    second_half_threshold = threshold_eye[0:height, int(width / 2):]
    second_half_white = cv.countNonZero(second_half_threshold)
    try:
        gaze_ratio = first_half_white / second_half_white
        # print(gaze_ratio)

    except ZeroDivisionError:
        return None
    return gaze_ratio


def get_eye_region(points, landmarks):
    return np.array([(landmarks.part(points[0]).x, landmarks.part(points[0]).y),
                     (landmarks.part(points[1]).x, landmarks.part(points[1]).y),
                     (landmarks.part(points[2]).x, landmarks.part(points[2]).y),
                     (landmarks.part(points[3]).x, landmarks.part(points[3]).y),
                     (landmarks.part(points[4]).x, landmarks.part(points[4]).y),
                     (landmarks.part(points[5]).x, landmarks.part(points[5]).y)], np.int32)


def min_max_frame(region, frame):
    min_x = np.min(region[:, 0])
    max_x = np.max(region[:, 0])
    min_y = np.min(region[:, 1])
    max_y = np.max(region[:, 1])
    # print(min_x, max_x, min_y, max_y)
    return frame[min_y: max_y, min_x: max_x]

# def min_max_points(region):
#     min_x = np.min(region[:, 0])
#     max_x = np.max(region[:, 0])
#     min_y = np.min(region[:, 1])
#     max_y = np.max(region[:, 1])
#     return (min_x,max_x,min_y,max_y)
