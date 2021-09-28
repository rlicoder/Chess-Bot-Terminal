import re

def getTurnNumber(html):
    pat = re.findall('data-whole-move-number="\d*?"(?!.*data-whole-move-number)', html)
    if len(pat) == 0:
        turnnum = 0
    else:
        pat[0] = pat[0].replace('data-whole-move-number="', '')
        pat[0] = pat[0].replace('"', '')
        turnnum = int(pat[0])

    return turnnum;
