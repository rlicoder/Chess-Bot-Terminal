import os
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

stockfish = Stockfish(enginedir, parameters={"Threads": 6, "Minimum Thinking Time": 1000, "Skill Level": 20, "Min Split Depth": 10, "Hash": 256})

ops = Options()
ops.add_argument('--user-agent=nigerundayo')
ops.add_experimental_option("excludeSwitches", ["enable-automation"])
ops.add_experimental_option('useAutomationExtension', False)
ops.add_argument("--disable-blink-features=AutomationControlled")

bot = webdriver.Chrome(ChromeDriverManager().install(), options = ops)
bot.set_page_load_timeout(20)

bot.get('https://www.chess.com/home')
email = bot.find_element(By.XPATH, '//*[@id="username"]')
email.send_keys('doggydawg1234')
passw = bot.find_element(By.XPATH, '//*[@id="password"]')
passw.send_keys('pv3Q5QDbUir7R2H')
signin = bot.find_element(By.XPATH, '//*[@id="login"]')
signin.click()

cont = input("go?")

good = 0
bad = 0
lasttime = time()
totaltime = 0

while (cont != 'q'):
    html = bot.page_source
    while True:
        html = bot.page_source
        FEN = chessUtil.getFen(html)
        dir_x, dir_y = chessUtil.getDir(html)
        if (chessUtil.getTurn(html)):
            turn = 'w'
        else:
            turn = 'b'

        stockfish.set_fen_position(FEN)
        move = stockfish.get_best_move_time(1000)
        
        #print(move)

        piece, difx, dify = chessUtil.makeMove(move, bot)
        webdriver.ActionChains(bot).drag_and_drop_by_offset(piece, dify * dir_y, difx * dir_x).perform()

        if (len(move) == 5):
            sleep(1)
            try:
                bot.get('https://www.chess.com/puzzles/rated')
                sleep(1)
                bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div[1]/button').click()
                sleep(3)
            except Exception as e:
                print(e)
                print("WAITING")
                sleep(10)
        sleep(.6)
        try:
            nextb = bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[5]/div[1]/div/button[3]')
            html = bot.page_source
            if (html.find('Incorrect') != -1):
                nextb = bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[5]/div[1]/div/button[4]')
                bad += 1
            else:
                good += 1
            totaltime += time() - lasttime
            lasttime = time()
            nextb.click()
            print("Passed: ", good, "  Failed: ", bad)
            print("Average time per puzzle: ", totaltime / (good + bad))

            sleep(1)
        except NoSuchElementException:
            continue
bot.quit()
