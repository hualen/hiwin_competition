#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.constants import CENTER
from PIL import Image,ImageTk


win = tk.Tk() # 如果使用直譯器的話，在這行Enter後就會先看到一個視窗了！
win.title('點餐機') # 更改視窗的標題
win.geometry('720x640') # 修改視窗大小(寬x高)
win.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False

tea_image = Image.open('src/competition/photo/tea.png')
tea_w = tea_image.width
tea_h = tea_image.height
tea_image = tea_image.resize((int(tea_w*0.18),int(tea_h*0.18)))
tea_img = ImageTk.PhotoImage(tea_image)

puf_image = Image.open('src/competition/photo/puff.png')
puf_w = puf_image.width
puf_h = puf_image.height
puf_image = puf_image.resize((int(tea_w*0.18),int(tea_h*0.18)))
puf_img = ImageTk.PhotoImage(puf_image)

egg_image = Image.open('src/competition/photo/egg.png')
egg_w = egg_image.width
egg_h = egg_image.height
egg_image = egg_image.resize((int(tea_w*0.18),int(tea_h*0.18)))
egg_img = ImageTk.PhotoImage(egg_image)



num_egg1 = tk.IntVar()
num_egg1.set(0)
num_tea1 = tk.IntVar()
num_tea1.set(0)
num_puff1 = tk.IntVar()
num_puff1.set(0)

num_egg2 = tk.IntVar()
num_egg2.set(0)
num_tea2 = tk.IntVar()
num_tea2.set(0)               
num_puff2 = tk.IntVar()
num_puff2.set(0)

num_egg3 = tk.IntVar()
num_egg3.set(0)
num_tea3 = tk.IntVar()
num_tea3.set(0)
num_puff3 = tk.IntVar()
num_puff3.set(0)

num_egg4 = tk.IntVar()
num_egg4.set(0)
num_tea4 = tk.IntVar()
num_tea4.set(0)
num_puff4 = tk.IntVar()
num_puff4.set(0)

final_order = [ [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0]  ]

def add(item):
    if item.get() < 9:
        item.set(item.get()+1)
    else:
        pass
def sub(item):
    if item.get() > 0:
        item.set(item.get()-1)
    else:
        pass

def clear_window():
    for widget in win.winfo_children():
        widget.destroy()    

def finish():
    # Order 1
    final_order[0][0] = num_tea1.get()
    final_order[0][1] = num_puff1.get()
    final_order[0][2] = num_egg1.get()
    # Order 2
    final_order[1][0] = num_tea2.get()
    final_order[1][1] = num_puff2.get()
    final_order[1][2] = num_egg2.get()
    # Order 3
    final_order[2][0] = num_tea3.get()
    final_order[2][1] = num_puff3.get()
    final_order[2][2] = num_egg3.get()
    
    final_order[3][0] = num_tea4.get()
    final_order[3][1] = num_puff4.get()
    final_order[3][2] = num_egg4.get()
    
    total_egg = final_order[0][0] + final_order[1][0] + final_order[2][0] + final_order[3][0]
    total_tea = final_order[0][1] + final_order[1][1] + final_order[2][1] + final_order[3][1]
    total_puff = final_order[0][2] + final_order[1][2] + final_order[2][2] + final_order[3][2]
    if total_egg > 9 or total_tea > 9 or total_puff > 9:
        clear_window()
        retext = tk.Label(win,text='The item demand \nexceeds the inventory!\nPlease place your order again.',font=('Time New Roman',32))
        retext.place(x=360,y=200,anchor=CENTER)
        resbutton = tk.Button(win,text="restart",font=('Time New Roman',28),command = restart)
        resbutton.place(x=360,y=350,anchor=CENTER)
    elif total_egg == 0 and total_tea == 0 and total_puff == 0:
        clear_window()
        retext = tk.Label(win,text='The order does not \ncontain any items!\nPlease place your order again.',font=('Time New Roman',32))
        retext.place(x=360,y=200,anchor=CENTER)
        resbutton = tk.Button(win,text="restart",font=('Time New Roman',28),command = restart)
        resbutton.place(x=360,y=350,anchor=CENTER)
    else:
        win.destroy()
        return final_order
    
