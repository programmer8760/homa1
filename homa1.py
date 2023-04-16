import sys
sys.path.append('/lib')
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from turtle import *
import turtle
from math import *
from PIL import ImageGrab
from sympy import *

def triangleSOSelected(event): #при изменении способа задания треугольника
    selection = triangleSOCombobox.get()
    if selection == "2 стороны, 1 угол":
        triangleLabel1['text'] = "Сторона"
        triangleLabel2['text'] = "Угол"
        triangleLabel3['text'] = "Сторона"
    elif selection == "1 сторона, 2 угла":
        triangleLabel1['text'] = "Угол"
        triangleLabel2['text'] = "Сторона"
        triangleLabel3['text'] = "Угол"
    elif selection == "3 стороны":
        triangleLabel1['text'] = "Сторона"
        triangleLabel2['text'] = "Сторона"
        triangleLabel3['text'] = "Сторона"

def on_closing(): #при закрытии главного окна
    root.destroy()
    turtleRoot.destroy()
    
def on_tur_closing(): #при закрытии окна turtle
    if messagebox.askyesno("➡️", "Сохранить?"):
        save_as_png(turtleRoot, turtle.getcanvas())
    turtleRoot.withdraw()
    
def save_as_png(turRoot, widget): #сохранения холста turtle в png
    fileName = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", ".png")])
    turRoot.attributes('-topmost',True)
    turRoot.attributes('-fullscreen',True)
    turRoot.update()
    sleep(0.25)
    x=turRoot.winfo_rootx()+widget.winfo_x()
    y=turRoot.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save(fileName)
    turRoot.attributes('-topmost',False)
    turRoot.attributes('-fullscreen',False)
    turRoot.update()

#черепаха
tur = turtle.Turtle()
tur.hideturtle()
tur.width(3)
turtleRoot = turtle.getcanvas().winfo_toplevel()
turtleRoot.withdraw()
turtleRoot.protocol("WM_DELETE_WINDOW", on_tur_closing)

