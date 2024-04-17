from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math as mat
import time

class TrCanvas(tk.Canvas):

    def create_rectangle(self, x1: int, y1: int, x2: int, y2: int, **kwargs):
        if "alpha" in kwargs:
            alpha = int(kwargs.pop("alpha") * 255)
            if "fill" in kwargs:
                fill = kwargs.pop("fill")
            else:
                fill = "white"
            fill = self.master.winfo_rgb(fill) + (alpha,)
            image = Image.new("RGBA", (x2 - x1, y2 - y1), fill)
            image = ImageTk.PhotoImage(image)
            self.create_image(x1, y1, image=image, anchor="nw")
        tk.Canvas.create_rectangle(self, x1, y1, x2, y2, **kwargs)
        return image

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget
#
#
# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#
#     w = QWidget()
#     w.resize(250, 150)
#     w.move(300, 300)
#     w.setWindowTitle('Simple')
#     w.show()
#
#     sys.exit(app.exec_())


debuger = False
prev_x = None
prev_y = None
A = None
B = None
direction = None
coord: list = []
last_coor: list = []
col_p = None
zamk = False

def debug():
    global debuger
    if debuger:
        debuger = False
    else:
        debuger = True


def draw():
    global debuger
    if debuger:
        pic.set(+1)

#Линии 1-го порядка
def cda(event):
    global prev_x, prev_y, debuger
    x = event.x
    y = event.y
    if prev_x:
        tx = prev_x - x
        ty = prev_y - y
        leng = max(abs(tx), abs(ty))
        dy = ty/leng
        dx = tx/leng

        dot_x = 0
        dot_y = 0

        if dx < 0:
            dot_x = x + 0.5*(-1)
        elif dx == 0:
            dot_x = x
        elif dx > 0:
            dot_x = x + 0.5

        if dy < 0:
            dot_y = y + 0.5 * (-1)
        elif dy == 0:
            dot_y = y
        elif dy > 0:
            dot_y = y + 0.5
        i = 0
        dot_y1 = None
        dot_x1 = None
        while i <= leng:
            if debuger:
                dot_x1 = dot_x + dx
                dot_y1 = dot_y + dy
                canvas.wait_variable(pic)
                image = canvas.create_rectangle(round(dot_x)+5, round(dot_y1)+5, round(dot_x)+10, round(dot_y1)+10,
                                                width=5, fill='black', outline='black', alpha=1.0)
                i += 5
            else:
                dot_x1 = dot_x + dx
                dot_y1 = dot_y + dy
                image = canvas.create_rectangle(round(dot_x), round(dot_y1), round(dot_x), round(dot_y1),
                                                width=1, fill='black', outline='black', alpha=1.0)
                i += 1
            dot_x = dot_x1
            dot_y = dot_y1
        prev_x = None
        prev_y = None
    else:
        prev_x = x
        prev_y = y


def sign(a):
    if a < 0:
        return -1
    else:
        return 1


def brez(event):
    global prev_x, prev_y, debuger
    x = event.x
    y = event.y
    bug = 0
    if prev_x:
        dx = x - prev_x
        dy = y - prev_y
        if abs(dx) >= abs(dy):
            main = prev_x
            sec = prev_y
            main_d = dx
            sec_d = dy
        else:
            main = prev_y
            sec = prev_x
            main_d = dy
            sec_d = dx
        e = abs(2*sec_d)-abs(main_d)
        # if debuger:
        #     canvas.wait_variable(pic)
        #     image = canvas.create_rectangle(x, y, x+5, y+5, width=0.5, fill='black', outline='black', alpha=1.0)
        # else:
        #     image = canvas.create_rectangle(x,y,x,y, width=0.5, fill='black', outline='black', alpha=1.0)
        i = 0
        while i < abs(main_d):
            if e >= 0:
                sec += 1*sign(sec_d)
                e -= abs(2*main_d)
            main += 1*sign(main_d)
            e += abs(2*sec_d)
            i += 1
            if debuger:
                canvas.wait_variable(pic)
                if abs(dx) >= abs(dy):
                    image = canvas.create_rectangle(main, sec, main+5, sec+5, width=1, fill='black',
                                                    outline='black', alpha=1.0)
                else:
                    image = canvas.create_rectangle(sec, main, sec+5, main+5, width=1, fill='black',
                                                    outline='black', alpha=1.0)
            else:
                if abs(dx) >= abs(dy):
                    image = canvas.create_rectangle(main, sec, main, sec, width=1, fill='black',
                                                    outline='black', alpha=1.0)
                else:
                    image = canvas.create_rectangle(sec, main, sec, main, width=1, fill='black',
                                                    outline='black', alpha=1.0)
        prev_x = None
        prev_y = None
        x = None
        y = None
    else:
        prev_x = x
        prev_y = y


