import re

def getFen(html):
    #f = open("html.txt", "w")
    #f.write(html)
    #f.close()
    whiteturn = True
    #live game
    if html.find('clock-player-turn') != -1:
        loc = html.find('clock-player-turn')
        turn = html[loc-80:loc-47]
        if turn.find('white') != -1:
            whiteturn = True
        else:
            whiteturn = False
    #puzzle
    elif html.find('to Move') != -1:
        if (html.find('Black to Move')) != -1:
            whiteturn = False
        else:
            whiteturn = True
    #manual input when the bot is confused
    else:
        t = str(input('w or b'))
        if t == 'w':
            whiteturn = True
        else:
            whiteturn = False
        html = bot.page_source

    pieces = []
    pattern = re.compile('[bw]\D square-\d\d|square-\d\d [bw]\D')
    matches = pattern.finditer(html)
    for match in matches:
        if html[match.span()[1]+9:match.span()[1]+16] == 'opacity':
            continue;
        res = match.group();
        res = res.replace("square-", "")
        pieces.append(res)
    f = open("pieces.txt", "a")
    for piece in pieces:
        f.write(piece)
    f.write('\n')

    rows, cols = (8, 8)
    board=[]
    for i in range(cols):
        col = []
        for j in range(rows):
            col.append(' ')
        board.append(col)

    for i in range(0, len(pieces)):
        if (pieces[i].find('ihatechess')) != -1:
            continue
        if pieces[i][0].isalpha():
            y = int(pieces[i][3])
            x = int(pieces[i][4])
            p = pieces[i][1]
            if pieces[i][0] == 'w':
                p = p.upper()
        else:
            y = int(pieces[i][0])
            x = int(pieces[i][1])
            p = pieces[i][4];
            if pieces[i][3] == 'w':
                p = p.upper()
        board[x-1][y-1] = p;

    FEN = ""

    for i in range(7,-1, -1):
        count = 0
        for j in range(0,8):
            if board[i][j] == ' ':
                count += 1
            else:
                if count > 0:
                    FEN += (str(count))
                    count = 0
                FEN += (board[i][j])
        if count > 0:
            FEN += (str(count))
        FEN += ('/')

    if whiteturn == True:
        FEN += " w"
    else:
        FEN += " b"
    cast = False;
    FEN += " ";
    if board[0][7] == 'R' and board[0][4] == 'K':
        FEN += "K"
        cast = True
    if board[0][0] == 'R' and board[0][4] == 'K':
        FEN += "Q"
        cast = True
    if board[7][4] == 'k' and board[7][7] == 'r':
        FEN += "k"
        cast = True
    if board[7][0] == 'r' and board[7][4] == 'k':
        FEN += "q"
        cast = True
    if cast == False:
        FEN += " - "
    FEN += " - 0 0"
    print(FEN)
    return FEN

def getDir(html):
    widpat = re.compile('width: \d\d\dpx')
    matches = widpat.finditer(html)
    width = 0
    for i in matches:
        width = max(width, int(i.group()[-5:-2]))
    if html.find('<text x="10" y="99" font-size="2.8" class="coordinate-dark">h</text>') != -1:
        dir_x = width / 8
        dir_y = -1 * width / 8
    else:
        dir_x = -1 * width / 8
        dir_y = width / 8
    return dir_x, dir_y
