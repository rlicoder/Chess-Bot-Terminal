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

stockfish = Stockfish(enginedir, parameters={"Threads": 1, "Minimum Thinking Time": 100, "Min Split Depth": 5, "Hash": 256})
stockfish.set_elo_rating(2200)

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
email.send_keys('LookingForFriends3')
passw = bot.find_element(By.XPATH, '//*[@id="password"]')
passw.send_keys('Abc12345')
signin = bot.find_element(By.XPATH, '//*[@id="login"]')
signin.click()

#bot.get('https://www.chess.com/puzzles/rated')
#sleep(1)
#bot.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div[1]/button').click()
#sleep(3)


while True:
    cont = input("go?")
    html = bot.page_source
    dir_x, dir_y = chessUtil.getDir(html)
    FEN = chessUtil.getFen(html)
    stockfish.set_fen_position(FEN)
    move = stockfish.get_best_move_time(500)
    
    piece, difx, dify = chessUtil.makeMove(move, bot)
    webdriver.ActionChains(bot).drag_and_drop_by_offset(piece, dify * dir_y, difx * dir_x).perform()
bot.quit()