def vu(event):
    global prev_x, prev_y, debuger
    x = event.x
    y = event.y
    if prev_x:
        dx = x - prev_x
        dy = y - prev_y
        if abs(dx) >= abs(dy):
            main = prev_x
            sec = prev_y
            main_d = dx
            sec_d = dy
        else:
            main = prev_y
            sec = prev_x
            main_d = dy
            sec_d = dx
        e = abs(2 * sec_d) - abs(main_d)
        # if debuger:
        #     canvas.wait_variable(pic)
        #     image = canvas.create_rectangle(x, y+5, x, y+5, width=0.5, fill='black', outline='black', alpha=1.0)
        # else:
        #     image = canvas.create_rectangle(x,y,x,y, width=0.5, fill='black', outline='black', alpha=1.0)
        i = 0
        itery = 0
        while i < abs(main_d):
            if e >= 0:
                sec += 1 * sign(sec_d)
                e -= abs(2 * main_d)
            main += 1 * sign(main_d)
            e += abs(2 * sec_d)
            i += 1
            if abs(dx) >= abs(dy):
                grad = dy / dx
                xgap = 1 - ((prev_x + 0.5) % 1)
                yend = prev_y + grad * (round(prev_x) - prev_x)
                if itery == 0:
                    itery = yend + grad
                alp = 1-itery%1
                if debuger:
                    canvas.wait_variable(pic)
                    image = canvas.create_rectangle(main, sec, main+5, sec+5, width=0.1, fill='black', outline='black',
                                                    alpha=1.0)
                    image1 = canvas.create_rectangle(main, sec + 1, main+5, sec + 6, width=0.1, fill='black',
                                                     outline='black', alpha=alp)
                else:
                    image = canvas.create_rectangle(main, sec, main+5, sec+5, width=0.1, fill='black', outline='black',
                                                    alpha=1.0)
                    image1 = canvas.create_rectangle(main, sec + 1, main+5, sec + 6, width=0.1, fill='black',
                                                     outline='black', alpha=alp)
                itery += grad
            else:
                grad = dx / dy
                xgap = 1 - ((prev_y + 0.5) % 1)
                yend = prev_x + grad * (round(prev_y) - prev_y)
                if itery == 0:
                    itery = yend + grad
                alp = 1 - itery%1
                if debuger:
                    canvas.wait_variable(pic)
                    image = canvas.create_rectangle(sec, main, sec+5, main+5, width=0.1, fill='black', outline='black',
                                                    alpha=1.0)
                    image1 = canvas.create_rectangle(sec + 1, main, sec + 6, main+5, width=0.1, fill='black',
                                                     outline='black', alpha=alp)
                else:
                    image = canvas.create_rectangle(sec, main, sec+5, main+5, width=0.1, fill='black', outline='black',
                                                    alpha=1.0)
                    image1 = canvas.create_rectangle(sec + 1, main, sec + 6, main+5, width=0.1, fill='black',
                                                     outline='black', alpha=alp)
                itery += grad
        prev_x = None
        prev_y = None
        x = None
        y = None
    else:
        prev_x = x
        prev_y = y


def selected(event):
    selection = combobox1.get()
    if selection == 'ЦДА':
        canvas.unbind('<1>')
        canvas.bind('<1>', cda)
    elif selection == 'Брезенхем':
        canvas.unbind('<1>')
        canvas.bind('<1>', brez)
    elif selection == 'Ву':
        canvas.unbind('<1>')
        canvas.bind('<1>', vu)
    else:
        canvas.unbind('<1>')

#Линии 2-го порядка
def mirr (x, y, c_x, c_y):
    global debuger
    m_x = c_x - x - 1
    m_y = c_y - y - 1
    if debuger:
        canvas.wait_variable(pic)
        canvas.create_rectangle(m_x, c_y + y, m_x+5, c_y + y+5, fill='black', outline='black', alpha=1.0)
        canvas.create_rectangle(c_x + x, m_y, c_x + x+5, m_y+5, fill='black', outline='black', alpha=1.0)
        canvas.create_rectangle(m_x, m_y, m_x+5, m_y+5, fill='black', outline='black', alpha=1.0)
    else:
        canvas.create_rectangle(m_x, c_y + y, m_x, c_y + y, fill='black', outline='black', alpha=1.0)
        canvas.create_rectangle(c_x + x, m_y, c_x + x, m_y, fill='black', outline='black', alpha=1.0)
        canvas.create_rectangle(m_x, m_y, m_x, m_y, fill='black', outline='black', alpha=1.0)


