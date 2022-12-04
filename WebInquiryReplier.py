import pandas
from tkinter import *
import tkinter
import tkinter.filedialog
import win32com.client as win32
def GetFileDir():
    return "./files/"

def GetFileName():
    return "WebInqOct.csv"

def GetFile():
    return GetFileDir() + GetFileName()

def GenerateEmail(GenerateFile = False):
    df = getEmail(False)
    outDf = pandas.DataFrame()
    emailAddresses = []
    emailMsgs = []
    emailTitles = []
    for i in range(0, len(df)):
        firstName = df["first names"][i]
        lastName = df["last names"][i]
        email = df["emails"][i]
        emailAddresses.append(email)
        msg = f"""Dear {firstName},\n
        
This is Professor Li, director of the Master of Game Development program. Thanks for your interest in the program.\n
If you have any questions about the program, please do not hesitate to reply to this email directly, and I am more than happy to answer them.\n
        
Thank you!\n
JT
"""
        emailMsgs.append(msg)
        emailTitles.append("Inquiry about the Master of Game Development Program")

    outDf["Addresses"] = emailAddresses
    outDf["emailTitles"] = emailTitles
    outDf["messages"] = emailMsgs
    if GenerateFile:
        outDf.to_csv("./files/emailMsg.csv", index=False)
    return outDf

def getEmail(generateFile = True):
    df = pandas.read_csv(GetFile())

    outDf = pandas.DataFrame()

    firstNames = ["Jingtian"]
    lastNames = ["Li"]
    emails = ["jingtianli.animation@gmail.com"]

    for item in df.Body:
        allWords = item.split(' ')
        name = []
        for word in allWords:
            if "has" in word:
                if "\u2009" in word:
                    name.append(word.split("\u2009")[0])
                break
            name.append(word)

        email = ""
        for i in range(0, len(allWords)):
            if "Email:" in allWords[i]:
                email = allWords[i+1][:-7]

        firstNames.append(name[0])

        name.reverse()
        for i in name:
            if i != "" and i != "III" and i != "Jr" and i != "II" and i != "I":
                lastNames.append(i)
                break

        emails.append(email)

    outDf["first names"] = firstNames
    outDf["last names"] = lastNames
    outDf["emails"] = emails

    if generateFile:
        outDf.to_csv("./files/nameEmail.csv", index=False, mode='a')

    return outDf

def getPhone():
    df = pandas.read_csv(GetFile())

    outDf = pandas.DataFrame()

    firstNames = []
    lastNames = []
    phones = []

    for item in df.Body:
        allWords = item.split(' ')
        name = []
        for word in allWords:
            if "has" in word:
                if "\u2009" in word:
                    name.append(word.split("\u2009")[0])
                break
            name.append(word)

        phone = ""
        for i in range(0, len(allWords)):
            if "Phone:" in allWords[i]:
                phoneRaw = allWords[i + 1]
                for num in phoneRaw:
                    if num.isdigit():
                        phone += num

        firstNames.append(name[0])

        name.reverse()
        for i in name:
            if i != "" and i != "III" and i != "Jr" and i != "II" and i != "I":
                lastNames.append(i)
                break

        phones.append(phone)

    removeFirstName = []
    removeLastName = []
    for i in range(len(phones)):
        if len(phones[i]) == 0:
            removeFirstName.append(firstNames[i])
            removeLastName.append(lastNames[i])

    for n in removeFirstName:
        firstNames.remove(n)
        phones.remove("")
    for n in removeLastName:
        lastNames.remove(n)

    outDf["first names"] = firstNames
    outDf["last names"] = lastNames
    outDf["phones"] = phones

    outDf.to_csv("../Assets/namePhone.csv", index=False)

def SendOutlookEmailTo(address, subject, msg):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.To = address
    mail.Body = msg
    mail.Send()

def sendOutEmail():
    Df = GenerateEmail()
    print(Df)
    for i in range(0, len(Df)):
        address = Df["Addresses"][i]
        subject = Df["emailTitles"][i]
        msg = Df["messages"][i]
        SendOutlookEmailTo(address, subject, msg)


#############################################################





winBg = "#101010"
winFg = "#bfbfbf"
tfBg = "#222222"
fnt = "none 12 bold"

def browseDirButtonCmd(entry):
    file = tkinter.filedialog.askopenfile(mode='r', filetypes=[('csv files', '*.csv')])
    if file is not None:
        entry.delete(0, END)
        entry.insert(0, file.name)

def pullEntries(csvFile):
    df = pandas.read_csv(csvFile)

    outDf = pandas.DataFrame()

    firstNames = ["Jingtian"]
    lastNames = ["Li"]
    emails = ["jingtianli.animation@gmail.com"]

    for item in df.Body:
        allWords = item.split(' ')
        name = []
        for word in allWords:
            if "has" in word:
                if "\u2009" in word:
                    name.append(word.split("\u2009")[0])
                break
            name.append(word)

        email = ""
        for i in range(0, len(allWords)):
            if "Email:" in allWords[i]:
                email = allWords[i+1][:-7]

        firstNames.append(name[0])

        name.reverse()
        for i in name:
            if i != "" and i != "III" and i != "Jr" and i != "II" and i != "I":
                lastNames.append(i)
                break

        emails.append(email)

    outDf["first names"] = firstNames
    outDf["last names"] = lastNames
    outDf["emails"] = emails

    return outDf

def GenerateEntriesCmd(entry, outputField):
    file = entry.get()
    df = pullEntries(file)
    outputField.insert(END, df.to_string())

def GenerateEmail(TitleField, BodyField, ouputField):
    pass

def SendEmail(DataFrame):
    pass

window = Tk()
window.title("Web Inquiry Replier")
window.config(background=winBg, height=200, width=200)
Label(window, text="Please select the csv file:", bg=winBg, fg=winFg, font=fnt).grid(row=1, column=0, sticky=W)
DirEntry = Entry(window, width=50, bg=tfBg, fg=winFg, font=fnt)
DirEntry.grid(row=2, column=0, sticky=W)
Button(window, text="...", command=lambda: browseDirButtonCmd(DirEntry), bg=winBg, fg=winFg, font=fnt, height=1).grid(row=2, column=1, sticky=W)

Output = Text(window, width=50, height=20, wrap=WORD, background=tfBg,fg=winFg,font=fnt)
Output.grid(row=9, column=0, sticky = W)

Button(window, text="generate entries", command=lambda: GenerateEntriesCmd(DirEntry, Output), bg=winBg, fg=winFg, font=fnt, height=1).grid(row=3, column=0, sticky=W)

Label(window, text="Subject: ", bg=winBg, fg=winFg, font=fnt).grid(row=4, column=0, sticky=W)
TitleEntry = Entry(window, width=50, bg=tfBg, fg=winFg, font=fnt)
TitleEntry.grid(row=5, column=0, sticky=W)

Label(window, text="Body:", bg=winBg, fg=winFg, font=fnt).grid(row=6, column=0, sticky=W)
MsgEntry = Entry(window, width=50, bg=tfBg, fg=winFg, font=fnt)
MsgEntry.grid(row=7, column=0, sticky=W)

Button(window, text="generate email", command=lambda: GenerateEmail(DirEntry, Output), bg=winBg, fg=winFg, font=fnt, height=1).grid(row=8, column=0, sticky=W)
Button(window, text="send Email", command=lambda: GenerateEmail(DirEntry, Output), bg=winBg, fg=winFg, font=fnt, height=1).grid(row=8, column=0, sticky=W)
window.mainloop()