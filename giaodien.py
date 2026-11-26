from tkinter import *
import tkinter.messagebox 
import threading
import time
import serial
from tkinter import font, Label
import kinematicrobot


try:
    user = serial.Serial("COM3",115200,timeout=0.01)
    time.sleep(2)
    print("Đã kết nối với port")
except serial.SerialException as a:
    user = None
    print("không thể kết nối với port: ",a)

giaodien = Tk()
giaodien.title("Giao diện điều khiển cánh tay Robot 3 bậc tự do")
giaodien.geometry("1100x630")
giaodien.resizable(False,False)
giaodien.configure(background="lavender")
theta1=0
theta2=0
theta3=0
Px = 0
Py = 0
Pz = 0
theta1_max = 90
theta1_min = -90
theta2_max = 90
theta2_min = -70
theta3_max = 100
theta3_min = -100
def fc_slider_theta1(x):
    display_theta1_slider.delete(0,END)
    theta1=slider_theta1.get()
    display_theta1_slider.insert(0,theta1)
    return theta1
def fc_slider_theta2(x):
    display_theta2_slider.delete(0,END)
    theta2=slider_theta2.get()
    display_theta2_slider.insert(0,theta2)
    return theta2
def fc_slider_theta3(x):
    display_theta3_slider.delete(0,END)
    theta3=slider_theta3.get()
    display_theta3_slider.insert(0,theta3)
    return theta3

def fc_btn_settheta1():
    theta1 = float(display_theta1_slider.get())
    slider_theta1.set(theta1)
    Donghocthuan(theta1)
def fc_btn_settheta2():
    theta2 = float(display_theta2_slider.get())
    slider_theta2.set(theta2)
    Donghocthuan(theta2)
def fc_btn_settheta3():
    theta3 = float(display_theta3_slider.get())
    slider_theta3.set(theta3)
    Donghocthuan(theta3)


def Donghocthuan(x):
    display_Px.delete(0,END)
    display_Py.delete(0,END)
    display_Pz.delete(0,END)
    theta1 = fc_slider_theta1(x)
    theta2 = fc_slider_theta2(x)
    theta3 = fc_slider_theta3(x)
    mang = kinematicrobot.forward_kinematic(theta1,theta2,theta3)
    Px = mang[0]
    Py = mang[1]
    Pz = mang[2]
    display_Px.insert(0,Px)
    display_Py.insert(0,Py)
    display_Pz.insert(0,Pz)


def Donghocnghich():
    display_theta11.delete(0,END)
    display_theta21.delete(0,END)
    display_theta31.delete(0,END)
    display_theta12.delete(0,END)
    display_theta22.delete(0,END)
    display_theta32.delete(0,END)
    Px = float(display_Px_nghich.get())
    Py = float(display_Py_nghich.get())
    Pz = float(display_Pz_nghich.get())
    mang = kinematicrobot.inverse_kinematic(Px,Py,Pz)
    if((mang == None) or (Pz < 0) ):
        tkinter.messagebox.showerror("CẢNH BÁO","VỊ TRÍ NÀY NGOÀI VÙNG LÀM VIỆC VUI LÒNG CHỌN LẠI VỊ TRÍ KHÁC")
    else:
        theta1 = mang[0]
        theta21 = mang[1]
        theta31 = mang[2]
        theta22 = mang[3]
        theta32 = mang[4]
        display_theta11.insert(0,theta1)
        display_theta21.insert(0,theta21)
        display_theta31.insert(0,theta31)
        display_theta12.insert(0,theta1)
        display_theta22.insert(0,theta22)
        display_theta32.insert(0,theta32)

def fc_run_donghocnghich():
    nghiem = value_inside.get()
    if(nghiem == "NGHIỆM 1"):
        theta11 = float(display_theta11.get())
        theta21 = float(display_theta21.get())
        theta31 = float(display_theta31.get())
        if(abs(theta11) > 90 or theta21 > theta2_max or theta21 < theta2_min or abs(theta31)>100):
            tkinter.messagebox.showerror("NGOÀI VÙNG LÀM VIỆC THỰC TẾ","VUI LÒNG CHỌN NGHIỆM 2")
        else:
            data = f"F{theta11}A{theta21}B{theta31}C"
            user.write(data.encode())
    elif( nghiem== "NGHIỆM 2"):
        theta12 = float(display_theta12.get())
        theta22 = float(display_theta22.get())
        theta32 = float(display_theta32.get())
        if(abs(theta12) > 90 or theta22 > theta2_max or theta22 < theta2_min or abs(theta32)>100):
            tkinter.messagebox.showerror("NGOÀI VÙNG LÀM VIỆC THỰC TẾ","VUI LÒNG CHỌN NGHIỆM 1")
        else:
            data = f"F{theta12}A{theta22}B{theta32}C"
            user.write(data.encode())
    else:
        print("vui lòng chọn nghiệm")

