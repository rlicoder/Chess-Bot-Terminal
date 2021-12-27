import os
import json
import platform
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
from time import time
from stockfish import Stockfish
import chessUtil
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

curdir = os.getcwd()
#driverdir = curdir + '/chromedriver'
#check if the system is a mac, then use the brew package
if platform.system() == 'Darwin':
    enginedir = '/usr/local/Cellar/stockfish/14/bin/stockfish'
elif platform.system() == 'Windows':
    enginedir = curdir + '/windows_stockfish'
else:
    enginedir = curdir + '/stockfish'

stockfish = Stockfish(enginedir, parameters={"Threads": 2, "Minimum Thinking Time": 1000, "Skill Level": 20, "Min Split Depth": 10, "Hash": 256})

ops = Options()
ops.add_argument('--user-agent=nigerundayo')
ops.add_experimental_option("excludeSwitches", ["enable-automation"])
ops.add_experimental_option('useAutomationExtension', False)
ops.add_argument("--disable-blink-features=AutomationControlled")
ops.add_argument("--mute-audio")

bot = webdriver.Chrome(ChromeDriverManager().install(), options = ops)
bot.set_page_load_timeout(20)

bot.get('https://www.chess.com/home')
email = bot.find_element(By.XPATH, '//*[@id="username"]')
email.send_keys('doggydawg1234')
passw = bot.find_element(By.XPATH, '//*[@id="password"]')
passw.send_keys('pv3Q5QDbUir7R2H')
signin = bot.find_element(By.XPATH, '//*[@id="login"]')
signin.click()

#bot.get('https://www.chess.com/puzzles/rated')
#sleep(1)
#bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div[1]/button').click()
#sleep(3)
cont = input("go?")

good = 0
bad = 0
lasttime = time()
totaltime = 0
movecount = 0
redone = 0
found = False

f = open('solset.txt')
data = json.load(f)
f.close()

sols = data["puzzles"]

html = bot.page_source
while True:
    html = bot.page_source
    dir_x, dir_y = chessUtil.getDir(html)
    if (chessUtil.getTurn(html)):
        turn = 'w'
        opp = 'b'
    else:
        turn = 'b'
        opp = 'w'

    if (movecount == 0):
        FEN = chessUtil.getFen(html)
        stockfish.set_fen_position(FEN)
        startFEN = FEN
        solution = []
        puz = {}
        for x in sols:
            if (x["FEN"]) == startFEN:
                found = True
                sub = x["sol"]
    else:
        moveMade = []
        moveMade.append(chessUtil.findInBetween(FEN, chessUtil.getFen(html), opp))
        stockfish.make_moves_from_current_position(moveMade)
        FEN = stockfish.get_fen_position()

    movecount += 1
    move = stockfish.get_best_move_time(1000)
    
    print(FEN)
    print("best move: ", move)

    if (not found):
        piece, difx, dify = chessUtil.makeMove(move, bot)
        webdriver.ActionChains(bot).drag_and_drop_by_offset(piece, dify * dir_y, difx * dir_x).perform()
    
        moveMade = []
        moveMade.append(move)
        solution.append(move)
        stockfish.make_moves_from_current_position(moveMade)
        FEN = stockfish.get_fen_position()
        if (len(move) == 5):
            bot.get('https://www.chess.com/puzzles/rated')
            sleep(1)
            bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div[1]/button').click()
            sleep(3)
            movecount = 0
    else:
        redone += 1
        for move in sub:
            piece, difx, dify = chessUtil.makeMove(move, bot)
            webdriver.ActionChains(bot).drag_and_drop_by_offset(piece, dify * dir_y, difx * dir_x).perform()
            sleep(1.25)
    sleep(1.5)
    try:
        nextb = bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[5]/div[1]/div/button[3]')
        html = bot.page_source
        if (html.find('Incorrect') != -1):
            nextb = bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[5]/div[1]/div/button[4]')
            bad += 1
        else:
            puz.update({"FEN": startFEN})
            puz.update({"sol": solution})
            sols.append(puz)
            good += 1
            solset = {}
            solset.update({"puzzles": sols})
            jsonStr = json.dumps(solset, indent = 4)
            f = open('solset.txt', 'w')
            f.write(jsonStr)
            f.close()
            
        totaltime += time() - lasttime
        lasttime = time()
        nextb.click()
        print("\nPassed: ", good, "  Failed: ", bad, "Redone: ", redone)
        print("Average time per puzzle: ", totaltime / (good + bad), '\n')
        movecount = 0
        found = False
        sleep(2)
    except NoSuchElementException:
        continue
bot.quit()
