from time import sleep
from random import normalvariate, triangular
from helpers import FENload
from morehelpers import print_doc

board = FENload("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R/ w KQkq - 2 3")
temp = board.status
rowcount = 8
columns = {0:'a', 1:'b', 2: 'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

unicode_map = {'k': 0X2654, 'q':0X2655,'r':0X2656,'b':0X2657,'n':0X2658,'p':0X2659,'K':0X265A,'Q':0X265B,'R':0X265C,'B':0X265D,'N':0X265E,'P':0X265F}

print ("*" * 50)

for row in range(len(temp)):
    print (" " + chr(0x2500)*24)
    print (f"{rowcount} ", end = "")
    rowcount -= 1
    print(chr(0x2502), end = "")
    for character in temp[7-row]:
        if character == "0":
            print(chr(0x3000) + chr(0x2502), end = "")
        else:
            print(chr(unicode_map[character]) + chr(0x2502), end = "")
        print ("")
    print ("  " + chr(0x2502)*24)
    print (chr(0x25005) + chr(0x200A)*2 + "A"+chr(0x3000) + "B"+chr(0x3000) + "C"+chr(0x3000) + "D"+chr(0x3000) + "E"+chr(0x3000) + "F"+chr(0x3000) + "G"+chr(0x3000) + "H")

print_doc("Untitled1")