def fc_run_donghocthuan():
    theta1 = float(display_theta1_slider.get())
    theta2 = float(display_theta2_slider.get())
    theta3 = float(display_theta3_slider.get())
    data = f"F{theta1}A{theta2}B{theta3}C"
    user.write(data.encode())

def fc_sethome():
    data = "S"
    user.write(data.encode())
def fc_stop():
    data = "O"
    user.write(data.encode())

def fc_A1():
    theta1 = 17.745
    theta2 = -34.038
    theta3 = -50.513
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A2():
    theta1 = 6.843
    theta2 = -34.633
    theta3 = -53.648
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A3():
    theta1 = -5.711
    theta2 = -34.626
    theta3 = -53.868
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A4():
    theta1 = -17.745
    theta2 = -34.96
    theta3 = -49.025
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A5():
    theta1 = 19.654
    theta2 = -36.162
    theta3 = -62.194
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A6():
    theta1 = 4.899
    theta2 = -37.416
    theta3 = -64.862
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A7():
    theta1 = -9.462
    theta2 = -36.861
    theta3 = -64.957
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A8():
    theta1 = -20.931
    theta2 = -35.353
    theta3 = -60.74
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A9():
    theta1 =  20.95
    theta2 = -40.606
    theta3 = -68.704
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A10():
    theta1 = 3.366
    theta2 = -43.005
    theta3 = -71.484
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A11():
    theta1 = -11.502
    theta2 = -42.218
    theta3 = -70.716
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A12():
    theta1 = -27.745
    theta2 = -38.92
    theta3 = -68.364
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())


def fc_A13():
    theta1 = 22.166
    theta2 = -46.02
    theta3 = -76.537
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A14():
    theta1 = 2.309
    theta2 = -50.575
    theta3 = -77.635
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A15():
    theta1 = -17.103
    theta2 = -47.995
    theta3 = -77.173
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_A16():
    theta1 = -34.086
    theta2 = -44.252
    theta3 = -73.328
    data = f"F{theta1}A{theta2}B{theta3}C"  
    user.write(data.encode())

def fc_box():
    theta1 = 48.576
    theta2 = -11.877
    theta3 = -98.759
    data = f"F{theta1}A{theta2}B{theta3}C" 
    user.write(data.encode())
def hutnamcham():
    data = "H"
    user.write(data.encode())
def thanamcham():
    data = "T"
    user.write(data.encode())

def read_serial():
    while(user.in_waiting):
        data = user.readline().decode("utf-8", errors="ignore").strip()
        if data.startswith("khop 1:"):
            display_theta1_sensor.delete(0,END)
            value = data.split(' ')
            theta1_sensor = float(value[2])
            display_theta1_sensor.insert(0,theta1_sensor)
        elif data.startswith("khop 2:"):
            display_theta2_sensor.delete(0,END)
            value = data.split(' ')
            theta2_sensor = float(value[2])
            display_theta2_sensor.insert(0,theta2_sensor)
        elif data.startswith("khop 3:"):
            display_theta3_sensor.delete(0,END)
            value = data.split(' ')
            theta3_sensor = float(value[2])
            display_theta3_sensor.insert(0,theta3_sensor)
    giaodien.after(20,read_serial)

###### GIAO DIEN BANG DIEU KHIEN

Label(giaodien,text="BẢNG ĐIỀU KHIỂN",background="ghostwhite",font=("Arial",25,font.BOLD),fg="blue").pack()

#### GIAO DIEN DONG HOC THUAN
Label(giaodien,text="ĐỘNG HỌC THUẬN",background="ghostwhite",font=("arial",15,font.BOLD),fg="RED").place(x=150,y=50)

## Hien thi thanh cuon theta1
slider_theta1 = Scale(giaodien,orient="horizontal",from_=-90,to=90,width=15,resolution=0.25,length=320,command=Donghocthuan)
slider_theta1.place(x=80,y=100)
slider_theta1.set(theta1)
display_theta1_slider = Entry(giaodien,width=5,font=("arial",12,font.BOLD))
display_theta1_slider.insert(0,theta1)
display_theta1_slider.place(x=430,y=115)
Label(giaodien,text="Theta1",background="ghostwhite",font=("Arial",12,font.BOLD),fg="olive").place(x=427,y=85)
btn_settheta1 = Button(giaodien,text="Set Theta1",background="dodgerblue",font=("Arial",12,font.BOLD),fg="red",command=fc_btn_settheta1)
btn_settheta1.place(x=500,y=105)