def okr(event):
    global prev_x, prev_y
    x = event.x
    y = event.y
    if prev_x:
        leng = round(mat.sqrt(abs(x-prev_x)*abs(x-prev_x)+abs(y-prev_y)*abs(y-prev_y))+0.5)
        pred = prev_y
        x0 = 0
        y0 = leng
        #delt = x0^2 + y0^2 - leng^2
        delt = 2 - 2*leng
        if debuger:
            canvas.wait_variable(pic)
            image = canvas.create_rectangle(x0, y0, x0+5, y0+5, fill='black', outline='black', alpha=1.0)
        else:
            image = canvas.create_rectangle(x0, y0, x0, y0, fill='black', outline='black', alpha=1.0)
        while y0 > 0:
            if delt > 0:
                bet = 2*delt-2*x0-1
                if bet > 0:
                    y0 = y0-1
                    delt = delt-2*y0+1
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + prev_x, y0 + prev_y, x0 + prev_x+5, y0 + prev_y+5,
                                                        fill='black', outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0 + prev_x, y0 + prev_y, x0 + prev_x, y0 + prev_y,
                                                    fill='black', outline='black', alpha=1.0)
                    mirr(x0, y0, prev_x, prev_y)
                else:
                    x0 = x0+1
                    y0 = y0-1
                    delt = delt+2*x0-2*y0+2
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + prev_x, y0 + prev_y, x0 + prev_x+5, y0 + prev_y+5,
                                                        fill='black', outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0+prev_x, y0+prev_y, x0+prev_x, y0+prev_y,
                                                        fill='black', outline='black', alpha=1.0)
                    mirr(x0, y0, prev_x, prev_y)
            elif delt < 0:
                bet = 2*delt+2*y0-1
                if bet <= 0:
                    x0 = x0+1
                    delt = delt+2*x0+1
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + prev_x, y0 + prev_y, x0 + prev_x +5, y0 + prev_y+5,
                                                        fill='black', outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0+prev_x, y0+prev_y, x0+prev_x, y0+prev_y, fill='black', outline='black', alpha=1.0)
                    mirr(x0, y0, prev_x, prev_y)
                else:
                    x0 = x0 + 1
                    y0 = y0 - 1
                    delt = delt + 2 * x0 - 2 * y0 + 2
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + prev_x, y0 + prev_y, x0 + prev_x+5, y0 + prev_y+5,
                                                        fill='black', outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0+prev_x, y0+prev_y, x0+prev_x, y0+prev_y, fill='black', outline='black', alpha=1.0)
                    mirr(x0, y0, prev_x, prev_y)
            elif delt == 0:
                x0 = x0 + 1
                y0 = y0 - 1
                delt = delt + 2 * x0 - 2 * y0 + 2
                if debuger:
                    image = canvas.create_rectangle(x0+prev_x, y0+prev_y, x0+prev_x+5, y0+prev_y+5, fill='black', outline='black', alpha=1.0)
                else:
                    image = canvas.create_rectangle(x0+prev_x, y0+prev_y, x0+prev_x, y0+prev_y, fill='black', outline='black', alpha=1.0)
                mirr(x0, y0, prev_x, prev_y)
        x = None
        y = None
        prev_x = None
        prev_y = None
    else:
        prev_x = x
        prev_y = y


