import RPi.GPIO as GPIO
import cv2
import numpy as np
import time

# CONTROL CONSTANT
max_speed = 50
turn_high_speed = 75
turn_low_speed = 20
k_slope = 0.15
k_bias = 0.01
lth_small = 0.05
rth_small = 0.05
lth = 0.45
rth = 0.45
framerate = 18
cross_thred = 50
# Transform speed with theta


def trans(speed, theta):
    return int(speed*(1-0.8*theta)**0.25)

# HARDWARE STUFF DO NOT CHANGE
############################################################################
EA, I2, I1, EB, I4, I3 = (13, 19, 26, 16, 20, 21)
FREQUENCY = 100
GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.output([EA, I2, EB, I3], GPIO.LOW)
GPIO.output([I1, I4], GPIO.HIGH)
pwma = GPIO.PWM(EA, FREQUENCY)
pwmb = GPIO.PWM(EB, FREQUENCY)
pwma.start(0)
pwmb.start(0)


def set_duty(l_speed, r_speed):
    pwma.ChangeDutyCycle(r_speed)
    pwmb.ChangeDutyCycle(l_speed)
############################################################################


# CONSTANT
############################################################################
# FRAME CONSTANT
height = 120
width = 160

mid_x = int(width/2)
mid_y = int(height/2)


# IMAGE CONSTANT
gaussian_matrix_size = 3
hsv_v_max = 40
erode_dilate_kernel = np.ones((3, 3), dtype=np.uint8)
canny_threshold1 = 15
canny_threshold2 = 85
hlp_min_line_len = 5
hlp_max_line_gap = 20
hlp_min_thred = 10

############################################################################

# OPENCV CONNECTION
############################################################################
cap = cv2.VideoCapture(0)  # 获取摄像头句柄,只连接一个摄像头时参数写0即可
if not cap.isOpened():
    print("cannot DETECT camera")
    exit()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width*4)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height*4)
cap.set(cv2.CAP_PROP_FPS, framerate)


def put_text(frame: np.array, text: str):
    cv2.putText(frame, text, (mid_x, mid_y), 0, 1, 255, 2)
############################################################################

try:
    while True:
        ret, frame = cap.read()  # 读一帧
        frame = cv2.pyrDown(frame)
        frame = cv2.pyrDown(frame)
        if not ret:
            print("Getting frame error, exiting")
            exit()
        key = cv2.waitKey(1) & 0xFF  # 检测键盘,最长等待1ms (注意0表示永远而非0ms)
        if key == ord('q'):
            print("Exiting")
            break
        blurred = cv2.GaussianBlur(frame, ksize=(
            gaussian_matrix_size, gaussian_matrix_size), sigmaX=0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        thresh1 = cv2.inRange(hsv, (0, 0, 0), (255, 255, hsv_v_max))
        mask = cv2.erode(thresh1, kernel=erode_dilate_kernel, iterations=3)
        mask = cv2.dilate(mask, kernel=erode_dilate_kernel, iterations=3)
        edged = cv2.Canny(blurred, canny_threshold1, canny_threshold2)
        lines = cv2.HoughLinesP(edged, rho=1, theta=np.pi/180,
                                threshold=hlp_min_thred, minLineLength=hlp_min_line_len, maxLineGap=hlp_max_line_gap)
        if lines is None:
            put_text(frame, "No lines")
            print("Cannot detect line")
        else:
            lines = np.array(lines)
            l = np.mat(lines)
            if lines.size >= cross_thred:
                put_text(frame, "Cross"+str(l.size))
                print("Go straight")
                # set_duty(max_speed, max_speed)
            else:
                avg_line = np.average(lines, axis=0)
                x1, y1, x2, y2 = avg_line[0]
                slope = (x2-x1)/(y2-y1)
                bias = (x1+x2)/2 - mid_x
                theta = (slope*k_slope-bias*k_bias)*1.0
                print(slope*k_slope, bias*k_bias, theta)
                if(theta > lth):
                    put_text(frame, "Left")
                    print("Go left")
                    # set_duty(turn_low_speed, turn_high_speed)
                elif(theta > lth_small):
                    put_text(frame, "SLeft")
                    print("Go Sleft")
                    # set_duty(trans(max_speed,theta), max_speed)
                elif(theta < -rth):
                    put_text(frame, "Right")
                    print("Go right")
                    # set_duty(turn_high_speed, turn_low_speed)
                elif(theta < -rth_small):
                    put_text(frame, "SRight")
                    print("Go Sright")
                    # set_duty(max_speed, trans(max_speed,theta))
                else:
                    put_text(frame, "Go straight")
                    print("Go straight")
                    # set_duty(max_speed, max_speed)

                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), thickness=1)
        cv2.line(frame, (mid_x, 0), (mid_x, height), (255, 0, 0), thickness=1)
        cv2.imshow("View", frame)