## Hien thi thanh cuon theta2
slider_theta2 = Scale(giaodien,orient="horizontal",from_=-70,to=90,width=15,resolution=0.25,length=320,command=Donghocthuan)
slider_theta2.place(x=80,y=170)
slider_theta2.set(theta2)
display_theta2_slider = Entry(giaodien,width=5,font=("arial",12,font.BOLD))
display_theta2_slider.insert(0,theta2)
display_theta2_slider.place(x=430,y=185)
Label(giaodien,text="Theta2",background="ghostwhite",font=("Arial",12,font.BOLD),fg="olive").place(x=427,y=155)
btn_settheta2 = Button(giaodien,text="Set Theta2",background="dodgerblue",font=("Arial",12,font.BOLD),fg="red",command=fc_btn_settheta2)
btn_settheta2.place(x=500,y=170)


## Hien thi thanh cuon theta3
slider_theta3 = Scale(giaodien,orient="horizontal",from_=-100,to=100,width=15,resolution=0.25,length=320,command=Donghocthuan)
slider_theta3.place(x=80,y=240)
slider_theta3.set(theta3)
display_theta3_slider = Entry(giaodien,width=5,font=("arial",12,font.BOLD))
display_theta3_slider.insert(0,theta3)
display_theta3_slider.place(x=430,y=255)
Label(giaodien,text="Theta3",background="ghostwhite",font=("Arial",12,font.BOLD),fg="olive").place(x=427,y=225)
btn_settheta3 = Button(giaodien,text="Set Theta3",background="dodgerblue",font=("Arial",12,font.BOLD),fg="red",command=fc_btn_settheta3)
btn_settheta3.place(x=500,y=240)

## Hien thi Px
Label(giaodien,text="Px",font=("arial",12,font.BOLD),background="ghostwhite",fg="blue").place(x=80,y=290)
display_Px = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_Px.place(x=70,y=315)
## Hien thi Py
Label(giaodien,text="Py",font=("arial",12,font.BOLD),background="ghostwhite",fg="blue").place(x=230,y=290)
display_Py = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_Py.place(x=220,y=315)
## Hien thi Pz
Label(giaodien,text="Pz",font=("arial",12,font.BOLD),background="ghostwhite",fg="blue").place(x=380,y=290)
display_Pz = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_Pz.place(x=370,y=315)

#### CHAY DONG HOC THUAN
run_donghocthuan = Button(giaodien,text="CHẠY ĐỘNG HỌC THUẬN",background="peru",font=("Arial",12,font.BOLD),fg="white",command=fc_run_donghocthuan)
run_donghocthuan.place(x=450,y=305)

#### GIAO DIEN DONG HOC NGHICH
Label(giaodien,text="ĐỘNG HỌC NGHỊCH",background="ghostwhite",font=("arial",15,font.BOLD),fg="RED").place(x=150,y=370)

Label(giaodien,text="Px",font=("arial",12,font.BOLD),background="ghostwhite",fg="blue").place(x=60,y=450)
display_Px_nghich = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_Px_nghich.place(x=90,y=450)
Label(giaodien,text="Py",font=("arial",12,font.BOLD),background="ghostwhite",fg="blue").place(x=60,y=500)
display_Py_nghich = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_Py_nghich.place(x=90,y=500)
Label(giaodien,text="Pz",font=("arial",12,font.BOLD),background="ghostwhite",fg="blue").place(x=60,y=550)
display_Pz_nghich = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_Pz_nghich.place(x=90,y=550)

## NGHIEM 1
Label(giaodien,text="NGHIỆM 1",font=("arial",12,font.BOLD),background="ghostwhite",fg="blueviolet").place(x=230,y=410)
Label(giaodien,text="Theta1",font=("arial",12,font.BOLD),background="ghostwhite",fg="olive").place(x=200,y=448)
display_theta11 = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_theta11.place(x=260,y=448)
Label(giaodien,text="Theta2",font=("arial",12,font.BOLD),background="ghostwhite",fg="olive").place(x=200,y=500)
display_theta21 = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_theta21.place(x=260,y=500)
Label(giaodien,text="Theta3",font=("arial",12,font.BOLD),background="ghostwhite",fg="olive").place(x=200,y=550)
display_theta31 = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_theta31.place(x=260,y=550)

## NGHIEM 2
Label(giaodien,text="NGHIỆM 2",font=("arial",12,font.BOLD),background="ghostwhite",fg="deeppink").place(x=400,y=410)
Label(giaodien,text="Theta1",font=("arial",12,font.BOLD),background="ghostwhite",fg="olive").place(x=370,y=448)
display_theta12 = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_theta12.place(x=430,y=448)
Label(giaodien,text="Theta2",font=("arial",12,font.BOLD),background="ghostwhite",fg="olive").place(x=370,y=500)
display_theta22 = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_theta22.place(x=430,y=500)
Label(giaodien,text="Theta3",font=("arial",12,font.BOLD),background="ghostwhite",fg="olive").place(x=370,y=550)
display_theta32 = Entry(giaodien,width=7,font=("arial",12,font.BOLD))
display_theta32.place(x=430,y=550)

