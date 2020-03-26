import sys
from tkinter import*
from tkinter import ttk
import tkinter as tk
import time
import serial 
import requests
import smbus
#======================================================================

klok=Tk()
klok.title("KLOK")
klok.geometry("1366x750")
klok.configure(background="black")

stereo=Tk()
stereo.title("stereo")
stereo.geometry("1366x750")
stereo.configure(background="black")

tb=Tk()
tb.title("TOETSENBORD")
tb.geometry("1366x750")
tb.configure(background="black")

#=======================================================================

SlaveAddress = 0x04 

I2Cbus = smbus.SMBus(1)

def ConvertStringToBytes(src): 
  converted = [] 
  for b in src: 
    converted.append(ord(b)) 
 
  return converted

def tp(key):
    bSelect = key
    BytesToSend = ConvertStringToBytes(bSelect) 
    I2Cbus.write_i2c_block_data(SlaveAddress,0x3C,BytesToSend)
    print("Sent ", SlaveAddress, " the ", bSelect, " command.")



def times():
    alarm = "21:21:30"
    kl=time.strftime("%H:%M:%S")
    clock.config(text=kl)
    clock.after(1000,times)
    if (kl == alarm):
        testData.append("<AAN1>")
        testData.append("<lichtaan>")
        runTest(testData)
        testData.clear()

def wuit():
    testData.append("<AAN1>")
    testData.append("<lichtuit>")
    runTest(testData)
    testData.clear()

def aan():
    testData.append("<lichtaan>")
    runTest(testData)
    testData.clear()
def uit():
    testData.append("<lichtuit>")
    runTest(testData)
    testData.clear()
def radioaan():
    testData.append("<AAN1>")
    runTest(testData)
    testData.clear()
def fm():
    testData.append("<FM1>")
    runTest(testData)
    testData.clear()
def eject():
    testData.append("<EJECT1>")
    runTest(testData)
    testData.clear()
def cd():
    testData.append("<CD1>")
    runTest(testData)
    testData.clear()
def usb():
    testData.append("<USB1>")
    runTest(testData)
    testData.clear()
def boven():
    testData.append("<BOVEN1>")
    runTest(testData)
    testData.clear()
def onder():
    testData.append("<ONDER1>")
    runTest(testData)
    testData.clear()
def terug():
    testData.append("<TERUG1>")
    runTest(testData)
    testData.clear()
def vooruit():
    testData.append("<VOORT1>")
    runTest(testData)
    testData.clear()
def pauze():
    testData.append("<PAUZE1>")
    runTest(testData)
    testData.clear()
def plus():
    testData.append("<PLUS1>")
    runTest(testData)
    testData.clear()
def mn():
    testData.append("<MIN1>")
    runTest(testData)
    testData.clear()
def stop():
    testData.append("<STOP1>")
    runTest(testData)
    testData.clear()
def repeat():
    testData.append("<REPEAT1>")
    runTest(testData)
    testData.clear()
def shuffle():
    testData.append("<SHUFFLE1>")
    runTest(testData)
    testData.clear()
def mute():
    testData.append("<MUTE1>")
    runTest(testData)
    testData.clear()
def prog():
    testData.append("<PROG1>")
    runTest(testData)
    testData.clear()
def sleep():
    testData.append("<SLEEP1>")
    runTest(testData)
    testData.clear()

def sendToArduino(sendStr):
    ser.write(sendStr.encode('utf-8'))


def recvFromArduino():
    global startMarker, endMarker
    
    ck = ""
    x = "z" 
    byteCount = -1 
    
    while  ord(x) != startMarker: 
        x = ser.read()
    
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode("utf-8") 
            byteCount += 1
        x = ser.read()
    
    return(ck)



def waitForArduino():
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass
        
        msg = recvFromArduino()

        print (msg)
        print ()

