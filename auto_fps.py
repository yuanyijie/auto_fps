import math
import random
import time
import pydirectinput as direct
from ultralytics import YOLO
from pgutils import window_screen_shot_2, window_xywh
direct.PAUSE = False
model = YOLO("yolov8n.pt")
title = "你的FPS游戏标题！！"
left, top, w, h = window_xywh(title=title)
mp = (w/2, h/2)
while True:
    image = window_screen_shot_2(w, h, window_name=title)
    results = model(source=image, classes=0)
    boxes = results[0].boxes
    point = None
    distance = 999999
    for box in boxes:
        cls = box.cls.cpu().numpy().tolist()[0]
        conf = boxes.conf.cpu().numpy().tolist()[0]
        # 只处理概率在0.7以上的点
        if cls == 0 and conf >= 0.7:
            xyxy = box.xyxy.cpu().numpy().tolist()[0]
            if xyxy[3] >= 0.9 * h:
                continue
            temp_point = (xyxy[0] + (xyxy[2] - xyxy[0]) / 2, xyxy[1])
            temp_distance = math.sqrt(math.pow((temp_point[0] - mp[0]), 2) + math.pow((temp_point[1] - mp[1]), 2))
            if temp_distance < distance:
                point = temp_point
                distance = temp_distance
    # 只对距离150以内的点射击
    if point and distance <= 150:
        xOffset = int(point[0] - mp[0])
        yOffset = int(point[1] - mp[1])
        direct.moveRel(xOffset=xOffset, yOffset=yOffset, relative=True)
        direct.mouseDown()
        time.sleep(random.randint(1, 3)/100)
        direct.mouseUp()

