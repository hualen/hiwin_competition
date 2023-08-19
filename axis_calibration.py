#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.constants import CENTER
from PIL import Image,ImageTk

start_ac = False
next_go = True

# axis_txt = open('src/competition/photo/axis_calibration.txt','w+')
# for i in range(0,3):
#     for j in range(0,3):
#         axis_txt.write('0.0'+' ')
#     axis_txt.write('\n')
# axis_txt.close()

'''
    召喚視窗
'''
win = tk.Tk() # 如果使用直譯器的話，在這行Enter後就會先看到一個視窗了！
win.title('座標調整') # 更改視窗的標題
win.geometry('1280x720+700+100') # 修改視窗大小(寬x高)
win.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False

'''
    召喚圖片
'''
tea_image = Image.open('src/competition/photo/tea.png')
tea_w = tea_image.width
tea_h = tea_image.height
tea_image = tea_image.resize((int(tea_w*0.3),int(tea_h*0.3)))
tea_img = ImageTk.PhotoImage(tea_image)

puf_image = Image.open('src/competition/photo/puff.png')
puf_w = puf_image.width
puf_h = puf_image.height
puf_image = puf_image.resize((int(tea_w*0.3),int(tea_h*0.3)))
puf_img = ImageTk.PhotoImage(puf_image)

egg_image = Image.open('src/competition/photo/egg.png')
egg_w = egg_image.width
egg_h = egg_image.height
egg_image = egg_image.resize((int(tea_w*0.3),int(tea_h*0.3)))
egg_img = ImageTk.PhotoImage(egg_image)

tea_x = tk.DoubleVar()
tea_x.set(0.0)
tea_y = tk.DoubleVar()
tea_y.set(0.0)
tea_z = tk.DoubleVar()
tea_z.set(0.0)

puf_x = tk.DoubleVar()
puf_x.set(0.0)
puf_y = tk.DoubleVar()
puf_y.set(0.0)
puf_z = tk.DoubleVar()
puf_z.set(0.0)

egg_x = tk.DoubleVar()
egg_x.set(0.0)
egg_y = tk.DoubleVar()
egg_y.set(0.0)
egg_z = tk.DoubleVar()
egg_z.set(0.0)

axis_calibration =  [   
                        [tea_x.get(),tea_y.get(),tea_z.get()],
                        [puf_x.get(),puf_y.get(),puf_z.get()],
                        [egg_x.get(),egg_y.get(),egg_z.get()]
                    ]

def add(item):
    global tea_x,tea_y,tea_z,puf_x,puf_y,puf_z,egg_x,egg_y,egg_z,start_ac
    # axis_txt = open('src/competition/photo/axis_calibration.txt','w+')
    item.set(item.get()+1.0)
    start_ac = True
    # axis_calibration =  [   
    #                         [tea_x.get(),tea_y.get(),tea_z.get()],
    #                         [puf_x.get(),puf_y.get(),puf_z.get()],
    #                         [egg_x.get(),egg_y.get(),egg_z.get()]
    #                     ]
    # for i in range(0,3):
    #     for j in range(0,3):
    #         axis_txt.write(str(axis_calibration[i][j])+' ')
    #     axis_txt.write('\n')
    # axis_txt.close()    
   
    
def sub(item):
    global tea_x,tea_y,tea_z,puf_x,puf_y,puf_z,egg_x,egg_y,egg_z,start_ac
    item.set(item.get()-1.0)
    start_ac = True
    # axis_txt = open('src/competition/photo/axis_calibration.txt','w+')
    # item.set(item.get()-1.0)
    # axis_calibration =  [   
    #                         [tea_x.get(),tea_y.get(),tea_z.get()],
    #                         [puf_x.get(),puf_y.get(),puf_z.get()],
    #                         [egg_x.get(),egg_y.get(),egg_z.get()]
    #                     ]
    # for i in range(0,3):
    #     for j in range(0,3):
    #         axis_txt.write(str(axis_calibration[i][j])+' ')
    #     axis_txt.write('\n')
    # axis_txt.close() 
def go_next ():
    global next_go
    next_go = False
    

