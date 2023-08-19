import tkinter as tk
from tkinter.constants import CENTER
win = tk.Tk() # 如果使用直譯器的話，在這行Enter後就會先看到一個視窗了！
win.title('點餐機') # 更改視窗的標題
win.geometry('720x640') # 修改視窗大小(寬x高)
win.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False

teaX = tk.IntVar()
teaX.set(0)
teaX = tk.IntVar()
teaX.set(0)
teaZ = tk.IntVar()
teaZ.set(0)
teaA = tk.IntVar()
teaA.set(0)
teaB = tk.IntVar()
teaB.set(0)
teaC = tk.IntVar()
teaC.set(0)

puffX = tk.IntVar()
puffX.set(0)
puffX = tk.IntVar()
puffX.set(0)
puffZ = tk.IntVar()
puffZ.set(0)
puffA = tk.IntVar()
puffA.set(0)
puffB = tk.IntVar()
puffB.set(0)
puffC = tk.IntVar()
puffC.set(0)

eggX = tk.IntVar()
eggX.set(0)
eggX = tk.IntVar()
eggX.set(0)
eggZ = tk.IntVar()
eggZ.set(0)
eggA = tk.IntVar()
eggA.set(0)
eggB = tk.IntVar()
eggB.set(0)
eggC = tk.IntVar()
eggC.set(0)


item_axis = 

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
    

def order1():
    start.destroy()
    last_order.destroy()
    # 訂單
    order = tk.Label(win,text='訂單1 ',font=('標楷體',32))
    order.place(x=360,y=110,anchor=CENTER)
    # 奇趣蛋
    egg = tk.Label(win,text='奇趣蛋',font=('標楷體',32))
    egg.place(x=120,y=200,anchor=CENTER)

    negg = tk.Entry(win,textvariable=num_egg1,bg = '#E0E0E0',font=('Time New Roman',28),justify='center')
    negg.place(x=450,y=200,anchor=CENTER)


    # 麥香
    tea = tk.Label(win,text='麥香紅茶',font=('標楷體',32))
    tea.place(x=120,y=290,anchor=CENTER)

    ntea = tk.Entry(win,textvariable=num_tea1,bg = '#E0E0E0',font=('Time New Roman',28),justify='center')
    ntea.place(x=450,y=290,anchor=CENTER)


    # 泡芙
    puff = tk.Label(win,text='泡芙',font=('標楷體',32))
    puff.place(x=120,y=380,anchor=CENTER)

    npuff = tk.Entry(win,textvariable=num_puff1,bg = '#E0E0E0',font=('Time New Roman',28),justify='center')
    npuff.place(x=450,y=380,anchor=CENTER)
    
    # 下一筆
    next_order = tk.Button(win,text="下一筆",font=('標楷體',28),command=order2)
    next_order.place(x=600,y=520,anchor=CENTER)


def start_order():
    global  start,next_order,last_order,fin_order  
    # 標題
    title = tk.Label(win,text='物品座標點位',font=('標楷體',40))
    title.place(x=360,y=30,anchor=CENTER)

    fin_order = tk.Button(win,text="完成定位",font=('標楷體',28),command=finish)

    

    win.mainloop() # 在一般python xxx.py的執行方式中，呼叫mainloop()才算正式啟動
    
if __name__ == '__main__'  :
    start_order() 