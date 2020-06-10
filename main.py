import cv2 as cv
import dlib
import constants as _constant
import sms
import eye
import morseCode

cap = cv.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
message = ''
currentframe = 0
currentChar = ''
previousChar = ''
is_message_final = False

def show_message(text):
    cv.putText(frame, text, (20, 30), cv.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 1)

def show_eye_status(text):
    # cv.putText(frame, text, (20, 30), cv.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 1)
    cv.putText(frame, text, (20, 60), cv.FONT_HERSHEY_DUPLEX, 0.6, (147, 58, 31), 1)


while True:
    _, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        gaze = 0
        landmarks = predictor(gray, face)

        # brinking events
        left_blink_ratio = eye.get_blinking_ratio(_constant.left_eye, landmarks, frame)
        right_blink_ratio = eye.get_blinking_ratio(_constant.right_eye, landmarks, frame)
        both_eye = (left_blink_ratio + right_blink_ratio) / 2
        # print(both_eye)
        if (both_eye > _constant.blinking_ratio):
            show_eye_status('Blinking')
            currentChar = '/'

        else:
        # # gazing events
            left_gaze_ratio = eye.get_gaze_ratio(_constant.left_eye, landmarks, frame, gray)
            right_gaze_ratio = eye.get_gaze_ratio(_constant.right_eye, landmarks, frame, gray)
            if left_gaze_ratio != None and right_gaze_ratio != None:
                average_age_ratio = (left_gaze_ratio + right_gaze_ratio) / 2
                gaze = average_age_ratio
                print(gaze)
                if gaze < .6:
                    show_eye_status('Seeing Left')
                    currentChar = '-'
                elif gaze > 2:
                    show_eye_status('Seeing Right')
                    currentChar = '.'
                else:
                    show_eye_status('Seeing Center')
                    currentChar = ''

        if (currentChar != previousChar) and not is_message_final:
            print(str(gaze)+ currentChar)
            message = message + currentChar
            if message.endswith('////'):
                is_message_final = True
                message = morseCode.get_real_text(message)
                sms.SMSSender(_constant.number, message)
            previousChar = currentChar
            print(message)
            show_message(message)

        elif is_message_final:
            "to convert message"
            show_message("SMS send: "+message)
            print(morseCode.get_real_text(message))
        else:
            show_message(message)
    cv.imshow("Frame", frame)

    key = cv.waitKey(2)
    if key == 27: #escape key
        break
print("messge: ", message)
print(morseCode.get_real_text(message))
cap.release()
cv.destroyAllWindows()