def ell(event):
    global prev_x, prev_y, debuger
    x = event.x
    y = event.y
    if prev_x:
        c_x = round((x+prev_x)/2)
        c_y = round((y+prev_y)/2)
        a = round(abs((x - prev_x) / 2))
        b = round(abs((y - prev_y) / 2))
        # delt = x0^2 + y0^2 - leng^2
        delt = a**2 + b**2 -2*b*(a**2)
        x0, y0 = 0, b
        # if debuger:
        #     canvas.wait_variable(pic)
        #     image = canvas.create_rectangle(x0, y0 + b, x0+5, y0 + b+5, fill='black', outline='black', alpha=1.0)
        # else:
        #     image = canvas.create_rectangle(x0, y0+b, x0, y0+b, fill='black', outline='black', alpha=1.0)
        while y0 > 0:
            if delt > 0:
                bet = 2 * delt - 2 * x0 * b**2 - b**2
                if bet > 0:
                    y0 = y0 - 1
                    delt = delt + a**2 - 2 * y0 * (a**2)
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x+5, y0 + c_y+5,
                                                        fill='black', outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x, y0 + c_y,
                                                    fill='black', outline='black', alpha=1.0)
                    mirr(x0, y0, c_x, c_y)
                else:
                    x0 = x0 + 1
                    y0 = y0 - 1
                    delt = delt + b**2 + 2*x0*(b**2) + a**2 - 2*y0*(a**2)
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x+5, y0 + c_y+5, fill='black',
                                                        outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x, y0 + c_y, fill='black',
                                                    outline='black', alpha=1.0)
                    mirr(x0, y0, c_x, c_y)
            elif delt < 0:
                bet = 2 * delt + 2 * y0 * (a**2) - a**2
                if bet <= 0:
                    x0 = x0 + 1
                    delt = delt + 2 * x0*(b**2) + b**2
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x+5, y0 + c_y+5, fill='black',
                                                        outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x, y0 + c_y, fill='black',
                                                    outline='black', alpha=1.0)
                    mirr(x0, y0, c_x, c_y)
                else:
                    x0 = x0 + 1
                    y0 = y0 - 1
                    delt = delt + b**2 + 2*x0*(b**2) + a**2 - 2*y0*(a**2)
                    if debuger:
                        canvas.wait_variable(pic)
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x+5, y0 + c_y+5, fill='black',
                                                        outline='black', alpha=1.0)
                    else:
                        image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x, y0 + c_y, fill='black',
                                                    outline='black', alpha=1.0)
                    mirr(x0, y0, c_x, c_y)
            elif delt == 0:
                x0 = x0 + 1
                y0 = y0 - 1
                delt = delt + b**2 + 2*x0*(b**2) + a**2 - 2*y0*(a**2)
                if debuger:
                    canvas.wait_variable(pic)
                    image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x+5, y0 + c_y+5, fill='black',
                                                    outline='black', alpha=1.0)
                else:
                    image = canvas.create_rectangle(x0 + c_x, y0 + c_y, x0 + c_x, y0 + c_y, fill='black',
                                                outline='black', alpha=1.0)
                mirr(x0, y0, c_x, c_y)
        x = None
        y = None
        prev_x = None
        prev_y = None
    else:
        prev_x = x
        prev_y = y


def hyper(event):
    global prev_x, prev_y, A, B, direction, debuger
    x = event.x
    y = event.y
    for сx in range(x - 200, x + 201):
        try:
            y_positive = y + int(B) * ((int(A) ** 2 + (сx - x) ** 2) ** 0.5) / int(A)
            y_negative = y - int(B) * ((int(A) ** 2 + (сx - x) ** 2) ** 0.5) / int(A)
            if direction == "vert":
                if debuger:
                    canvas.wait_variable(pic)
                    canvas.create_oval(сx, y_positive, сx + 1, y_positive + 1, width=5, fill="black")
                else:
                    canvas.create_oval(сx, y_positive, сx + 1, y_positive + 1, fill="black")
            else:
                if debuger:
                    canvas.wait_variable(pic)
                    canvas.create_oval(сx, y_negative, сx + 1, y_negative + 1, width=5, fill="black")
                else:
                    canvas.create_oval(сx, y_negative, сx + 1, y_negative + 1, fill="black")
        except ZeroDivisionError:
            pass