def runTest(td):
    numLoops = len(td)
    waitingForReply = False

    n = 0
    while n < numLoops:
        teststr = td[n]

        if waitingForReply == False:
            sendToArduino(teststr)
            print ("Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr)
            waitingForReply = True

        if waitingForReply == True:

            while ser.inWaiting() == 0:
                pass
            
            dataRecvd = recvFromArduino()
            print ("Reply Received  " + dataRecvd)
            n += 1
            waitingForReply = False

#==================================================================================


testData = []

clock=Label(klok,font=("gill sans MT",200),bg="black",fg="white")
clock.place(relx=0,rely=0.3,relwidth=1,relheight=0.5)
times()

wuit=Button(klok,bg='black',fg='white',bd=0,font=("gill sans MT",40),text='wekker uit',command=wuit)
wuit.place(relx=0,rely=0,relwidth=0.22,relheight=0.20)



weer = Frame(klok, bg='black')
weer.place(relx=0.22,rely=0,relwidth=0.78,relheight=0.2)

def format_response(weather):
    try:
       
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']

        final_str = '%s °C' % (temp)
        
    except:
        final_str = 'ERROR'

    return final_str


    weather_key = '8fdbec7500395cfb13d3c9e7344594ff'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': 'leuven', 'units': 'metric'}
    response = requests.get(url, params=params)
    weather = response.json()

    label['text'] = format_response(weather)

label = Label(weer, bg='black',fg='white',bd=0,font=("gill sans MT",90))
label.place(relwidth=0.5, relheight=1)
weather_key = '8fdbec7500395cfb13d3c9e7344594ff'
url = 'https://api.openweathermap.org/data/2.5/weather'
params = {'APPID': weather_key, 'q': 'leuven', 'units': 'metric'}
response = requests.get(url, params=params)
weather = response.json()
label['text'] = format_response(weather)
label.after(1000,times)

serPort = "/dev/ttyACM0"
baudRate = 9600
ser = serial.Serial(serPort, baudRate)
print ("Serial port " + serPort + " opened  Baudrate " + str(baudRate))

startMarker = 60
endMarker = 62


waitForArduino()

brt = 1/13
hct = 0.25
ta=0.1
r1=0
r2=0.25
r3=0.5
r4=0.75

nums=Frame(tb, bg='black')
nums.place(relx=0.77, rely=0.4, relwidth=0.2, relheight=0.5)
sps=Frame(tb, bg='black')
sps.place(relx=0.02, rely=0.8, relwidth=0.73, relheight=0.1)
mkb=Frame(tb, bg='black')
mkb.place(relx=0.02, rely=0.4, relwidth=0.73, relheight=0.4)


mt=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Esc',command = lambda: tp('31'))
mt.place(relx=0,rely=0,relwidth=0.25,relheight=0.2)
sl=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='/',command = lambda: tp('47'))
sl.place(relx=0.25,rely=0,relwidth=0.25,relheight=0.2)
ml=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='*',command = lambda: tp('42'))
ml.place(relx=0.50,rely=0,relwidth=0.25,relheight=0.2)
mn=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='-',command = lambda: tp('45'))
mn.place(relx=0.75,rely=0,relwidth=0.25,relheight=0.2)
ps=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='+',command = lambda: tp('43'))
ps.place(relx=0.75,rely=0.2,relwidth=0.25,relheight=0.4)
sev=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='7',command = lambda: tp('55'))
sev.place(relx=0,rely=0.2,relwidth=0.25,relheight=0.2)
at=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='8',command = lambda: tp('56'))
at.place(relx=0.25,rely=0.2,relwidth=0.25,relheight=0.2)
nuf=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='9',command = lambda: tp('57'))
nuf.place(relx=0.5,rely=0.2,relwidth=0.25,relheight=0.2)
vr=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='4',command = lambda: tp('52'))
vr.place(relx=0,rely=0.4,relwidth=0.25,relheight=0.2)
nf=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='5',command = lambda: tp('53'))
nf.place(relx=0.25,rely=0.4,relwidth=0.25,relheight=0.2)
zs=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='6',command = lambda: tp('54'))
zs.place(relx=0.50,rely=0.4,relwidth=0.25,relheight=0.2)
een=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='1',command = lambda: tp('49'))
een.place(relx=0,rely=0.6,relwidth=0.25,relheight=0.2)
tw=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='2',command = lambda: tp('50'))
tw.place(relx=0.25,rely=0.6,relwidth=0.25,relheight=0.2)
dr=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='3',command = lambda: tp('51'))
dr.place(relx=0.5,rely=0.6,relwidth=0.25,relheight=0.2)
ntr=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",15),text='Enter',command = lambda: tp('10'))
ntr.place(relx=0.75,rely=0.6,relwidth=0.25,relheight=0.4)
nul=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='0',command = lambda: tp('48'))
nul.place(relx=0,rely=0.8,relwidth=0.50,relheight=0.2)
pnt=Button(nums,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='.',command = lambda: tp('46'))
pnt.place(relx=0.5,rely=0.8,relwidth=0.25,relheight=0.2)



