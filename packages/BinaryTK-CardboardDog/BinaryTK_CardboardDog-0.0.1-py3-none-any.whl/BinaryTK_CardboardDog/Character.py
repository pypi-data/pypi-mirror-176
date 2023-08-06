import BinaryTK.Integer as binPAR
key = "       	                           ! #$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
def BinToChar(Dat):
    newdat = key[binPAR.BinToInt(str(Dat))]
    return newdat
def CharToBin(Char):
    ii = 1
    num = 0
    for i in key:
        if(i == Char):
            num = ii
        ii+=1
    return binPAR.IntToBin(num)