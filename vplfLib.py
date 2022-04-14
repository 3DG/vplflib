print("Using vplfLib v0.1 (Prototype version)")
import os
import math
optEnt = [["","","","B","C","C","","","","","C","","B","B","","","","","","","","","","","","","","B","","","","","","","","S","S","S","S""S","S","","I","","","","",""], ["","","","","C","","","","C","","","","","","C"]]
optBlk = ["","","B","B","CB","CB","B","B","B","BB","CBB","CB","CB","B","B","","B","B","CBBB","CB","B","CB","B","CB","B","CB","CB","CB","B","B","B","CBB","B","B","BB","B","B","BB","BB"]
rencalphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
def fromb64(num):
    
    returnint = 0 # set an int to return the number
    for i in range(len(num)): # for each character in the encoded number
        returnint += (rencalphabet.index(num[len(num)-i-1]))*(64**i) # calculate the number in that place in base 10 and add it to the int
    return returnint # return int

def tob64(num):
    
    returnStr = "" # set a string to return the encoded number
    for i in range((math.ceil((len(str(bin(num)))-2) / 6))): # use number to calculate how long the resulting string will be and only use within that range
        returnStr = rencalphabet[math.floor(num/(64**i))%64] + returnStr # get the encoded version of the number and add it to the string
    return returnStr # return string

def hextobits(bytestr):
    
    returnbits = "" # set string to return bits
    for byte in bytestr: # for every hex byte
        byte = bin(byte)[2:] # get binary value for byte
        if len(byte) != 8:# if the byte is less than 8 numbers long
            for x in range(8-len(byte)): # fill in with 0 until 8 numbers long
                byte = "0" + byte
        returnbits = returnbits + byte # add to resulting string
    return returnbits


def getLvl(directory):
    
    file = open(directory, "rb") # lmao get file
    return file.read() # and read
    # yes really its that simple!!!

def readFile(data):
    fileBits = hextobits(data)
    currentChar=0
    levelString = "~"
    bits = fileBits[0:6] # the first 6 bytes are always the theme
    currentChar += 6
    levelString += rencalphabet[int(bits, 2)] + "-"
    while (currentChar < math.floor(len(fileBits)/8-1)*8):
        if fileBits[currentChar] == "1": # if the object is an entity
            
            currentChar += 1 # move reader over
            bits = fileBits[currentChar] # get the enemy group bit
            if (bits == "0"):
                levelString += "AA" # enemy group 0
            else:
                levelString += "AB" # enemy group 1
            group = bits # store bit in group var for later
            currentChar += 1 # move reader over
            
            bits = fileBits[currentChar:currentChar+36] # get position
            bits = tob64(int(bits, 2)) # convert to b64
            bits = "A"*(6-len(bits))+bits # fill in if it isnt the correct length
            levelString += bits # add to code
            currentChar += 36 # move reader over
            
            bits = fileBits[currentChar:currentChar+12] # get entity id
            enemyid = int(bits, 2) # store these bits in base 10 for later
            bits = tob64(int(bits, 2)) # convert to b64
            bits = "A"*(2-len(bits))+bits # fill in if it isnt the correct length
            levelString += bits+"AAAA" # add to code
            currentChar += 12 # move reader over
            
            bits = fileBits[currentChar:currentChar+18] # get rotation
            bits = tob64(int(bits, 2)) # convert to b64
            bits = "A"*(3-len(bits))+bits # fill in if it isnt the correct length
            levelString += bits # add to code
            currentChar += 18 # move reader over
            props = optEnt[int(group)][int(enemyid)]
            for prop in props:
                if prop == "B":
                    bits = fileBits[currentChar] # get bit
                    bits = tob64(int(bits, 2)) # convert to b64
                    levelString += (bits if bits == "AB" else "AA") # add to code
                    currentChar += 1
                elif prop == "C":
                    bits = fileBits[currentChar:currentChar+36] # get color
                    bits = tob64(int(bits, 2)) # convert to b64
                    bits = "A"*(6-len(bits))+bits # fill in if it isnt the correct length
                    levelString += bits # add to code
                    currentChar += 36 # move reader over
                elif prop == "I":
                    bits = fileBits[currentChar:currentChar+12] # get int
                    bits = tob64(int(bits, 2)) # convert to b64
                    bits = "A"*(2-len(bits))+bits # fill in if it isnt the correct length
                    levelString += bits # add to code
                    currentChar += 12 # move reader over
                elif prop == "S":
                    stringy = ""
                    def getStr(bits, char):
                        stringy = ""
                        while (bits[char:char+8] != "01111111"):
                            stringy += chr(int(bits[char:char+8], 2))
                            char += 8
                        return stringy
                    stringy = getStr(fileBits, currentChar)
                    levelString += stringy
                    currentChar += (len(stringy)+1)*8
                else:
                    print(f"Possibly corrupted properties on Group {group} enemy {enemyid}")
        else: # if it is a block
            currentChar += 1 # move reader over
            bits = fileBits[currentChar:currentChar+54] # get half of everything (base 64 function is jank, i could get everything all at once if it didnt have issues)
            bits = tob64(int(bits, 2)) # convert to b64
            bits = "A"*(9-len(bits))+bits # fill it in if it isnt the correct length
            levelString += bits # add to code
            blockid = int(fileBits[currentChar:currentChar+12], 2) # store the block id for later
            currentChar += 54 # move reader over
            
            bits = fileBits[currentChar:currentChar+48] # get the other half
            bits = tob64(int(bits, 2)) # convert to b64
            bits = "A"*(8-len(bits))+bits # fill it in if it isnt the correct length
            levelString += bits # add to code
            currentChar += 48 # move reader over
            props = optBlk[blockid]
            for prop in props:
                if prop == "B":
                    bits = fileBits[currentChar] # get bit
                    levelString += ("AA" if bits == "0" else "AB") # add to code
                    currentChar += 1
                elif prop == "C":
                    bits = fileBits[currentChar:currentChar+36] # get color
                    bits = tob64(int(bits, 2)) # convert to b64
                    bits = "A"*(6-len(bits))+bits # fill in if it isnt the correct length
                    levelString += bits # add to code
                    currentChar += 36 # move reader over
                elif prop == "I":
                    bits = fileBits[currentChar:currentChar+12] # get int
                    bits = tob64(int(bits, 2)) # convert to b64
                    bits = "A"*(2-len(bits))+bits # fill in if it isnt the correct length
                    levelString += bits # add to code
                    currentChar += 12 # move reader over
                elif prop == "S":
                    stringy = ""
                    def getStr(bits, char):
                        stringy = ""
                        while (bits[char:char+8] != "01111111"):
                            stringy += chr(int(bits[char:char+8], 2))
                            char += 8
                        return stringy
                    stringy = getStr(fileBits, currentChar)
                    levelString += stringy
                    currentChar += (len(stringy)+1)*8
                else:
                    print(f"Possibly corrupted properties on Group {group} enemy {enemyid}")

        levelString += "-"

    return levelString


