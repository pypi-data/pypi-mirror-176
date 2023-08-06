def IntToBin(Binary):
    newbin = bin(Binary)
    res = ""
    c=0
    for i in newbin:
        if(c != 0 and c != 1):
            if(i != "-" and i != "b"):
                res = res + i
        c+=1
    return res
def BinToInt(Bin):
    newbin = "".join(reversed(str(Bin)))
    res = 0
    mult = 1
    for i in newbin:
        res = res + int(i)*mult
        mult *= 2
    return res