def generate(): #генерация треугольника
    tur.clear()
    triangleSetVar = triangleSOCombobox.get()
    input1 = triangleEntry1.get()
    input2 = triangleEntry2.get()
    input3 = triangleEntry3.get()
    if len(input1) != 0 and len(input2) != 0 and len(input3) != 0:
        SPtriangle = None
        if triangleSetVar == "2 стороны, 1 угол":
            SPtriangle = Triangle(sas=(int(input1), int(input2), int(input3)))
        elif triangleSetVar == "1 сторона, 2 угла":
            SPtriangle = Triangle(asa=(int(input1), int(input2), int(input3)))
        elif triangleSetVar == "3 стороны":
            SPtriangle = Triangle(sss=(int(input1), int(input2), int(input3)))
    else:
        print("введи")
        return
    nameVar = nameEntry.get()
    if len(nameVar) == 0: nameVar = "ABC"
    
    SPsides = []
    sideLengths = []
    for i in range(0, 3): SPsides.append(Segment(N(SPtriangle.vertices[i]), N(SPtriangle.vertices[i-2])))
    for side in SPsides: sideLengths.append(N(side.length))

    turtleRoot.deiconify()
    tur.penup()
    tur.setpos(-300, -300)
    tur.setheading(0)
    tur.pendown()
    
    showNames = showNamesVar.get()
    progressBar.step()
    root.update()
    for i in range(0, 3): #сама фигура
        if showNames: tur.write(nameVar[i], move=False, align="center", font=("Times New Roman", 20, "normal"))
        if i == 2:
            tur.setpos(-300, -300)
        else:
            tur.setpos(N(SPtriangle.vertices[i+1][0])*50-300, N(SPtriangle.vertices[i+1][1])*50-300)
    progressBar.step()
    if inCircleVar.get(): #вписанная окружность
        tur.penup()
        tur.setpos(N(SPtriangle.incenter[0])*50-300, N(SPtriangle.incenter[1])*50-300)
        tur.pendown()
        tur.dot()
        if showNames: tur.write("I", move=False, align="center", font=("Times New Roman", 10, "normal"))
        tur.penup()
        tur.setpos(N(SPtriangle.incenter[0])*50-300, -300)
        tur.pendown()
        tur.circle(N(SPtriangle.inradius)*50)
    progressBar.step()
    if circumCircleVar.get():#описанная окружность
        tur.penup()
        tur.setpos(N(SPtriangle.circumcenter[0])*50-300, N(SPtriangle.circumcenter[1])*50-300)
        tur.pendown()
        tur.dot()
        if showNames: tur.write("O", move=False, align="center", font=("Times New Roman", 10, "normal"))
        tur.penup()
        tur.setpos(N(SPtriangle.circumcenter[0])*50-300, (N(SPtriangle.circumcenter[1])-N(SPtriangle.circumradius))*50-300)
        tur.pendown()
        tur.circle(N(SPtriangle.circumradius)*50)
    progressBar.step()
    #медианы
    mediansTD = []
    if median1Var.get(): mediansTD.append(0)
    if median2Var.get(): mediansTD.append(1)
    if median3Var.get(): mediansTD.append(2)
    for i in range(0, 3): 
        if len(mediansTD) == 0:
            progressBar.step(3)
            break
        if i in mediansTD:
            tur.penup()
            tur.setpos(N(SPtriangle.vertices[i-1][0])*50-300, N(SPtriangle.vertices[i-1][1])*50-300)
            tur.pendown()
            tur.setpos(N(SPtriangle.medians[SPtriangle.vertices[i-1]].points[1][0])*50-300, N(SPtriangle.medians[SPtriangle.vertices[i-1]].points[1][1])*50-300)
            if showNames:
                tur.write("M", move=False, align="center", font=("Times New Roman", 20, "normal"))
                tur.penup()
                tur.forward(15)
                tur.write(str(i+1), move=False, align="center", font=("Times New Roman", 14, "normal"))
        progressBar.step()
    #биссектрисы
    bisectorsTD = []
    if bisector1Var.get(): bisectorsTD.append(0)
    if bisector2Var.get(): bisectorsTD.append(1)
    if bisector3Var.get(): bisectorsTD.append(2)
    for i in range(0, 3):
        if len(bisectorsTD) == 0: 
            progressBar.step(3)
            break
        if i in bisectorsTD:
            ang = degrees(N(SPtriangle.angles[SPtriangle.vertices[i]]))/2
            l = 1/(sideLengths[i]+sideLengths[i-1])*sqrt(sideLengths[i]*sideLengths[i-1]*sum(sideLengths)*(sum(sideLengths)-sideLengths[i-2]*2))
            tur.penup()
            tur.setpos(N(SPtriangle.vertices[i][0])*50-300, N(SPtriangle.vertices[i][1])*50-300)
            tur.setheading(ang) if i == 0 else tur.setheading(180-ang) if i == 1 else tur.setheading(-ang-degrees(N(SPtriangle.angles[SPtriangle.vertices[1]])))
            tur.pendown()
            tur.forward(l*50)
            #tur.setpos(N(SPtriangle.bisectors()[SPtriangle.vertices[i]].points[1][0])*50-300, N(SPtriangle.bisectors()[SPtriangle.vertices[i]].points[1][1])*50-300)
            if showNames:
                tur.write("L", move=False, align="center", font=("Times New Roman", 20, "normal"))
                tur.penup()
                tur.forward(15)
                tur.write(str(i+1), move=False, align="center", font=("Times New Roman", 14, "normal"))
        progressBar.step()
    #высоты
    altitudesTD = []
    if altitude1Var.get(): altitudesTD.append(0)
    if altitude2Var.get(): altitudesTD.append(1)
    if altitude3Var.get(): altitudesTD.append(2)
    for i in range(0, 3):
        if len(altitudesTD) == 0: 
            progressBar.step(3)
            break
        if i in altitudesTD:
            ang = 90 - degrees(N(SPtriangle.angles[SPtriangle.vertices[i]])) if i != 2 else 90 - degrees(N(SPtriangle.angles[SPtriangle.vertices[0]]))
            p = sum(sideLengths)/2
            h = 2/sideLengths[i]*sqrt(p*(p-sideLengths[i])*(p-sideLengths[i-1])*(p-sideLengths[i-2]))
            tur.penup()
            tur.setpos(N(SPtriangle.vertices[i-1][0])*50-300, N(SPtriangle.vertices[i-1][1])*50-300)
            tur.setheading(ang) if i == 1 else tur.setheading(180-ang) if i == 2 else tur.setheading(-90)
            tur.pendown()
            tur.forward(h*50)
            #tur.setpos(N(SPtriangle.altitudes[SPtriangle.vertices[i-1]].points[1][0])*50-300, N(SPtriangle.altitudes[SPtriangle.vertices[i-1]].points[1][1])*50-300)
            if showNames:
                tur.write("H", move=False, align="center", font=("Times New Roman", 20, "normal"))
                tur.penup()
                tur.forward(15)
                tur.write(str(i+1), move=False, align="center", font=("Times New Roman", 14, "normal"))
        progressBar.step()
    #серединные перпендикуляры
    PBsTD = []
    if PB1Var.get(): PBsTD.append(0)
    if PB2Var.get(): PBsTD.append(1)
    if PB3Var.get(): PBsTD.append(2)
    for i in range(0, 3):
        if len(PBsTD) == 0: 
            progressBar.step(3)
            break
        if i in PBsTD:
            sideToPB = SPsides[i]
            sidePBing = SPsides[i-1] if sideToPB.angle_between(SPsides[i-1]) > sideToPB.angle_between(SPsides[i-2]) else SPsides[i-2]
            pb = sideToPB.perpendicular_bisector()
            pb = Segment(pb.points[0], intersection(pb, sidePBing)[0])
            
            tur.penup()
            tur.setpos(N(pb.points[0][0])*50-300, N(pb.points[0][1])*50-300)
            if showNames:
                tur.write("P", move=False, align="center", font=("Times New Roman", 20, "normal"))
                tur.penup()
                tur.forward(15)
                tur.write(str(i+1), move=False, align="center", font=("Times New Roman", 14, "normal"))
                tur.backward(15)
            tur.pendown()
            tur.setpos(N(pb.points[1][0])*50-300, N(pb.points[1][1])*50-300)
        progressBar.step()