def para(event):
    global prev_x, prev_y, debuger, A, B, direction
    x = event.x
    y = event.y
    A = float(A)
    if direction == 'down':
        cy = lambda cx: A*(cx-x)**2+y
    else:
        cy = lambda cx: -A * (cx - x) ** 2 + y
    for cx in range(x-100, x+101):
        if debuger:
            canvas.wait_variable(pic)
            canvas.create_oval(cx,cy(cx),cx+1,cy(cx+1), width=5, outline='black')
        else:
            canvas.create_oval(cx, cy(cx), cx + 1, cy(cx + 1), outline='black')
    x = None
    y = None
    # if prev_x:
        # def save():
        #     global A, B
        #     A = entry1.get()
        #     B = entry2.get()
        # coor = tk.Tk()
        # size = 100
        # canvas1 = TrCanvas(root, bg='white', width=size, height=size)
        # coor.geometry("200x200")
        # coor.title('a и b')
        # label1 = Label(text='Значение А:')
        # label1.pack()
        # entry1 = ttk.Entry(coor)
        # entry1.pack(anchor=NE)
        # label2 = Label(text='Значение B:')
        # label2.pack()
        # entry2 = ttk.Entry(coor)
        # entry2.pack(anchor=NE)
        # saves = Button(coor, text='Сохранить', command=save)
        # saves.pack()
        # canvas1.pack(anchor='s', expand=False, fill=BOTH)
        # coor.mainloop()
        #передпредыдущий
        # p2 = 2*y
        # p4 = p2*2
        # y0 = 0
        # x0 = 0
        # d = 1 - y
        # while y0 < y and x0 < x:
        #     image = canvas.create_rectangle(x0+prev_x, abs(y0-prev_y), x0+prev_x, abs(y0-prev_y), fill='black',
        #                                             outline='black', alpha=1.0)
        #     if d>=0:
        #         x0+=1
        #         d -= p2
        #     y0+=1
        #     d+= 2 * y0+1
        # if d == 1:
        #     d = 1 - p4
        # else:
        #     d = 1 - p2
        # while x0 <= x:
        #     image = canvas.create_rectangle(x0+prev_x, abs(y0-prev_y), x0+prev_x, abs(y0-prev_y), fill='black',
        #                                     outline='black', alpha=1.0)
        #     if d <= 0:
        #         y0 += 1
        #         d += 4 * y0
        #     x0 += 1
        #     d -= p4
        #предыдущий варик
        # a = (y - prev_y)/((x - prev_x)*(x+prev_x))
        # b = prev_y-a*prev_x**2
        # for cx in range(prev_x,x+1):
        #     cy = round(a*cx**2+b+0.5)
        #     image = canvas.create_rectangle(cx, cy, cx, cy, fill='black', outline='black', alpha=1.0)
        # x = None
        # y = None
        # prev_x = None
        # prev_y = None
    # else:
    #     prev_x = x
    #     prev_y = y


def sel_ovals(event):
    selection = combobox2.get()
    if selection == 'Окружность':
        canvas.unbind('<1>')
        canvas.bind('<1>', okr)
    elif selection == 'Эллипс':
        canvas.unbind('<1>')
        canvas.bind('<1>', ell)
    elif selection == 'Гипербола':
        canvas.unbind('<1>')
        canvas.bind('<1>', hyper)
    elif selection == 'Парабола':
        canvas.unbind('<1>')
        canvas.bind('<1>', para)
    else:
        canvas.unbind('<2>')


def save():
    global A, B
    A = entry1.get()
    B = entry2.get()


def direct(event):
    global direction
    direct = combobox.get()
    if direct == 'Вверх':
        direction = 'up'
    elif direct == 'Вниз':
        direction = 'down'
    elif direct == 'Вертикально':
        direction = 'vert'
    elif direct == 'Горизонтально':
        direction = 'horiz'

#Кривые
def interpol(event):
    global col_p
    selection = combobox3.get()
    if selection == 'Эрмит':
        canvas.unbind('<1>')
        canvas.bind('<1>', ermit)
    elif selection == 'Безье':
        canvas.unbind('<1>')
        canvas.bind('<1>', beze)
    elif selection == 'В-сплайн':
        col_p = int(entry3.get())
        canvas.unbind('<1>')
        canvas.bind('<1>', bsplayn)
    else:
        canvas.unbind('<2>')


def ermit(event):
    global prev_x, prev_y, last_coor
    x = event.x
    y = event.y
    if prev_x:
        p1x, p1y = prev_x, prev_y
        p4x, p4y = x, y
        r1x, r1y = prev_x, y
        r4x, r4y = x, y
        l1 = [(2*p1x+(-2)*p4x+r1x+r4x),(2*p1y+(-2)*p4y+r1y+r4y)]
        l2 = [((-3)*p1x+3*p4x+(-2)*r1x-r4x),((-3)*p1y+3*p4y+(-2)*r1y-r4y)]
        l3 = [r1x,r1y]
        l4 = [p1x,p1y]
        t = 0
        cxp = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
        cyp = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
        t += 0.1
        while t <= 1:
            cx = l1[0]*(t**3)+l2[0]*(t**2)+l3[0]*t+l4[0]
            cy = l1[1]*(t**3)+l2[1]*(t**2)+l3[1]*t+l4[1]
            #canvas.create_line(round(cx), round(cy), round(cxp), round(cyp))
            cda_ermit(round(cx), round(cy), round(cxp), round(cyp))
            cxp = cx
            cyp = cy
            t += 0.1
        last_coor.append([prev_x, prev_y])
        last_coor.append([x, y])
        prev_y = None
        prev_x = None
        y = None
        x = None
    else:
        prev_x = x
        prev_y = y