#======================

mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='[',command = lambda: tp('91'))
mt.place(relx=0,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='&',command = lambda: tp('38'))
mt.place(relx=brt*1,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=']',command = lambda: tp('93'))
mt.place(relx=brt*2,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='"',command = lambda: tp('34'))
mt.place(relx=brt*3,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="'",command = lambda: tp('39'))
mt.place(relx=brt*4,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='(',command= lambda: tp('40'))
mt.place(relx=brt*5,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='/',command= lambda: tp('47'))
mt.place(relx=brt*6,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='\\',command= lambda: tp('92'))
mt.place(relx=brt*7,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='!',command= lambda: tp('33'))
mt.place(relx=brt*8,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='?',command= lambda: tp('63'))
mt.place(relx=brt*9,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=';',command= lambda: tp('59'))
mt.place(relx=brt*10,rely=r1,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='<--',command= lambda: tp('8'))
mt.place(relx=brt*11,rely=r1,relwidth=brt*2,relheight=hct)

mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Tab',command= lambda: tp('9'))
mt.place(relx=0,rely=r2,relwidth=ta,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='a',command= lambda: tp('97'))
mt.place(relx=ta,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='z',command= lambda: tp('122'))
mt.place(relx=ta+brt,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='e',command= lambda: tp('101'))
mt.place(relx=ta+brt*2,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="r",command= lambda: tp('114'))
mt.place(relx=ta+brt*3,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='t',command= lambda: tp('116'))
mt.place(relx=ta+brt*4,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='y',command= lambda: tp('121'))
mt.place(relx=ta+brt*5,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='u',command= lambda: tp('117'))
mt.place(relx=ta+brt*6,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='i',command= lambda: tp('105'))
mt.place(relx=ta+brt*7,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='o',command= lambda: tp('111'))
mt.place(relx=ta+brt*8,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='p',command= lambda: tp('112'))
mt.place(relx=ta+brt*9,rely=r2,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Enter',command= lambda: tp('10'))
mt.place(relx=ta+brt*10,rely=r2,relwidth=0.131,relheight=hct)

ta=0.11

mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='<',command= lambda: tp('60'))
mt.place(relx=ta-brt,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='q',command= lambda: tp('113'))
mt.place(relx=ta,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='s',command= lambda: tp('115'))
mt.place(relx=ta+brt,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='d',command= lambda: tp('100'))
mt.place(relx=ta+brt*2,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="f",command= lambda: tp('102'))
mt.place(relx=ta+brt*3,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='g',command= lambda: tp('103'))
mt.place(relx=ta+brt*4,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='h',command= lambda: tp('104'))
mt.place(relx=ta+brt*5,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='j',command= lambda: tp('105'))
mt.place(relx=ta+brt*6,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='k',command= lambda: tp('107'))
mt.place(relx=ta+brt*7,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='l',command= lambda: tp('108'))
mt.place(relx=ta+brt*8,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='m',command= lambda: tp('109'))
mt.place(relx=ta+brt*9,rely=r3,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Enter',command= lambda: tp('10'))
mt.place(relx=ta+brt*10,rely=r3,relwidth=0.121,relheight=hct)

ta=0.077

mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='>',command= lambda: tp('62'))
mt.place(relx=ta,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='w',command= lambda: tp('119'))
mt.place(relx=ta+brt,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='x',command= lambda: tp('120'))
mt.place(relx=ta+brt*2,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="c",command= lambda: tp('99'))
mt.place(relx=ta+brt*3,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='v',command= lambda: tp('118'))
mt.place(relx=ta+brt*4,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='b',command= lambda: tp('98'))
mt.place(relx=ta+brt*5,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='n',command= lambda: tp('110'))
mt.place(relx=ta+brt*6,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=',',command= lambda: tp('44'))
mt.place(relx=ta+brt*7,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='.',command= lambda: tp('46'))
mt.place(relx=ta+brt*8,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=':',command= lambda: tp('58'))
mt.place(relx=ta+brt*9,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='=',command= lambda: tp('61'))
mt.place(relx=ta+brt*10,rely=r4,relwidth=brt,relheight=hct)
mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='+',command= lambda: tp('43'))
mt.place(relx=ta+brt*11,rely=r4,relwidth=brt,relheight=hct)

