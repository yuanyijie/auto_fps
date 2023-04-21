import pyautogui
import pygetwindow
import torch
import win32con
import win32gui
import win32ui
import cv2
import numpy as np

if not torch.cuda.is_available():
    print("当前安装的torch不支持GPU，CPU推理慢，最好重新装下GPU版本")
# 获取窗口位置和宽高
def window_xywh(title):
    matchingWindows = pygetwindow.getWindowsWithTitle(title)
    if len(matchingWindows) == 0:
        raise Exception('获取窗口失败 %s ' % title)
    win = matchingWindows[0]
    return win.left, win.top, win.width, win.height

# 对指定区域截图
def window_screen_shot_1(region):
    return pyautogui.screenshot(region=region)

def window_screen_shot_2(w, h, window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