def compressLvl(data):
    lvl = data[1:].split("-")[:-1]
    bits = ""
    theme = str(bin(fromb64(lvl[0])))[2:]
    theme = "0"*(6-len(theme))+theme
    bits += theme
    lvl.pop(0)
    ltr=0
    for x in lvl:
        if fromb64(x[0:2]) <= 1:
            bits += "1"
            objGrp = int(fromb64(x[0:2]) == 1)
            bits += str(objGrp)
            for y in range(6):
                char = str(bin(fromb64(x[y+2])))[2:]
                char = "0"*(6-len(char))+char
                bits += char
            char = str(bin(fromb64(x[8:10])))[2:]
            char = "0"*(12-len(char))+char
            objId = int(char, 2)
            bits += char
            for y in range(3):
                char = str(bin(fromb64(x[y+14])))[2:]
                char = "0"*(6-len(char))+char
                bits += char
            ltr = 17
            for prop in optEnt[objGrp][objId]:
                if prop == "B":
                    char = fromb64(x[ltr:ltr+1])
                    bits += str(int(char == 0))
                    ltr += 1
                elif prop == "C":
                    char = str(bin(fromb64(x[ltr:ltr+6])))[2:]
                    char = "0"*(36-len(char))+char
                    bits += char
                    ltr += 6
                elif prop == "I":
                    char = str(bin(fromb64(x[ltr:ltr+2])))[2:]
                    char = "0"*(16-len(char))+char
                    bits += char
                    ltr += 2
                elif prop == "S":
                    char = x[ltr:].encode()
                    for z in char:
                        w = str(bin(z))[2:]
                        w = "0"*(8-len(w))+w
                        bits += w
                    bits += "01111111"
                else:
                    print(f"Possibly corrupted properties on Group {group} enemy {enemyid}")
        else:
            ltr = 17
            bits += "0"
            for y in range(17):
                char = str(bin(fromb64(x[y])))[2:]
                char = "0"*(6-len(char))+char
                bits += char
            blockId = fromb64(x[0:2])
            for prop in optBlk[blockId]:
                if prop == "B":
                    char = fromb64(x[ltr:ltr+1])
                    bits += str(int(char != 0))
                    ltr += 1
                elif prop == "C":
                    char = str(bin(fromb64(x[ltr:ltr+6])))[2:]
                    char = "0"*(36-len(char))+char
                    bits += char
                    ltr += 6
                elif prop == "I":
                    char = str(bin(fromb64(x[ltr:ltr+2])))[2:]
                    char = "0"*(12-len(char))+char
                    bits += char
                    ltr += 2
                elif prop == "S":
                    char = x[ltr:].encode()
                    for z in char:
                        w = str(bin(z))[2:]
                        w = "0"*(8-len(w))+w
                        bits += w
                    bits += "01111111"
                else:
                    print(f"Possibly corrupted properties on Group {group} enemy {enemyid}")
    bits += "1"*(8-(len(bits)%8)) # round bytes so it can be readable
    output = b""
    for x in range(int(len(bits)/8)): # for every byte in bits
        byte = bits[(x*8):(x*8)+8] # get byte
        char = int(byte, 2).to_bytes(1, 'little') # convert to character
        output += char # add to output
    return output

def saveFile(path, code):
    file = open(path, "wb")
    file.write(compressLvl(code))
    file.close()