#основное окно
root = Tk()
root.title("homa1")
root.geometry("600x350")
root.protocol("WM_DELETE_WINDOW", on_closing)

#-----треугольник гуи------
#обозначение
nameLabel = ttk.Label(root, text="Обозначение").grid(row=1, column=0)
nameEntry = ttk.Entry(root, width=6)
nameEntry.grid(row=2, column=0)
nameEntry.insert(0, "ABC")

#комбобокс для выбора способа задания треугольника
triangleSetOptions = ["2 стороны, 1 угол", "1 сторона, 2 угла", "3 стороны"]
triangleSOLabel = ttk.Label(root, text="Способ задания").grid(row=5, column=0)
triangleSOCombobox = ttk.Combobox(root, values=triangleSetOptions, state="readonly")
triangleSOCombobox.current(0)
triangleSOCombobox.grid(row=6, column=0)
triangleSOCombobox.bind("<<ComboboxSelected>>", triangleSOSelected)

#Поля ввода для треугольника
triangleEntry1 = ttk.Entry(root, width=6) 
triangleEntry2 = ttk.Entry(root, width=6)
triangleEntry3 = ttk.Entry(root, width=6)
triangleLabel1 = ttk.Label(root, text="Сторона")
triangleLabel2 = ttk.Label(root, text="Угол")
triangleLabel3 = ttk.Label(root, text="Сторона")
triangleLabel1.grid(row=7, column=0)
triangleEntry1.grid(row=8, column=0)
triangleLabel2.grid(row=9, column=0)
triangleEntry2.grid(row=10, column=0)
triangleLabel3.grid(row=11, column=0)
triangleEntry3.grid(row=12, column=0)