def cda_ermit(prev_x, prev_y, x, y):
    global debuger
    tx = prev_x - x
    ty = prev_y - y
    leng = max(abs(tx), abs(ty))
    dy = ty / leng
    dx = tx / leng

    dot_x = 0
    dot_y = 0

    if dx < 0:
        dot_x = x + 0.5 * (-1)
    elif dx == 0:
        dot_x = x
    elif dx > 0:
        dot_x = x + 0.5

    if dy < 0:
        dot_y = y + 0.5 * (-1)
    elif dy == 0:
        dot_y = y
    elif dy > 0:
        dot_y = y + 0.5
    i = 0
    dot_y1 = None
    dot_x1 = None
    while i < leng:
        if debuger:
            dot_x1 = dot_x + dx
            dot_y1 = dot_y + dy
            canvas.wait_variable(pic)
            image = canvas.create_rectangle(round(dot_x) + 5, round(dot_y1) + 5, round(dot_x) + 10, round(dot_y1) + 10,
                                            width=5, fill='black', outline='black', alpha=1.0)
            i += 5
        else:
            dot_x1 = dot_x + dx
            dot_y1 = dot_y + dy
            image = canvas.create_rectangle(round(dot_x), round(dot_y1), round(dot_x), round(dot_y1),
                                            fill='black', outline='black', alpha=1.0)
            i += 1
        dot_x = dot_x1
        dot_y = dot_y1


def beze(event):
    global coord, last_coor
    x = event.x
    y = event.y
    if len(coord) == 3:
        p1, p2 = [coord[0][0], coord[0][1]], [coord[1][0], coord[1][1]]
        p3, p4 = [coord[2][0], coord[2][1]], [x, y]
        l1 = [(-1)*p1[0]+3*p2[0]-3*p3[0]+p4[0],(-1)*p1[1]+3*p2[1]-3*p3[1]+p4[1]]
        l2 = [3*p1[0]-6*p2[0]+3*p3[0],3*p1[1]-6*p2[1]+3*p3[1]]
        l3 = [(-3)*p1[0]+3*p2[0],(-3)*p1[1]+3*p2[1]]
        l4 = [p1[0],p1[1]]
        t = 0
        cxp = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
        cyp = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
        t += 0.1
        while t <= 1:
            cx = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
            cy = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
            # canvas.create_line(round(cx), round(cy), round(cxp), round(cyp))
            cda_ermit(round(cx), round(cy), round(cxp), round(cyp))
            cxp = cx
            cyp = cy
            t += 0.1
        for l in coord:
            last_coor.append(l)
        last_coor.append([x,y])
        coord.clear()
        y = None
        x = None
    else:
        coord.append([x, y])


def bsplayn(event):
    global direction, coord, last_coor, zamk, col_p
    x = event.x
    y = event.y
    if len(coord) == col_p - 1:
        coord.append([x, y])
        if zamk:
            coord.append([coord[0][0], coord[0][1]])
            coord.append([coord[1][0], coord[1][1]])
            coord.append([coord[2][0], coord[2][1]])
        for i in range(1, len(coord)-2):
            p1, p2 = [coord[i-1][0], coord[i-1][1]], [coord[i][0], coord[i][1]]
            p3, p4 = [coord[i+1][0], coord[i+1][1]], [coord[i+2][0], coord[i+2][1]]
            l1 = [(-1)*p1[0]+3*p2[0]-3*p3[0]+p4[0], (-1)*p1[0]+3*p2[0]-3*p3[0]+p4[0]]
            l2 = [3*p1[0]-6*p2[0]+3*p3[0], 3*p1[1]-6*p2[1]+3*p3[1]]
            l3 = [(-3)*p1[0]+3*p3[0], (-3)*p1[0]+3*p3[0]]
            l4 = [p1[0]+4*p2[0]+p3[0], p1[0]+4*p2[0]+p3[0]]
            t = 0
            cxp = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
            cyp = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
            t += 0.1
            while t <= 1:
                cx = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
                cy = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
                # canvas.create_line(round(cx), round(cy), round(cxp), round(cyp))
                brez_b(round(cx/6 + 0.5), round(cy/6 + 0.5), round(cxp/6 + 0.5), round(cyp/6 + 0.5))
                cxp = cx
                cyp = cy
                t += 0.1
        for l in coord:
            last_coor.append(l)
        last_coor.append([x, y])
        coord.clear()
        y = None
        x = None
    else:
        coord.append([x, y])
    #по циклу пройтись. попросиь ввести число точек, и по количеству тоек сохранять по принципу coord[i]=[x.event, y.event]