def axis_cal():
    '''
        tea
    '''
    tea = tk.Label(win,image=tea_img,font=('Time New Roman',32))
    tea.place(x=120,y=100,anchor=CENTER)

    text_tea_x = tk.Label(win,text='X:',font=('Time New Roman',32))
    text_tea_x.place(x=240,y=100,anchor=CENTER)

    add_teax = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(tea_x),width=1)
    add_teax.place(x=300,y=100,anchor=CENTER)

    ntea_x = tk.Label(win,textvariable=tea_x,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    ntea_x.place(x=400,y=100,anchor=CENTER)

    sub_teax = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(tea_x),width=1)
    sub_teax.place(x=500,y=100,anchor=CENTER)

    text_tea_y = tk.Label(win,text='Y:',font=('Time New Roman',32))
    text_tea_y.place(x=580,y=100,anchor=CENTER)

    add_teay = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(tea_y),width=1)
    add_teay.place(x=640,y=100,anchor=CENTER)

    ntea_y = tk.Label(win,textvariable=tea_y,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    ntea_y.place(x=740,y=100,anchor=CENTER)

    sub_teay = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(tea_y),width=1)
    sub_teay.place(x=840,y=100,anchor=CENTER)
    
    text_tea_z = tk.Label(win,text='Z:',font=('Time New Roman',32))
    text_tea_z.place(x=920,y=100,anchor=CENTER)

    add_teaz = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(tea_z),width=1)
    add_teaz.place(x=980,y=100,anchor=CENTER)

    ntea_z = tk.Label(win,textvariable=tea_z,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    ntea_z.place(x=1080,y=100,anchor=CENTER)

    sub_teaz = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(tea_z),width=1)
    sub_teaz.place(x=1180,y=100,anchor=CENTER)


    '''
        puff
    '''
    puf = tk.Label(win,image=puf_img,font=('Time New Roman',32))
    puf.place(x=120,y=300,anchor=CENTER)

    text_puf_x = tk.Label(win,text='X:',font=('Time New Roman',32))
    text_puf_x.place(x=240,y=300,anchor=CENTER)

    add_pufx = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(puf_x),width=1)
    add_pufx.place(x=300,y=300,anchor=CENTER)

    npuf_x = tk.Label(win,textvariable=puf_x,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    npuf_x.place(x=400,y=300,anchor=CENTER)

    sub_pufx = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(puf_x),width=1)
    sub_pufx.place(x=500,y=300,anchor=CENTER)

    text_puf_y = tk.Label(win,text='Y:',font=('Time New Roman',32))
    text_puf_y.place(x=580,y=300,anchor=CENTER)

    add_pufy = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(puf_y),width=1)
    add_pufy.place(x=640,y=300,anchor=CENTER)

    npuf_y = tk.Label(win,textvariable=puf_y,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    npuf_y.place(x=740,y=300,anchor=CENTER)

    sub_pufy = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(puf_y),width=1)
    sub_pufy.place(x=840,y=300,anchor=CENTER)
    
    text_puf_z = tk.Label(win,text='Z:',font=('Time New Roman',32))
    text_puf_z.place(x=920,y=300,anchor=CENTER)

    add_pufz = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(puf_z),width=1)
    add_pufz.place(x=980,y=300,anchor=CENTER)

    npuf_z = tk.Label(win,textvariable=puf_z,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    npuf_z.place(x=1080,y=300,anchor=CENTER)

    sub_pufz = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(puf_z),width=1)
    sub_pufz.place(x=1180,y=300,anchor=CENTER)

    '''
        egg
    '''
    egg = tk.Label(win,image=egg_img,font=('Time New Roman',32))
    egg.place(x=120,y=500,anchor=CENTER)

    text_egg_x = tk.Label(win,text='X:',font=('Time New Roman',32))
    text_egg_x.place(x=240,y=500,anchor=CENTER)

    add_eggx = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(egg_x),width=1)
    add_eggx.place(x=300,y=500,anchor=CENTER)

    negg_x = tk.Label(win,textvariable=egg_x,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    negg_x.place(x=400,y=500,anchor=CENTER)

    sub_eggx = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(egg_x),width=1)
    sub_eggx.place(x=500,y=500,anchor=CENTER)

    text_egg_y = tk.Label(win,text='Y:',font=('Time New Roman',32))
    text_egg_y.place(x=580,y=500,anchor=CENTER)

    add_eggy = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(egg_y),width=1)
    add_eggy.place(x=640,y=500,anchor=CENTER)

    negg_y = tk.Label(win,textvariable=egg_y,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    negg_y.place(x=740,y=500,anchor=CENTER)

    sub_eggy = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(egg_y),width=1)
    sub_eggy.place(x=840,y=500,anchor=CENTER)
    
    text_egg_z = tk.Label(win,text='Z:',font=('Time New Roman',32))
    text_egg_z.place(x=920,y=500,anchor=CENTER)

    add_eggz = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(egg_z),width=1)
    add_eggz.place(x=980,y=500,anchor=CENTER)

    negg_z = tk.Label(win,textvariable=egg_z,bg = '#E0E0E0',font=('Time New Roman',28),padx= 10)
    negg_z.place(x=1080,y=500,anchor=CENTER)

    sub_eggz = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(egg_z),width=1)
    sub_eggz.place(x=1180,y=500,anchor=CENTER)

    next_state = tk.Button(win,text="NEXT",font=('Time New Roman',28),command=go_next,width=5)
    next_state.place(x=640,y=620,anchor=CENTER)

    # finish = tk.Button(win,text="NEXT",font=('Time New Roman',28),command=lambda:sub(),width=3)
    # finish.place(x=740,y=700,anchor=CENTER)
    win.mainloop()


    
if __name__ == '__main__'  :
    axis_cal()