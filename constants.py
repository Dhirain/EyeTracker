import cv2 as cv

green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)
white =(255,255,255)
font = cv.FONT_HERSHEY_PLAIN
font2 = cv.QT_FONT_NORMAL
left_eye = [36,37,38,39,40,41]
right_eye = [42,43,44,45,46,47]
blinking_ratio = 5
gaze_threshold_cutoff = 40
frame_cycle = 4

number = 'Enter number here'