from controler import directionControler
from visual import visual
import cv2
# from tracking import tracking
from houghTracking import houghTracking as tracking
from constant import *

if __name__ == '__main__':

    camera = visual(**RETICLE_SHAPE)
    track = tracking(**HOUGH_KWARGS)
    direction = directionControler(**DIRECTION_KWARGS)

    while True:
        print('q -- exit, i -- aim line r -- start run')
        line = input("Please Enter Order: ")
        if line == 'q':
            break
        elif line == 'i':

            while True:
                pic = camera.getGrayPic()
                loss, line = track.computeLoss(pic)
                cv2.line(pic, line[0], line[1], (0,255,0),1)
                cv2.imshow("display", pic)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    break

        elif line == 'r':
            # 启动小车
            direction.update(0,isStop=False, isRun=True)
            try:
                while True:
                    pic = camera.getGrayPic()
                    loss, line = track.computeLoss(pic, '')
                    direction.update(loss)
                    cv2.line(pic, line[0], line[1], (0,255,0),1)
                    cv2.imshow("display", pic)
                    key= cv2.waitKey(100) & 0xFF
                    if key == ord('q'):
                        direction.update(0, isStop=True)
                        break
                    # time.sleep(0.1)
            
            except KeyboardInterrupt:
                pass
            cv2.destroyAllWindows()
            print('Stopped !!')
        # GPIO.cleanup()


# if __name__ == '__main__':

#     camera = visual(**RETICLE_SHAPE)
#     track = tracking(**RETICLE_SHAPE, **LOSS_KWARGS)
#     direction = directionControler(**DIRECTION_KWARGS)

#     while True:
#         print('q -- exit, i -- update the vertical sum, r -- start run')
#         line = input("Please Enter Order: ")
#         if line == 'q':
#             break
#         elif line == 'i':

#             while True:
#                 pic, reticlePic = camera.getGrayPic()
#                 loss = track.computeLoss(pic)
#                 cv2.imshow("display", reticlePic)
#                 key = cv2.waitKey(1) & 0xFF
#                 if key == ord('x'):
#                     track.updateVerticalSum(pic)
#                 if key == ord('q'):
#                     cv2.destroyAllWindows()
#                     break

#         elif line == 'r':
#             # 启动小车
#             direction.update(0,isStop=False, isRun=True)
#             try:
#                 while True:
#                     pic, reticlePic = camera.getGrayPic()
#                     loss = track.computeLoss(pic, '')
#                     direction.update(loss)
#                     cv2.imshow("display", reticlePic)
#                     key= cv2.waitKey(100) & 0xFF
#                     if key == ord('q'):
#                         direction.update(0, isStop=True)
#                         break
#                     # time.sleep(0.1)
            
#             except KeyboardInterrupt:
#                 pass
#             cv2.destroyAllWindows()
#             print('Stopped !!')
#         # GPIO.cleanup()
            


    # pic = camera.getGrayPic()
    # print(len(pic))
    # print(len(pic[0]))
    # print('get pic from camera:')
    # print(pic)
    # cv2.imshow("display", pic)  # 显示
    # cv2.waitKey(0)
    # print(track.computeLoss(pic))

    