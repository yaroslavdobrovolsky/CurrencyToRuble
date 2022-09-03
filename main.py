from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import re

def currensyRB():
    nameList = ['EUR', "USD", 'JPY', 'BYN', 'BTC', 'ETH']
    global currencyName
    if currencyVAR.get() <4:
        text["text"] = f"1 {nameList[currencyVAR.get()]} = {course(currencyName[currencyVAR.get()], 'phys')} RUB"
    elif currencyVAR.get() >= 4:
        text["text"] = f"1 {nameList[currencyVAR.get()]} = {course(currencyName[currencyVAR.get()], 'crypto')} RUB"
    
def course(curren, type):
    if type == "phys":
        url = f"https://www.google.com/search?q=course+{curren}+to+ruble"
    elif type == "crypto":
        url = f"https://www.coinbase.com/ru/converter/{curren}/rub"
        
    page = requests.get(url, headers = {'user-agent': 'my-app/0.0.1'})
    
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        
        if type == "phys":
            rublestr = str(soup.find("td", class_="sjsZvd s5aIid OE1use"))
        elif type == "crypto":
            rublestr = str(soup.find("div", class_="cds-flex-f1g67tkn cds-column-ci8mx7v"))
            
        ruble = rublestr.replace('<td class="sjsZvd s5aIid OE1use"><div class="hfgVwf"><div class="BNeawe s3v9rd AP7Wnd">','')
        ruble = ruble.replace("</div></div></td>", '')
        ruble = ruble.replace("RUB", '')
        ruble = ruble.replace("</h2></div>", '')
        if type == "crypto":
            ruble = ruble[:-1:]
        ruble = re.sub("₽", "", ruble)
        ruble = ruble.replace('<div class="cds-flex-f1g67tkn cds-column-ci8mx7v" style="flex-basis:0;flex-grow:1;flex-shrink:1"><h1 class="cds-typographyResets-t1xhpuq2 cds-display1-du4t46c cds-foreground-f1yzxzgu cds-transition-txjiwsi cds-start-s1muvu8a">Из Ethereum в Российский рубль</h1><h2 class="cds-typographyResets-t1xhpuq2 cds-title2-t37r1y cds-foregroundMuted-f1vw1sy6 cds-transition-txjiwsi cds-start-s1muvu8a cds-2-_1xqs9y8 cds-1-_18ml2at">1 ETH = ', '')
        ruble = ruble.replace('<div class="cds-flex-f1g67tkn cds-column-ci8mx7v" style="flex-basis:0;flex-grow:1;flex-shrink:1"><h1 class="cds-typographyResets-t1xhpuq2 cds-display1-du4t46c cds-foreground-f1yzxzgu cds-transition-txjiwsi cds-start-s1muvu8a">Из Bitcoin в Российский рубль</h1><h2 class="cds-typographyResets-t1xhpuq2 cds-title2-t37r1y cds-foregroundMuted-f1vw1sy6 cds-transition-txjiwsi cds-start-s1muvu8a cds-2-_1xqs9y8 cds-1-_18ml2at">1 BTC = ','')
        ruble = ruble.replace(",", ".")
        whitespace = r"\s+"
        ruble = re.sub(whitespace, "", ruble)
    else:
        messagebox.showerror(f"ERROR {page.status_code}", f"ERROR {page.status_code}")

    return float(ruble)

def calc():
    global currencyName
    if currencyVAR.get() <4:
        equalsText["text"] = f"{round(course(currencyName[currencyVAR.get()], 'phys')*float(value_entry.get()), 4)} RUB"
    if currencyVAR.get() >= 4:
        equalsText["text"] = f"{round(course(currencyName[currencyVAR.get()], 'crypto')*float(value_entry.get()), 4)} RUB"

root = Tk()
root.iconbitmap("favicon.ico")
root.minsize(350, 100)
root.maxsize(350, 100)
root.title("CTR")

currencyName = ['Euro', 'Dollar', 'Yen', 'Bel.Ruble', 'BTC', 'ETH']

currencyVAR = IntVar()
currencyVAR.set(0)
xVAR = IntVar()
xVAR.set(1)

text = Label()
text["text"] = f"1 EUR = {course('euro', 'phys')} RUB"
text.grid(column=1)

value_entry = Entry(textvariable=xVAR, width=8)
value_entry.place(relx=0.45, rely=0)

equalsButton = Button(text="=", command=calc)
equalsButton.place(relx=0.615, rely=0)

equalsText = Label(text=f"{round(course('euro', 'phys')*float(value_entry.get()), 4)} RUB")
equalsText.place(relx=0.72-0.05, rely=0)

for i in range(0, 6):
    exec(f'r{i} = Radiobutton(text=currencyName[i], variable=currencyVAR, value=i, command=currensyRB)')
    if i == 0:
        r0.place(relx=0, rely=0.25)
    elif i == 1:
        r1.place(relx=0, rely=0.55)
    elif i == 2:
        r2.place(relx=0.356, rely=0.25)
    elif i == 3:
        r3.place(relx=0.356, rely=0.55)
    elif i == 4:
        r4.place(relx=0.75, rely=0.25)
    if i == 5:
        r5.place(relx=0.75, rely=0.55)

root.mainloop()