def brez_b(prev_x, prev_y, x, y):
    dx = x - prev_x
    dy = y - prev_y
    if abs(dx) >= abs(dy):
        main = prev_x
        sec = prev_y
        main_d = dx
        sec_d = dy
    else:
        main = prev_y
        sec = prev_x
        main_d = dy
        sec_d = dx
    e = abs(2 * sec_d) - abs(main_d)
    i = 0
    while i < abs(main_d):
        if e >= 0:
            sec += 1 * sign(sec_d)
            e -= abs(2 * main_d)
        main += 1 * sign(main_d)
        e += abs(2 * sec_d)
        i += 1
        if abs(dx) >= abs(dy):
            image = canvas.create_rectangle(main, sec, main, sec, width=1, fill='black',
                                            outline='black', alpha=1.0)
        else:
            image = canvas.create_rectangle(sec, main, sec, main, width=1, fill='black',
                                            outline='black', alpha=1.0)


def change():
    global last_coor
    chan = tk.Tk()
    canvas = TrCanvas(chan, width=size, height=size)
    chan.geometry("400x400")
    chan.title('Меняем всё к чертям')
    show_ccor = Label(chan, text='Координаты: ')
    st = ''
    for k in range(len(last_coor)):
        st += 'x'+str(k+1)+': '+str(last_coor[k][0])+'   y'+str(k+1)+': '+str(last_coor[k][1])+'\n'
    show_ccor['text'] = f'Координаты: \n{st}'
    show_ccor.pack()
    var1 = Label(chan, text='Введите номер координат, которые хотите изменить')
    var1.pack()
    entr1 = ttk.Entry(chan)
    entr1.pack()
    var2 = Label(chan, text='Введите изменение (1 - для х, 2 - для у)')
    var2.pack()
    entr21 = ttk.Entry(chan)
    entr21.pack()
    entr22 = ttk.Entry(chan)
    entr22.pack()
    krivs1 = ['Эрмит', 'Безье', 'В-сплайн']
    kriv1 = StringVar(chan, value=krivs1[0])
    comboboxc = ttk.Combobox(chan, values=krivs1, textvariable=kriv1, width=11)
    comboboxc.pack()
    def ent():
        if not entr1.get() == None:
            i = int(entr1.get())
        if not entr21.get() == None and not entr22.get() == None:
            last_coor[i - 1][0] = int(entr21.get())
            last_coor[i - 1][1] = int(entr22.get())
            selection = comboboxc.get()
            if selection == 'Эрмит':
                ermit_c()
            elif selection == 'Безье':
                beze_c()
            elif selection == 'В-сплайн':
                bsplayn_c()
    enter = Button(chan, text='Изменить', command=ent)
    enter.pack()


def ermit_c():
    global last_coor
    canvas.delete(tk.ALL)
    prev_x, prev_y = last_coor[0][0], last_coor[0][1]
    x, y = last_coor[1][0], last_coor[1][1]
    p1x, p1y = prev_x, prev_y
    p4x, p4y = x, y
    r1x, r1y = prev_x, y
    r4x, r4y = x, y
    l1 = [(2 * p1x + (-2) * p4x + r1x + r4x), (2 * p1y + (-2) * p4y + r1y + r4y)]
    l2 = [((-3) * p1x + 3 * p4x + (-2) * r1x - r4x), ((-3) * p1y + 3 * p4y + (-2) * r1y - r4y)]
    l3 = [r1x, r1y]
    l4 = [p1x, p1y]
    t = 0
    cxp = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
    cyp = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
    t += 0.1
    while t <= 1:
        cx = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
        cy = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
        # canvas.create_line(round(cx), round(cy), round(cxp), round(cyp))
        cda_ermit(round(cx), round(cy), round(cxp), round(cyp))
        cxp = cx
        cyp = cy
        t += 0.1
    last_coor.append([prev_x, prev_y])
    last_coor.append([x, y])