#вписанная окружность галочка
inCircleVar = BooleanVar(root)
inCircleCheB = ttk.Checkbutton(root, text="Вписать окружность", variable=inCircleVar) 
inCircleCheB.grid(row=8, column=1)

#описанная окружность галочка
circumCircleVar = BooleanVar(root)
circumCircleCheB = ttk.Checkbutton(root, text="Описать окружность", variable=circumCircleVar) 
circumCircleCheB.grid(row=10, column=1)

#медианы
median1Var = BooleanVar(root)
median1CheB = ttk.Checkbutton(root, text="Медиана 1", variable=median1Var) 
median1CheB.grid(row=2, column=1)
median2Var = BooleanVar(root)
median2CheB = ttk.Checkbutton(root, text="Медиана 2", variable=median2Var) 
median2CheB.grid(row=4, column=1)
median3Var = BooleanVar(root)
median3CheB = ttk.Checkbutton(root, text="Медиана 3", variable=median3Var) 
median3CheB.grid(row=6, column=1)

#биссектрисы
bisector1Var = BooleanVar(root)
bisector1CheB = ttk.Checkbutton(root, text="Биссектриса 1", variable=bisector1Var) 
bisector1CheB.grid(row=2, column=2)
bisector2Var = BooleanVar(root)
bisector2CheB = ttk.Checkbutton(root, text="Биссектриса 2", variable=bisector2Var) 
bisector2CheB.grid(row=4, column=2)
bisector3Var = BooleanVar(root)
bisector3CheB = ttk.Checkbutton(root, text="Биссектриса 3", variable=bisector3Var) 
bisector3CheB.grid(row=6, column=2)

#высоты
altitude1Var = BooleanVar(root)
altitude1CheB = ttk.Checkbutton(root, text="Высота 1", variable=altitude1Var) 
altitude1CheB.grid(row=2, column=3)
altitude2Var = BooleanVar(root)
altitude2CheB = ttk.Checkbutton(root, text="Высота 2", variable=altitude2Var) 
altitude2CheB.grid(row=4, column=3)
altitude3Var = BooleanVar(root)
altitude3CheB = ttk.Checkbutton(root, text="Высота 3", variable=altitude3Var) 
altitude3CheB.grid(row=6, column=3)

#серединные перпендикуляры
PB1Var = BooleanVar(root)
PB1CheB = ttk.Checkbutton(root, text="Серед. перпендикуляр 1", variable=PB1Var) 
PB1CheB.grid(row=8, column=2)
PB2Var = BooleanVar(root)
PB2CheB = ttk.Checkbutton(root, text="Серед. перпендикуляр 2", variable=PB2Var) 
PB2CheB.grid(row=10, column=2)
PB3Var = BooleanVar(root)
PB3CheB = ttk.Checkbutton(root, text="Серед. перпендикуляр 3", variable=PB3Var) 
PB3CheB.grid(row=8, column=3)

#Кнопка
generateButton = ttk.Button(root, text="Нарисовать", command=generate).grid(row=12, column=2) 

#галочка подписать точки
showNamesVar = BooleanVar(root, value=True)
showNamesCheB = ttk.Checkbutton(root, text="Подписывать точки", variable=showNamesVar) 
showNamesCheB.grid(row=12, column=3)

#загрузка
progressBar = ttk.Progressbar(orient="horizontal", length=900, value=0, maximum=16)
progressBar.pack()

root.mainloop()