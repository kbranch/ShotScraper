import re
import pyautogui

from time import sleep
from screen_ocr import Reader
from Rectangle import Rectangle
from win32gui import FindWindow, GetWindowRect

class GameUi:
    ocr = Reader.create_reader(backend='easyocr')

    def __init__(self, windowName, headerHeight, sidebarWidth, listItemHeight, swipeDownTop, swipeDownBottom, swipeUpTop, swipeUpBottom, swipeRecoil):
        self.windowName = windowName
        self.headerHeight = headerHeight
        self.sidebarWidth = sidebarWidth
        self.listItemHeight = listItemHeight
        self.swipeDownTop = swipeDownTop
        self.swipeDownBottom = swipeDownBottom
        self.swipeUpTop = swipeUpTop
        self.swipeUpBottom = swipeUpBottom
        self.swipeRecoil = swipeRecoil
    
    def emulatorWindowRect(self):
        handle = FindWindow(None, self.windowName)
        return GetWindowRect(handle)
    
    def gameRect(self):
        rect = self.emulatorWindowRect()
        return Rectangle(rect[0], rect[1] + self.headerHeight, rect[2] - self.sidebarWidth, rect[3])

    def percentToPixels(self, point, addWindow=True):
        rect = self.gameRect()
        x = (rect.left if addWindow else 0) + (rect.width * point[0])
        y = (rect.top if addWindow else 0) + (rect.height * point[1])
        return (int(x), int(y))

    def windowCoords(self, point):
        return self.percentToPixels(point)
    
    def gameWindowRect(self, target):
        topLeft = self.percentToPixels((target.left, target.top))
        bottomRight = self.percentToPixels((target.right, target.bottom))
        return (
            topLeft[0],
            topLeft[1],
            bottomRight[0],
            bottomRight[1],
        )
    
    def addListIndexRect(self, rect, index):
        rect = Rectangle.fromObj(rect)

        height = self.percentToPixels((0, self.listItemHeight), addWindow=False)[1]
        rect.top += index * height
        rect.bottom += index * height

        return rect
    
    def addListIndexPoint(self, point, index):
        height = self.percentToPixels((0, self.listItemHeight), addWindow=False)[1]

        return (
            point[0],
            point[1] + index * height
        )
    
    def readRectText(self, target, index=0):
        target = Rectangle.fromObj(target)
        rect = self.gameWindowRect(target)
        rect = self.addListIndexRect(rect, index)

        results = GameUi.ocr.read_screen(bounding_box=rect.toTuple())
        words = [
            word
            for line in results.result.lines
            for word in line.words
        ]

        words.sort(key=lambda x: x.left)

        return ''.join([x.text for x in words])
    
    def readRectNumber(self, target, index=0):
        text = self.readRectText(target, index)
        number = re.sub('\D', '', text)
        return int(number) if number else None
    
    def click(self, point, delay=0.15, index=0):
        point = self.percentToPixels(point)
        point = self.addListIndexPoint(point, index)

        pyautogui.moveTo(point[0], point[1])
        pyautogui.click()
        sleep(delay)
    
    def swipeDown(self):
        top = self.percentToPixels(self.swipeDownTop)
        bottom = self.percentToPixels(self.swipeDownBottom)
        pyautogui.moveTo(top[0], top[1])
        pyautogui.mouseDown()
        pyautogui.moveTo(bottom[0], bottom[1], 0.25)
        pyautogui.mouseUp()
        sleep(1)
    
    def swipeUp(self):
        top = self.percentToPixels(self.swipeUpTop)
        bottom = self.percentToPixels(self.swipeUpBottom)
        recoil = self.percentToPixels(self.swipeRecoil)
        pyautogui.moveTo(bottom[0], bottom[1])
        pyautogui.mouseDown()
        pyautogui.moveTo(top[0], top[1], 4)
        pyautogui.moveTo(recoil[0], recoil[1], 0.25)
        # pyautogui.moveRel(0, 5, 0.25)
        pyautogui.mouseUp()

        # sleep(0.75)