def test_order():
    # Order 1
    final_order[0][0] = 1
    final_order[0][1] = 1
    final_order[0][2] = 1
    # Order 2
    final_order[1][0] = 0
    final_order[1][1] = 0
    final_order[1][2] = 0
    # Order 3
    final_order[2][0] = 0
    final_order[2][1] = 0
    final_order[2][2] = 0
    # Order 4
    final_order[3][0] = 0
    final_order[3][1] = 0
    final_order[3][2] = 0
    win.destroy()
    return final_order    
    
def restart() :
    clear_window()

    num_egg1.set(0)
    num_tea1.set(0)
    num_puff1.set(0)

    num_egg2.set(0)
    num_tea2.set(0)
    num_puff2.set(0)

    num_egg3.set(0)
    num_tea3.set(0)
    num_puff3.set(0)

    num_egg4.set(0)
    num_tea4.set(0)
    num_puff4.set(0)

    title = tk.Label(win,text='Crazy Chihuahua',bg = 'yellow',font=('Time New Roman',40),padx=720)
    title.place(x=360,y=30,anchor=CENTER)
    start_order()

def order1():
    start.destroy()
    test.destroy()
    last_order.destroy()           
    # order
    order = tk.Label(win,text='order1',font=('Time New Roman',32))
    order.place(x=360,y=110,anchor=CENTER)
    # Kinder Joy
    egg = tk.Label(win,image=egg_img,font=('Time New Roman',32))
    egg.place(x=140,y=380,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg1),width=2)
    add1.place(x=320,y=380,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg1,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=470,y=380,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg1),width=2)
    sub1.place(x=620,y=380,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,image=tea_img,font=('Time New Roman',32))
    tea.place(x=140,y=200,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea1),width=2)
    add2.place(x=320,y=200,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea1,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=470,y=200,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea1),width=2)
    sub2.place(x=620,y=200,anchor=CENTER)

    # Puffs
    puff = tk.Label(win,image=puf_img,font=('Time New Roman',32))
    puff.place(x=140,y=290,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff1),width=2)
    add3.place(x=320,y=290,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff1,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=470,y=290,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff1),width=2)
    sub3.place(x=620,y=290,anchor=CENTER)
    
    # next
    next_order = tk.Button(win,text="next",font=('Time New Roman',28),width=4,height=2,command=order2)
    next_order.place(x=620,y=520,anchor=CENTER)

def order2():
    global last_order
    last_order.destroy()
    # order
    order = tk.Label(win,text='order2',font=('Time New Roman',32))
    order.place(x=360,y=110,anchor=CENTER)
    # Kinder Joy
    egg = tk.Label(win,image=egg_img,font=('Time New Roman',32))
    egg.place(x=140,y=380,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg2),width=2)
    add1.place(x=320,y=380,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg2,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=470,y=380,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg2),width=2)
    sub1.place(x=620,y=380,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,image=tea_img,font=('Time New Roman',32))
    tea.place(x=140,y=200,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea2),width=2)
    add2.place(x=320,y=200,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea2,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=470,y=200,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea2),width=2)
    sub2.place(x=620,y=200,anchor=CENTER)

    # Puffs
    puff = tk.Label(win,image=puf_img,font=('Time New Roman',32))
    puff.place(x=140,y=290,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff2),width=2)
    add3.place(x=320,y=290,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff2,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=470,y=290,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff2),width=2)
    sub3.place(x=620,y=290,anchor=CENTER)

    # next
    next_order = tk.Button(win,text="next",font=('Time New Roman',28),width=4,height=2,command=order3)
    next_order.place(x=620,y=520,anchor=CENTER)
    
    # last
    last_order = tk.Button(win,text="last",font=('Time New Roman',28),width=4,height=2,command=order1)
    last_order.place(x=140,y=520,anchor=CENTER)
    
