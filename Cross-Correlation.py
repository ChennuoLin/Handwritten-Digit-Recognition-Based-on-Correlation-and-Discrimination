from PIL import Image

def Convert_to_binary(O_Png, C_Png):
    O_data = Image.open(O_Png).convert("L")                 
    pixels = O_data.load()
    O_data_L = []
    for y in range(10): 
        for x in range(10):
            if pixels[x, y]!=255:
                O_data_L.append(1)
            else:
                O_data_L.append(-1)

    C_data = Image.open(C_Png).convert("L")                 
    pixels = C_data.load()
    C_data_L = []
    for y in range(10): 
        for x in range(10):
            if pixels[x, y]!=255:
                C_data_L.append(1)
            else:
                C_data_L.append(-1)

    return O_data_L, C_data_L


def Cross_Correlation(X, Y):
    Rxyk = []
    for k in range(len(Y)):
        count = 0
        for n in range(len(Y)):
            count+=X[n]*Y[n]

        Rxyk.append(count)
        Y.pop(0)
    return Rxyk

def Discrmination_Factor(RxyK):

    D=RxyK[0]/max([abs(i) for i in RxyK[1:-1]])

    return D

for i in range(1,10):
    O_data_L,C_data_L = Convert_to_binary(str(i)+".png","drawing.png")
    print(f"{i} is {Discrmination_Factor(Cross_Correlation(O_data_L,C_data_L))}")






