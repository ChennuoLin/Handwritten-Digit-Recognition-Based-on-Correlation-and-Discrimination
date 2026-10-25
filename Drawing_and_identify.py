import tkinter as tk
import os
from PIL import Image, ImageDraw
BASE = os.path.dirname(os.path.abspath(__file__))
CANVAS_SIZE = 280
OUTPUT_SIZE = 20
BRUSH = 20

image = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), 255)
draw = ImageDraw.Draw(image)
last_x = None
last_y = None

def paint(event):
    global last_x, last_y              
    x, y = event.x, event.y
    if last_x is not None:
        canvas.create_line(last_x, last_y, x, y,
                           width=BRUSH, fill="black",
                           capstyle=tk.ROUND, smooth=True)
        draw.line([last_x, last_y, x, y], fill=0, width=BRUSH)
        r = BRUSH // 2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=0) 
    last_x, last_y = x, y

def reset(event):
    global last_x, last_y
    last_x = None
    last_y = None


#----------------------------------------
def Convert_to_binary(O_Png, C_Png):
    with Image.open(O_Png) as img:
        O_data = img.convert("L")
    pixels = O_data.load()
    O_data_L = []
    for y in range(20):
        O_data_List = []
        for x in range(20):
            if pixels[x, y] != 255:
                O_data_List.append(1)
            else:
                O_data_List.append(-1)
        O_data_L.append(O_data_List)

    with Image.open(C_Png) as img:
        C_data = img.convert("L")
    pixels = C_data.load()
    C_data_L = []
    for y in range(20):
        C_data_List = []
        for x in range(20):
            if pixels[x, y] != 255:
                C_data_List.append(1)
            else:
                C_data_List.append(-1)
        C_data_L.append(C_data_List)

    return O_data_L, C_data_L


def Correlation(X, Y, C_ave , O_ave):
    count = 0
    sx=0
    sy=0
    for n in range(len(Y)):
        count+=(X[n]-C_ave)*(Y[n]-O_ave)
        sx+=(X[n]-C_ave)**2
        sy+=(Y[n]-O_ave)**2

    return count/((sx*sy)**0.5)

def TwoD_to_OneD(List_2):
    List = []
    for y in range(len(List_2)):
        for x in range(len(List_2)):
            List.append(List_2[y][x])
    return List

def Discrmination_Factor(RxyK):

    RxyK=sorted(RxyK, reverse=True)
    return RxyK[0]/RxyK[1]

def aveList(List):
    Black=0
    for i in range(len(List)):
        for j in range(len(List)):
            if List[i][j] == 1:
                Black+=1

    return ((Black*1)+((400-Black)*-1))/400

def Moving_Data(img,dx,dy):
    new = []
    for y in range(20):
        row = []
        for x in range(20):
            sy = y - dy         
            sx = x - dx
            if 0 <= sy < 20 and 0 <= sx < 20:
                row.append(img[sy][sx])
            else:
                row.append(-1)
        new.append(row)
    return new
    

def clear():
    canvas.delete("all")
    draw.rectangle([0, 0, CANVAS_SIZE, CANVAS_SIZE], fill=255)

def save():
    small = image.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)
    small.save(os.path.join(BASE, "drawing.png"))

    

    sumRK = []
    for i in range(1,10):
        O_data_L, C_data_L = Convert_to_binary(os.path.join(BASE, str(i) + ".png"),os.path.join(BASE, "drawing.png"))
        O_ave = aveList(O_data_L)
        O_data_L=TwoD_to_OneD(O_data_L) 
        RxyK = []
        for dx in range(-2,3):
            for dy in range(-2,3):
                new = Moving_Data(C_data_L,dx,dy)
                C_ave = aveList(C_data_L)
                RxyK.append(Correlation(TwoD_to_OneD(new), O_data_L, C_ave , O_ave))
        sumRK.append(max(RxyK))

    for i in range(len(sumRK)):
        print(f"Similarity to {i+1} is {sumRK[i]}")

    print(f"Maybe is {sumRK.index(max(sumRK))+1}")


root = tk.Tk()

canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
canvas.pack()

canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", reset)

tk.Button(root, text="Identify", command=save).pack(side="left", expand=True)
tk.Button(root, text="Clear", command=clear).pack(side="left", expand=True)

root.mainloop()
