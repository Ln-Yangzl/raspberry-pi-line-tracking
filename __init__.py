from controler import directionControler
from visual import visual
import cv2
import time
from tracking import tracking
from constant import *



if __name__ == '__main__':

    camera = visual(**RETICLE_SHAPE)
    track = tracking(**RETICLE_SHAPE, **LOSS_KWARGS)
    direction = directionControler(**DIRECTION_KWARGS)

    while True:
        line = input("请输入指令: ")
        if line == 'q':
            break
        elif line == 'i':

            while True:
                pic, reticlePic = camera.getGrayPic()
                loss = track.computeLoss(pic)
                cv2.imshow("display", reticlePic)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('x'):
                    track.updateVerticalSum(pic)
                if key == ord('q'):
                    break

        elif line == 'r':
            # 启动小车
            direction.update(0)
            try:
                while True:
                    pic, reticlePic = camera.getGrayPic()
                    loss = track.computeLoss(pic)
                    direction.update(loss)
                    cv2.imshow("display", reticlePic)
                    cv2.waitKey(100)
                    # time.sleep(0.1)
            
            except KeyboardInterrupt:
                pass
            


    # pic = camera.getGrayPic()
    # print(len(pic))
    # print(len(pic[0]))
    # print('get pic from camera:')
    # print(pic)
    # cv2.imshow("display", pic)  # 显示
    # cv2.waitKey(0)
    # print(track.computeLoss(pic))

    