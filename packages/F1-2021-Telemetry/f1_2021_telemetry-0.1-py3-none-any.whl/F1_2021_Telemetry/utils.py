def bitsToList(bitsIn: bin, length = None, descending = True):
    if bitsIn is None:
        if length is None:
            return None
        return [None for _ in range(length)]

    if length is None:
        length = 1
        while 2**length <= int(bitsIn):
            length += 1

    intBits = int(bitsIn)
    returnList = []

    length -= 1

    while length >= 0:
        if intBits >= (2**length):
            intBits -= 2**length
            returnList.append(1)
        else:
            returnList.append(0)

        length -= 1

    if descending == True:
        return returnList
    else:
        return returnList[::-1]

def convToString(intList):
    if intList[0] is None:
        return None
    else:
        return "".join(chr(c) for c in intList)

def convToFloat(integer):
    if integer is None:
        return None
    else:
        return integer/32767