#============

def laag():
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='[',command = lambda: tp('91'))
    mt.place(relx=0,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='&',command = lambda: tp('38'))
    mt.place(relx=brt*1,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=']',command = lambda: tp('93'))
    mt.place(relx=brt*2,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='"',command = lambda: tp('34'))
    mt.place(relx=brt*3,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="'",command = lambda: tp('39'))
    mt.place(relx=brt*4,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='(',command= lambda: tp('40'))
    mt.place(relx=brt*5,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='/',command= lambda: tp('47'))
    mt.place(relx=brt*6,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='\\',command= lambda: tp('92'))
    mt.place(relx=brt*7,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='!',command= lambda: tp('33'))
    mt.place(relx=brt*8,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='?',command= lambda: tp('63'))
    mt.place(relx=brt*9,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=';',command= lambda: tp('59'))
    mt.place(relx=brt*10,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='<--',command= lambda: tp('8'))
    mt.place(relx=brt*11,rely=r1,relwidth=brt*2,relheight=hct)
    ta=0.1
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Tab',command= lambda: tp('9'))
    mt.place(relx=0,rely=r2,relwidth=ta,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='a',command= lambda: tp('97'))
    mt.place(relx=ta,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='z',command= lambda: tp('122'))
    mt.place(relx=ta+brt,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='e',command= lambda: tp('101'))
    mt.place(relx=ta+brt*2,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="r",command= lambda: tp('114'))
    mt.place(relx=ta+brt*3,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='t',command= lambda: tp('116'))
    mt.place(relx=ta+brt*4,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='y',command= lambda: tp('121'))
    mt.place(relx=ta+brt*5,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='u',command= lambda: tp('117'))
    mt.place(relx=ta+brt*6,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='i',command= lambda: tp('105'))
    mt.place(relx=ta+brt*7,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='o',command= lambda: tp('111'))
    mt.place(relx=ta+brt*8,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='p',command= lambda: tp('112'))
    mt.place(relx=ta+brt*9,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Enter',command= lambda: tp('10'))
    mt.place(relx=ta+brt*10,rely=r2,relwidth=0.131,relheight=hct)
    ta=0.11
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='<',command= lambda: tp('60'))
    mt.place(relx=ta-brt,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='q',command= lambda: tp('113'))
    mt.place(relx=ta,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='s',command= lambda: tp('115'))
    mt.place(relx=ta+brt,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='d',command= lambda: tp('100'))
    mt.place(relx=ta+brt*2,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="f",command= lambda: tp('102'))
    mt.place(relx=ta+brt*3,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='g',command= lambda: tp('103'))
    mt.place(relx=ta+brt*4,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='h',command= lambda: tp('104'))
    mt.place(relx=ta+brt*5,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='j',command= lambda: tp('105'))
    mt.place(relx=ta+brt*6,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='k',command= lambda: tp('107'))
    mt.place(relx=ta+brt*7,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='l',command= lambda: tp('108'))
    mt.place(relx=ta+brt*8,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='m',command= lambda: tp('109'))
    mt.place(relx=ta+brt*9,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Enter',command= lambda: tp('10'))
    mt.place(relx=ta+brt*10,rely=r3,relwidth=0.121,relheight=hct)
    ta=0.077
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='>',command= lambda: tp('62'))
    mt.place(relx=ta,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='w',command= lambda: tp('119'))
    mt.place(relx=ta+brt,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='x',command= lambda: tp('120'))
    mt.place(relx=ta+brt*2,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="c",command= lambda: tp('99'))
    mt.place(relx=ta+brt*3,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='v',command= lambda: tp('118'))
    mt.place(relx=ta+brt*4,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='b',command= lambda: tp('98'))
    mt.place(relx=ta+brt*5,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='n',command= lambda: tp('110'))
    mt.place(relx=ta+brt*6,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=',',command= lambda: tp('44'))
    mt.place(relx=ta+brt*7,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='.',command= lambda: tp('46'))
    mt.place(relx=ta+brt*8,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text=':',command= lambda: tp('58'))
    mt.place(relx=ta+brt*9,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='=',command= lambda: tp('61'))
    mt.place(relx=ta+brt*10,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='+',command= lambda: tp('43'))
    mt.place(relx=ta+brt*11,rely=r4,relwidth=brt,relheight=hct)

