# Wire size calculation from
# http://www.solar-wind.co.uk/cable-sizing-DC-cables.html

AWGSize = [0] * 32
AWGTitle = [""] * 32

AWGSize[0] = 0
AWGSize[1] = 0.13
AWGSize[2] = 0.16
AWGSize[3] = 0.2
AWGSize[4] = 0.26
AWGSize[5] = 0.33
AWGSize[6] = 0.41
AWGSize[7] = 0.52
AWGSize[8] = 0.65
AWGSize[9] = 0.82
AWGSize[10] = 1.04
AWGSize[11] = 1.31
AWGSize[12] = 1.65
AWGSize[13] = 2.08
AWGSize[14] = 2.63
AWGSize[15] = 3.31
AWGSize[16] = 4.17
AWGSize[17] = 5.26
AWGSize[18] = 6.63
AWGSize[19] = 8.36
AWGSize[20] = 10.55
AWGSize[21] = 13.29
AWGSize[22] = 16.76
AWGSize[23] = 21.14
AWGSize[24] = 26.65
AWGSize[25] = 33.61
AWGSize[26] = 42.39
AWGSize[27] = 53.46
AWGSize[28] = 67.4
AWGSize[29] = 84.97
AWGSize[30] = 107.16
AWGSize[31] = -1

AWGTitle[0] = "Too small"
AWGTitle[1] = "26 AWG"
AWGTitle[2] = "25 AWG"
AWGTitle[3] = "24 AWG"
AWGTitle[4] = "23 AWG"
AWGTitle[5] = "22 AWG"
AWGTitle[6] = "21 AWG"
AWGTitle[7] = "20 AWG"
AWGTitle[8] = "19 AWG"
AWGTitle[9] = "18 AWG"
AWGTitle[10] = "17 AWG"
AWGTitle[11] = "16 AWG"
AWGTitle[12] = "15 AWG"
AWGTitle[13] = "14 AWG"
AWGTitle[14] = "13 AWG"
AWGTitle[15] = "12 AWG"
AWGTitle[16] = "11 AWG"
AWGTitle[17] = "10 AWG"
AWGTitle[18] = "9 AWG"
AWGTitle[19] = "8 AWG"
AWGTitle[20] = "7 AWG"
AWGTitle[21] = "6 AWG"
AWGTitle[22] = "5 AWG"
AWGTitle[23] = "4 AWG"
AWGTitle[24] = "3 AWG"
AWGTitle[25] = "2 AWG"
AWGTitle[26] = "1 AWG"
AWGTitle[27] = "0 AWG"
AWGTitle[28] = "00 AWG"
AWGTitle[29] = "000 AWG"
AWGTitle[30] = "0000 AWG"
AWGTitle[31] = "Too large"

def CalculateWireSize(voltage, current, length, loss=5):
    result = round(((length * current * 0.04) / ((voltage * loss) / 100)) * 100) / 100
    index = 0
    found = False
    while not found and AWGSize[index] != -1:
        if result == AWGSize[index]:
            found = True
        else:
            if AWGSize[index + 1] != -1:
                if result > AWGSize[index] and result < AWGSize[index + 1]:
                    found = True
            index += 1
    return AWGTitle[index]

def CalculateWireSize1(voltage, current, length, loss=5):
    result = (length * current * 0.04) / ((voltage * loss) / 100.0)
    for i in range(len(AWGSize) - 1):
        if AWGSize[i] < result < AWGSize[i + 1]:
            return AWGTitle[i]
    return AWGTitle[-1]