#### GIAI
btn_solve = Button(giaodien,text="SOLVE",background="black",font=("Arial",12,font.BOLD),fg="white",command=Donghocnghich)
btn_solve.place(x=530,y=530)

#### SETHOME
sethome = Button(giaodien,text="SETHOME",background="purple",font=("Arial",12,font.BOLD),fg="white",command=fc_sethome)
sethome.place(x=740,y=400)
#### STOP
stop = Button(giaodien,text="STOP",width=8,background="red",font=("Arial",12,font.BOLD),fg="black",command=fc_stop)
stop.place(x=870,y=400)
#### HUT NAM CHAM
hut = Button(giaodien,text="HÚT",background="slategray",font=("Arial",12,font.BOLD),fg="white",command=hutnamcham)
hut.place(x=780,y=470)
#### THA NAM CHAM
tha = Button(giaodien,text="THẢ",background="slategray",font=("Arial",12,font.BOLD),fg="white",command=thanamcham)
tha.place(x=890,y=470)

#### Lua chon nghiem
options = ["NGHIỆM 1","NGHIỆM 2"]
value_inside = StringVar(giaodien)
value_inside.set("LỰA CHỌN NGHIỆM")
question_menu = OptionMenu(giaodien,value_inside,*options)
question_menu.place(x=530,y=400)
#### CHAY DONG HOC NGHICH
run_donghocnghich = Button(giaodien,text="CHẠY ĐỘNG HỌC NGHỊCH",background="orange",font=("Arial",12,font.BOLD),fg="white",command=fc_run_donghocnghich)
run_donghocnghich.place(x=520,y=470)

##### GOC DOC TU CAM BIEN
Label(giaodien,text="GÓC ĐỌC TỪ CẢM BIẾN",font=("arial",15,font.BOLD),background="ghostwhite",fg="brown").place(x=600,y=50)
Label(giaodien,text="Theta1",background="ghostwhite",font=("Arial",12,font.BOLD),fg="olive").place(x=680,y=85)
display_theta1_sensor = Entry(giaodien,width=6,font=("arial",12,font.BOLD))
display_theta1_sensor.place(x=680,y=115)
Label(giaodien,text="Theta2",background="ghostwhite",font=("Arial",12,font.BOLD),fg="olive").place(x=680,y=155)
display_theta2_sensor = Entry(giaodien,width=6,font=("arial",12,font.BOLD))
display_theta2_sensor.place(x=680,y=185)
Label(giaodien,text="Theta3",background="ghostwhite",font=("Arial",12,font.BOLD),fg="olive").place(x=680,y=225)
display_theta3_sensor = Entry(giaodien,width=6,font=("arial",12,font.BOLD))
display_theta3_sensor.place(x=680,y=255)
######## RUN THUC TE
a1 = Button(giaodien,text="A1",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A1)
a1.place(x=830,y=100)
a2 = Button(giaodien,text="A2",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A2)
a2.place(x=890,y=100)
a3 = Button(giaodien,text="A3",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A3)
a3.place(x=950,y=100)
a4 = Button(giaodien,text="A4",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A4)
a4.place(x=1010,y=100)
a5 = Button(giaodien,text="A5",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A5)
a5.place(x=830,y=160)
a6 = Button(giaodien,text="A6",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A6)
a6.place(x=890,y=160)
a7 = Button(giaodien,text="A7",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A7)
a7.place(x=950,y=160)
a8 = Button(giaodien,text="A8",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A8)
a8.place(x=1010,y=160)
a9 = Button(giaodien,text="A9",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A9)
a9.place(x=830,y=220)
a10 = Button(giaodien,text="A10",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A10)
a10.place(x=890,y=220)
a11 = Button(giaodien,text="A11",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A11)
a11.place(x=950,y=220)
a12 = Button(giaodien,text="A12",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A12)
a12.place(x=1010,y=220)
a13 = Button(giaodien,text="A13",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A13)
a13.place(x=830,y=280)
a14 = Button(giaodien,text="A14",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A14)
a14.place(x=890,y=280)
a15 = Button(giaodien,text="A15",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A15)
a15.place(x=950,y=280)
a16 = Button(giaodien,text="A16",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_A16)
a16.place(x=1010,y=280)
box = Button(giaodien,text="BOX",background="lime",font=("Arial",12,font.BOLD),fg="black",width=3,command=fc_box)
box.place(x=920,y=340)
giaodien.after(20,read_serial)
giaodien.mainloop()