def beze_c():
    global coord, last_coor
    canvas.delete(tk.ALL)
    coord = last_coor
    p1, p2 = [coord[0][0], coord[0][1]], [coord[1][0], coord[1][1]]
    p3, p4 = [coord[2][0], coord[2][1]], [coord[3][0], coord[3][1]]
    l1 = [(-1) * p1[0] + 3 * p2[0] - 3 * p3[0] + p4[0], (-1) * p1[1] + 3 * p2[1] - 3 * p3[1] + p4[1]]
    l2 = [3 * p1[0] - 6 * p2[0] + 3 * p3[0], 3 * p1[1] - 6 * p2[1] + 3 * p3[1]]
    l3 = [(-3) * p1[0] + 3 * p2[0], (-3) * p1[1] + 3 * p2[1]]
    l4 = [p1[0], p1[1]]
    t = 0
    cxp = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
    cyp = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
    t += 0.1
    while t <= 1:
        cx = l1[0] * (t ** 3) + l2[0] * (t ** 2) + l3[0] * t + l4[0]
        cy = l1[1] * (t ** 3) + l2[1] * (t ** 2) + l3[1] * t + l4[1]
        # canvas.create_line(round(cx), round(cy), round(cxp), round(cyp))
        cda_ermit(round(cx), round(cy), round(cxp), round(cyp))
        cxp = cx
        cyp = cy
        t += 0.1
    last_coor = coord
    coord.clear()


def bsplayn_c():
    pass


def smena():
    global zamk
    if colt.get() == 0:
        zamk = False
    else:
        zamk = True


def pess():
    global col_p
    col_p = entry3.get()


root = tk.Tk()
size = 600
canvas = TrCanvas(root, bg='white', width=size, height=size)
root.geometry("700x700")
root.title('Графический редактор, определённо')

f_left = Frame(root)
f_top = Frame(root)
f_right = Frame(root)

lab = Label(f_top, text='Направление: ')
dirs = ['Вверх', 'Вниз', 'Вертикально', 'Горизонтально']
dirc = StringVar(value=dirs[0])
combobox = ttk.Combobox(f_top, values=dirs, textvariable=dirc, width=11)
combobox.bind('<<ComboboxSelected>>', direct)
label1 = Label(f_top, text='Значение А:')
entry1 = ttk.Entry(f_top, width=5)
label2 = Label(f_top, text='Значение B:')
entry2 = ttk.Entry(f_top, width=5)
saves = Button(f_top, text='Ввод', command=save)
chang = Button(f_top, text='Изменить', command=change)



lines = ['Линия','ЦДА','Брезенхем','Ву']
line = StringVar(value=lines[0])
combobox1 = ttk.Combobox(f_left, values=lines, textvariable=line, width=11)
combobox1.bind('<<ComboboxSelected>>', selected)
ovals = ['Линии 2-го порядка','Окружность','Эллипс','Гипербола','Парабола']
oval = StringVar(value=ovals[0])
combobox2 = ttk.Combobox(f_left, values=ovals, textvariable=oval, width=11)
combobox2.bind('<<ComboboxSelected>>', sel_ovals)
krivs = ['Кривые','Эрмит','Безье','В-сплайн']
kriv = StringVar(value=krivs[0])
combobox3 = ttk.Combobox(f_left, values=krivs, textvariable=kriv, width=11)
combobox3.bind('<<ComboboxSelected>>', interpol)

label3 = Label(f_left, text='Количество точек:')
entry3 = ttk.Entry(f_left, width=5)
colt = IntVar()
zam = ttk.Checkbutton(f_left, text='Замкнутость',variable=colt, command=smena)
press = Button(f_left, text='Ввод', command=pess)


debuge = Button(f_right, text='Debug', command=debug)
pic = tk.IntVar(value=0)
step = Button(f_right, text='Шаг', command=draw)
clear = Button(f_right, text='Очистить', command=lambda : canvas.delete(tk.ALL))

f_left.pack()
f_top.pack()
f_right.pack()

lab.pack(side=LEFT)
combobox.pack(side=LEFT)
label1.pack(side=LEFT)
entry1.pack(side=LEFT)
label2.pack(side=LEFT)
entry2.pack(side=LEFT)
saves.pack(side=LEFT)
chang.pack(side=LEFT)

combobox1.pack(side=LEFT)
combobox2.pack(side=LEFT)
combobox3.pack(side=LEFT)

label3.pack(side=LEFT)
entry3.pack(side=LEFT)
zam.pack(side=LEFT)
press.pack(side=LEFT)

debuge.pack(side=LEFT)
step.pack(side=LEFT)
clear.pack(side=LEFT)
# bt_line1 = Button(text='Нарисовать линию (ЦДА)', command=dr_line1)
# bt_line1.pack()
# bt_line2 = Button(text='Нарисовать линию (Брезенхем)', command=dr_line2)
# bt_line2.pack()
# bt_line3 = Button(text='Нарисовать линию (Ву)', command=dr_line3)
# bt_line3.pack()
canvas.pack(anchor='s', expand=False, fill=BOTH)

root.mainloop()
# diap = 0
# while diap < 1000:
#     pass