#============
def hoog():
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='%',command = lambda: tp('37'))
    mt.place(relx=0,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='1',command = lambda: tp('49'))
    mt.place(relx=brt*1,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='2',command = lambda: tp('50'))
    mt.place(relx=brt*2,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='3',command = lambda: tp('51'))
    mt.place(relx=brt*3,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="4",command = lambda: tp('52'))
    mt.place(relx=brt*4,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='5',command= lambda: tp('53'))
    mt.place(relx=brt*5,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='6',command= lambda: tp('54'))
    mt.place(relx=brt*6,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='7',command= lambda: tp('55'))
    mt.place(relx=brt*7,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='8',command= lambda: tp('56'))
    mt.place(relx=brt*8,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='9',command= lambda: tp('57'))
    mt.place(relx=brt*9,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='0',command= lambda: tp('48'))
    mt.place(relx=brt*10,rely=r1,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='<--',command= lambda: tp('8'))
    mt.place(relx=brt*11,rely=r1,relwidth=brt*2,relheight=hct)
    ta=0.1
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Tab',command= lambda: tp('9'))
    mt.place(relx=0,rely=r2,relwidth=ta,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='A',command= lambda: tp('65'))
    mt.place(relx=ta,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Z',command= lambda: tp('90'))
    mt.place(relx=ta+brt,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='E',command= lambda: tp('69'))
    mt.place(relx=ta+brt*2,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="R",command= lambda: tp('82'))
    mt.place(relx=ta+brt*3,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='T',command= lambda: tp('84'))
    mt.place(relx=ta+brt*4,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Y',command= lambda: tp('89'))
    mt.place(relx=ta+brt*5,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='U',command= lambda: tp('85'))
    mt.place(relx=ta+brt*6,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='I',command= lambda: tp('73'))
    mt.place(relx=ta+brt*7,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='O',command= lambda: tp('79'))
    mt.place(relx=ta+brt*8,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='P',command= lambda: tp('80'))
    mt.place(relx=ta+brt*9,rely=r2,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Enter',command= lambda: tp('10'))
    mt.place(relx=ta+brt*10,rely=r2,relwidth=0.131,relheight=hct)
    ta=0.11
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='{',command= lambda: tp('123'))
    mt.place(relx=ta-brt,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Q',command= lambda: tp('81'))
    mt.place(relx=ta,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='S',command= lambda: tp('83'))
    mt.place(relx=ta+brt,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='D',command= lambda: tp('68'))
    mt.place(relx=ta+brt*2,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="F",command= lambda: tp('70'))
    mt.place(relx=ta+brt*3,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='G',command= lambda: tp('71'))
    mt.place(relx=ta+brt*4,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='H',command= lambda: tp('72'))
    mt.place(relx=ta+brt*5,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='J',command= lambda: tp('74'))
    mt.place(relx=ta+brt*6,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='K',command= lambda: tp('75'))
    mt.place(relx=ta+brt*7,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='L',command= lambda: tp('76'))
    mt.place(relx=ta+brt*8,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='M',command= lambda: tp('77'))
    mt.place(relx=ta+brt*9,rely=r3,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='Enter',command= lambda: tp('10'))
    mt.place(relx=ta+brt*10,rely=r3,relwidth=0.121,relheight=hct)
    ta=0.077
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='}',command= lambda: tp('125'))
    mt.place(relx=ta,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='W',command= lambda: tp('87'))
    mt.place(relx=ta+brt,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='X',command= lambda: tp('88'))
    mt.place(relx=ta+brt*2,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text="C",command= lambda: tp('67'))
    mt.place(relx=ta+brt*3,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='V',command= lambda: tp('86'))
    mt.place(relx=ta+brt*4,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='B',command= lambda: tp('66'))
    mt.place(relx=ta+brt*5,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='N',command= lambda: tp('78'))
    mt.place(relx=ta+brt*6,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='#',command= lambda: tp('35'))
    mt.place(relx=ta+brt*7,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='@',command= lambda: tp('64'))
    mt.place(relx=ta+brt*8,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='*',command= lambda: tp('42'))
    mt.place(relx=ta+brt*9,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='=',command= lambda: tp('61'))
    mt.place(relx=ta+brt*10,rely=r4,relwidth=brt,relheight=hct)
    mt=Button(mkb,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='-',command= lambda: tp('45'))
    mt.place(relx=ta+brt*11,rely=r4,relwidth=brt,relheight=hct)

#============

mt=Button(sps,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='',command= lambda: tp('32'))
mt.place(relx=0.26,rely=0,relwidth=0.45,relheight=1)
mt=Button(sps,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='a',command=laag)
mt.place(relx=0,rely=0,relwidth=0.13,relheight=1)
mt=Button(sps,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='A',command=hoog)
mt.place(relx=0.13,rely=0,relwidth=0.13,relheight=1)

#======================

ran=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='stereo aan/uit',command=radioaan)
ran.place(relx=0.01,rely=0,relwidth=0.22,relheight=0.20)
lan=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='licht aan',command=aan)
lan.place(relx=0.01,rely=0.8,relwidth=0.11,relheight=0.20)
lut=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='licht uit',command=uit)
lut.place(relx=0.12,rely=0.8,relwidth=0.11,relheight=0.20)
fm=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='FM',command=fm)
fm.place(relx=0.25,rely=0.2,relwidth=0.11,relheight=0.20)
cd=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='cd',command=cd)
cd.place(relx=0.25,rely=0.4,relwidth=0.11,relheight=0.20)
usb=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='usb/aux',command=usb)
usb.place(relx=0.25,rely=0.6,relwidth=0.11,relheight=0.20)

