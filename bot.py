import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
from stockfish import Stockfish
import parse
import util
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options


settings = open("settings.txt", "r")
thr = settings.readline()
mintime = settings.readline()
level = settings.readline()
mindep = settings.readline()
hashsize = settings.readline()
con = settings.readline()
slow = settings.readline()
timecons = settings.readline()
delayon = bool(settings.readline())
beg_delay = int(settings.readline())
mid_delay = int(settings.readline())
end_delay = int(settings.readline())
settings.close()

curdir = os.getcwd()
driverdir = curdir + '/chromedriver'
enginedir = curdir + '/stockfish'

stockfish = Stockfish(enginedir, parameters={"Threads": thr, "Minimum Thinking Time": mintime, "Skill Level": level, "Min Split Depth": mindep, "Hash": hashsize, "Contempt": con, "Slow Mover": slow})

ops = Options()
ops.add_argument('--user-agent=nigerundayo')
ops.add_experimental_option("excludeSwitches", ["enable-automation"])
ops.add_experimental_option('useAutomationExtension', False)
ops.add_argument("--disable-blink-features=AutomationControlled")
bot = webdriver.Chrome(ChromeDriverManager().install(), options=ops)
bot.set_page_load_timeout(20)

bot.get('https://www.chess.com/home')
email = bot.find_element_by_xpath('//*[@id="username"]')
email.send_keys('MiniMaxer')
passw = bot.find_element_by_xpath('//*[@id="password"]')
passw.send_keys('HPziac9W4JRiwkE')
signin = bot.find_element_by_xpath('//*[@id="login"]')
signin.click()

time = input("time control?")
cont = "New " + time + " min"

while (cont != 'q'):
    html = bot.page_source
    while (html.find(cont)) == -1:
        sleep(.5)
        html = bot.page_source
        if html.find('<text x="10" y="99" font-size="2.8" class="coordinate-dark">h</text>') != -1:
            look = "black"
        else:
            look = "white"
        loc = html.find('clock-player-turn')
        turn = html[loc-130:loc]
        while turn.find(look) == -1:
            html = bot.page_source
            if (html.find(cont)) != -1:
                break
            loc = html.find('clock-player-turn')
            turn = html[loc-130:loc]
        if html.find(cont) != -1:
            break
        html = bot.page_source
        turn_number = util.getTurnNumber(html);
        if delayon:
            if turn_number <= 10:
                offset = random.randint(0,beg_delay)
                timecons = 20
            elif turn_number >= 10 and turn_number <= 30:
                offset = random.randint(0,mid_delay)
                timecons = 400
            elif turn_number >= 31 and turn_number <=50:
                offset = random.randint(0,end_delay)
                timecons = 250
                stockfish.set_depth(7)
            else:
                offset = 0
                timecons = 50
                stockfish.set_depth(18)
            sleep(offset/1000)
        html = bot.page_source
        FEN = parse.getFen(html)
        dir_x, dir_y = parse.getDir(html)

        stockfish.set_fen_position(FEN)
        move = stockfish.get_best_move_time(timecons)
        
        print(move)
        print(stockfish.get_evaluation())

        posx = int(move[1])
        posy = int(ord(move[0]) - 96)
        search = "square-"
        search += str(posy)
        search += str(posx)
        piecel = bot.find_elements_by_class_name(search);
        if len(piecel) == 2:
            piece = piecel[1]
        else:
            piece = piecel[0]
        endx = int(move[3])
        endy = int(ord(move[2]) - 96)
        difx = endx - posx
        dify = endy - posy
        webdriver.ActionChains(bot).drag_and_drop_by_offset(piece, dify * dir_y, difx * dir_x).perform()
        html = bot.page_source
    sleep(random.randint(0,500)/1000)
    try:
        nextb = bot.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[4]/div[1]/button[2]')
    except NoSuchElementException:
        nextb = bot.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[5]/div[1]/button[2]')
    html = bot.page_source
    nextb.click()
    sleep(3)
    while (html.find('Draw') == -1):
        html = bot.page_source
        try:
            nextb.click()
            sleep(.1)
            nextb.click()
        except StaleElementReferenceException:
            break
        except StaleElementException:
            break       
        sleep(5)
bot.quit()
