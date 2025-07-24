import time
import pyodbc
import queries
import pyautogui
import traceback

from time import sleep
from GameUi import GameUi
from Ranking import Ranking
from GameActions import GameActions
from win32gui import FindWindow, GetWindowRect
from consts import *

ui = GameUi("BlueStacks App Player", headerHeight, sidebarWidth, rankHeight, swipeDownTop, swipeDownBottom, swipeUpTop, swipeUpBottom, swipeRecoil)
actions = GameActions(ui)

def getWindowRect():
    handle = FindWindow(None, "BlueStacks App Player")
    return GetWindowRect(handle)

def saveResults(rankings, type):
    sampleId = str(time.time())
    kingdoms = [int(x.kingdom) for x in rankings if x.kingdom is not None]
    kingdom = max(set(kingdoms), key=kingdoms.count)

    conn = pyodbc.connect(connenctionString)
    cursor = conn.cursor()

    for ranking in rankings:
        cursor.execute(queries.insertRanking, type, sampleId, ranking.id, ranking.name, ranking.power, ranking.rank, ranking.alliance, ranking.date, kingdom)

    conn.commit()
    cursor.close()
    conn.close()

def scrapePersonalPower():
    pyautogui.PAUSE = 0
    rankings = []

    for page in range(int(100 / (pageSize - 1) + 1)):
        while 'Personal' not in actions.readTitle():
            actions.waitForTitle('Personal', timeout=2)

            if 'Governor' in actions.readTitle():
                actions.clickBack()

        pageStart = min(page * (pageSize - 1), 100 - pageSize)
        
        while not actions.verifyPage(pageStart):
            actions.scrollToTop()
            for _ in range(page):
                actions.pageDown()

        for line in range(pageSize):
            if line + pageStart < len(rankings):
                continue

            rank = pageStart + line + 1

            powers = []
            for _ in range(3 if line in (1,2) else 1):
                try:
                    powers.append(actions.readPower(line))
                    print(f'Power attempt: {powers[-1]}')
                except Exception as e:
                    print(f'Error: {e}')

                sleep(0.5)
            
            power = max(set(powers), key=powers.count)

            actions.clickLine(line)

            while 'Governor' not in actions.readTitle():
                if 'Personal' in actions.readTitle():
                    print('Retrying clickLine due to title mismatch')
                    actions.clickLine(line)

                actions.waitForTitle('Governor', timeout=2)

            id = actions.readId()
            kingdom = actions.readKingdom()
            name = actions.readName()

            print(f'rank {rank}: {name}, ID {id}, {power} power, kingdom {kingdom}')

            ranking = Ranking(rank, name, id, power, kingdom)

            if [x for x in rankings if x.id == ranking.id]:
                print(f'Error: Duplicate ID {id} found, restarting')
                raise Exception('Duplicate ID')

            if [x for x in rankings if x.name == ranking.name]:
                print(f'Error: Duplicate name {ranking.name} found, restarting')
                raise Exception('Duplicate Name')
            
            if not power or (rankings and rankings[-1].power is not None and int(power) > int(rankings[-1].power)):
                print(f'Error: power {power} is greater than last ranking {rankings[-1].power}, value should be filled in later')
                ranking.power = None
                # raise Exception('Ranking out of order')

            rankings.append(ranking)

            sleep(0.1)

            actions.clickBack()

            while 'Personal' not in actions.readTitle():
                if 'Governor' in actions.readTitle():
                    actions.clickBack()

                actions.waitForTitle('Personal', timeout=2)
    
        actions.pageDown()
    
    print(rankings)
    saveResults(rankings, 'Personal Power')

def main():
    for _ in range(5):
        try:
            scrapePersonalPower()
            break
        except Exception as e:
            print(traceback.format_exc())
            print('Error during scraping, retrying...', e)
            sleep(2)

main()