except Exception as e:
    print(e)
    pass


try:
    while True:
        ret, frame = cap.read()  # 读一帧
        frame = cv2.pyrDown(frame)
        frame = cv2.pyrDown(frame)
        if not ret:
            print("Getting frame error, exiting")
            exit()
        key = cv2.waitKey(1) & 0xFF  # 检测键盘,最长等待1ms (注意0表示永远而非0ms)
        if key == ord('q'):
            print("Exiting")
            exit()
        blurred = cv2.GaussianBlur(frame, ksize=(
            gaussian_matrix_size, gaussian_matrix_size), sigmaX=0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        thresh1 = cv2.inRange(hsv, (0, 0, 0), (255, 255, hsv_v_max))
        mask = cv2.erode(thresh1, kernel=erode_dilate_kernel, iterations=3)
        mask = cv2.dilate(mask, kernel=erode_dilate_kernel, iterations=3)
        edged = cv2.Canny(blurred, canny_threshold1, canny_threshold2)
        lines = cv2.HoughLinesP(edged, rho=1, theta=np.pi/180,
                                threshold=hlp_min_thred, minLineLength=hlp_min_line_len, maxLineGap=hlp_max_line_gap)
        if lines is None:
            put_text(frame, "No lines")
            print("Cannot detect line")
        else:
            lines = np.array(lines)
            l = np.mat(lines)
            if lines.size >= cross_thred:
                put_text(frame, "Cross"+str(l.size))
                print("Go straight")
                set_duty(max_speed+4, max_speed)
            else:
                avg_line = np.average(lines, axis=0)
                x1, y1, x2, y2 = avg_line[0]
                slope = (x2-x1)/(y2-y1)
                bias = (x1+x2)/2 - mid_x
                theta = (slope*k_slope-bias*k_bias)*1.0
                print(slope*k_slope, bias*k_bias, theta)
                if(theta > lth):
                    put_text(frame, "Left")
                    print("Go left")
                    set_duty(turn_high_speed, turn_low_speed)
                elif(theta > lth_small):
                    put_text(frame, "SLeft")
                    print("Go Sleft")
                    set_duty(max_speed+4,trans(max_speed,theta) )
                elif(theta < -rth):
                    put_text(frame, "Right")
                    print("Go right")
                    set_duty(turn_low_speed, turn_high_speed)
                elif(theta < -rth_small):
                    put_text(frame, "SRight")
                    print("Go Sright")
                    set_duty(trans(max_speed,theta),max_speed )
                else:
                    put_text(frame, "Go straight")
                    print("Go straight")
                    set_duty(max_speed+4, max_speed)

                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), thickness=1)
        cv2.line(frame, (mid_x, 0), (mid_x, height), (255, 0, 0), thickness=1)
        cv2.imshow("View", frame)
except Exception as e:
    print(e)
    pass
finally:
    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 关闭所有显示窗体
    pwma.stop()
    pwmb.stop()
    GPIO.cleanup()
