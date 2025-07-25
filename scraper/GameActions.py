import time
from consts import *
from time import sleep
from win32clipboard import OpenClipboard, GetClipboardData, CloseClipboard

class GameActions:
    def __init__(self, ui):
        self.ui = ui

    def getClipboard(self):
        for _ in range(3):
            try:
                OpenClipboard()
                data = GetClipboardData()
                CloseClipboard()

                break
            except Exception as e:
                print(f'Error accessing clipboard: {e}')
                sleep(0.5)

        return data
    
    def readRankNumber(self, index):
        return self.ui.readRectNumber(rankRect, index)
    
    def readPower(self, index):
        power = self.ui.readRectNumber(powerRect, index)

        if not power:
            raise Exception(f'Failed to read power')

        return power

    def readTitle(self):
        return self.ui.readRectText(titleRect)

    def verifyPage(self, start):
        for i in range(start, start + pageSize):
            result = self.readRankNumber(i - start)
            if result == i + 1:
                return True

        return False

    def readName(self):
        name = None
        originalClipboard = self.getClipboard()
        attempts = 0

        while not name:
            self.ui.click(nameDotsPoint)
            self.ui.click(nameCopyPoint)

            clipboard = self.getClipboard()

            if not clipboard.isnumeric() and clipboard != originalClipboard:
                name = clipboard
            else:
                print(f'Error: clipboard is {clipboard} while reading name')
                attempts += 1
                sleep(0.1 + attempts)

        return name

    def readId(self):
        id = None
        originalClipboard = self.getClipboard()
        attempts = 0

        while not id:
            self.ui.click(idCopyPoint)

            clipboard = self.getClipboard()

            if clipboard.isnumeric() and clipboard != originalClipboard:
                id = clipboard
            else:
                print(f'Error: clipboard is {clipboard} while reading ID')
                attempts += 1
                sleep(0.1 + attempts * 0.1)

        return id

    def readKingdom(self):
        return self.ui.readRectNumber(kingdomRect)

    def scrollToTop(self):
        while not self.verifyPage(0):
            self.ui.swipeDown()

    def pageDown(self):
        self.ui.swipeUp()
        sleep(0.25)

    def clickLine(self, index):
        self.ui.click(lineClickPoint, index=index)
        self.waitForTitle('Governor', timeout=5)

    def clickBack(self):
        self.ui.click(backPoint)
        self.waitForTitle('Personal', timeout=5)

    def waitForTitle(self, title, timeout=None):
        startTime = time.time()

        while (
            title.strip().lower() not in self.readTitle().strip().lower()
            and (timeout is None or (time.time() - startTime) < timeout)
        ):
            print(f'Error: waiting for title {title}')
            sleep(0.25)