def order3():
    global last_order
    fin_order.destroy()
    last_order.destroy()
    # order
    order = tk.Label(win,text='order3',font=('Time New Roman',32))
    order.place(x=360,y=110,anchor=CENTER)
    # Kinder Joy
    egg = tk.Label(win,image=egg_img,font=('Time New Roman',32))
    egg.place(x=140,y=380,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg3),width=2)
    add1.place(x=320,y=380,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg3,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=470,y=380,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg3),width=2)
    sub1.place(x=620,y=380,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,image=tea_img,font=('Time New Roman',32))
    tea.place(x=140,y=200,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea3),width=2)
    add2.place(x=320,y=200,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea3,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=470,y=200,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea3),width=2)
    sub2.place(x=620,y=200,anchor=CENTER)

    # Puffs
    puff = tk.Label(win,image=puf_img,font=('Time New Roman',32))
    puff.place(x=140,y=290,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff3),width=2)
    add3.place(x=320,y=290,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff3,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=470,y=290,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff3),width=2)
    sub3.place(x=620,y=290,anchor=CENTER)
    
    # next
    next_order = tk.Button(win,text="next",font=('Time New Roman',28),width=4,height=2,command=order4)
    next_order.place(x=620,y=520,anchor=CENTER)
    
    # last
    last_order = tk.Button(win,text="last",font=('Time New Roman',28),width=4,height=2,command=order2)
    last_order.place(x=140,y=520,anchor=CENTER)


def order4():
    global fin_order,last_order,next_order
    next_order.destroy()
    
    # order
    order = tk.Label(win,text='order4',font=('Time New Roman',32))
    order.place(x=360,y=110,anchor=CENTER)
    # Kinder Joy
    egg = tk.Label(win,image=egg_img,font=('Time New Roman',32))
    egg.place(x=140,y=380,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg4),width=2)
    add1.place(x=320,y=380,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg4,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=470,y=380,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg4),width=2)
    sub1.place(x=620,y=380,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,image=tea_img,font=('Time New Roman',32))
    tea.place(x=140,y=200,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea4),width=2)
    add2.place(x=320,y=200,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea4,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=470,y=200,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea4),width=2)
    sub2.place(x=620,y=200,anchor=CENTER)

    # Puffs
    puff = tk.Label(win,image=puf_img,font=('Time New Roman',32))
    puff.place(x=140,y=290,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff4),width=2)
    add3.place(x=320,y=290,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff4,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=470,y=290,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff4),width=2)
    sub3.place(x=620,y=290,anchor=CENTER)
    
    next_order.destroy()
    # 結束
    fin_order = tk.Button(win,text="Finish",font=('Time New Roman',28),command=finish,width=4,height=2)
    fin_order.place(x=620,y=520,anchor=CENTER)
    
    # last
    last_order = tk.Button(win,text="last",font=('Time New Roman',28),width=4,height=2,command=order3)
    last_order.place(x=140,y=520,anchor=CENTER)        

def start_order():
    global  start,test,next_order,last_order,fin_order  
    # 標題
    title = tk.Label(win,text='Crazy Chihuahua',bg = 'yellow',font=('Time New Roman',40),padx=720)
    title.place(x=360,y=30,anchor=CENTER)

    next_order = tk.Button(win,text="next",font=('Time New Roman',28),width=4,height=2)
    last_order = tk.Button(win,text="last",font=('Time New Roman',28),width=4,height=2)
    fin_order = tk.Button(win,text="Finish",font=('Time New Roman',28),command=finish,width=2,height=2)

    start = tk.Button(win,text="Start",font=('Time New Roman',28),command=order1,width=7)
    start.place(x=360,y=260,anchor=CENTER)

    test = tk.Button(win,text="Test",font=('Time New Roman',28),command=test_order,width=7)
    test.place(x=360,y=380,anchor=CENTER)

    win.mainloop() # 在一般python xxx.py的執行方式中，呼叫mainloop()才算正式啟動
    return fin_order
    
if __name__ == '__main__'  :
    start_order()
    for i in range(0,4):
        print("訂單",i+1)
        print("麥香：",final_order[i][0],"個")
        print("泡芙：",final_order[i][1],"個")
        print("奇趣蛋：",final_order[i][2],"個")
        print("\n")