boven=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='boven',command=boven)
boven.place(relx=0.48,rely=0.2,relwidth=0.11,relheight=0.20)
onder=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='onder',command=onder)
onder.place(relx=0.48,rely=0.6,relwidth=0.11,relheight=0.20)
terug=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='terug',command=terug)
terug.place(relx=0.37,rely=0.4,relwidth=0.11,relheight=0.20)
vooruit=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='vooruit',command=vooruit)
vooruit.place(relx=0.59,rely=0.4,relwidth=0.11,relheight=0.20)
pp=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='play/pauze',command=pauze)
pp.place(relx=0.48,rely=0.4,relwidth=0.11,relheight=0.20)

plus=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='plus',command=plus)
plus.place(relx=0.01,rely=0.30,relwidth=0.11,relheight=0.20)
mn=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='min',command=mn)
mn.place(relx=0.01,rely=0.50,relwidth=0.11,relheight=0.20)


rpt=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='repeat',command=repeat)
rpt.place(relx=0.13,rely=0.30,relwidth=0.11,relheight=0.20)
sfl=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='shuffle',command=shuffle)
sfl.place(relx=0.13,rely=0.50,relwidth=0.11,relheight=0.20)

stp=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='stop',command=stop)
stp.place(relx=0.71,rely=0.30,relwidth=0.11,relheight=0.20)
ej=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='eject',command=eject)
ej.place(relx=0.71,rely=0.50,relwidth=0.11,relheight=0.20)

mute=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='mute',command=mute)
mute.place(relx=0.83,rely=0.2,relwidth=0.11,relheight=0.20)
prog=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='prog',command=prog)
prog.place(relx=0.83,rely=0.4,relwidth=0.11,relheight=0.20)
sleep=Button(stereo,bg='black',fg='white',bd=0,font=("gill sans MT",20),text='sleep',command=sleep)
sleep.place(relx=0.83,rely=0.6,relwidth=0.11,relheight=0.20)

ser.close

#==================================================================================

klok.mainloop()
stereo.mainloop()
tb.mainloop()