import random
from tkinter import *
from tkcalendar import Calendar
from OutlookUtility import GetIboxMsgBodyAsList
from OutlookUtility import GetContactFromMsg
from OutlookUtility import SendOutlookEmailTo
import re
from datetime import datetime

# colorGlobals:
winBg = "#252525"
winFg = "#bfbfbf"
tfBg = "#353535"
btBg = "#454545"
fnt = "none 12 bold"
insertbackgroundCd = '#FFFFFF'


class Contact:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


# globals:
allEmails = []
allContacts = []


def ClearEntryContent(entry):
    entry.delete(FIRST, END)


def ClearTextContent(text):
    text.delete('1.0', "end")


def SearchEmailsCmd(subject, startDate, endDate, OutMsgEntry):
    global allEmails

    subjectStr = subject.get()
    startDateStr = startDate.get_date() + " 00:00 AM"
    endDateStr = endDate.get_date() + " 23:59 PM"

    allEmails = GetIboxMsgBodyAsList(subject=subjectStr, startingDate=startDateStr, endDate=endDateStr)

    OutMsgEntry.config(state='normal')
    ClearTextContent(OutMsgEntry)
    emailCnt = len(allEmails)
    if emailCnt == 0:
        OutMsgEntry.insert(END, "Can't find any web inqury email")
        OutMsgEntry.config(state='disabled')
        return

    OutMsgEntry.insert(END, f"found {emailCnt} emails.\nexample:\n{allEmails[0]}")
    OutMsgEntry.config(state='disabled')


def ExtractContactCmd(name, email, phone, outText):
    global allEmails
    global allContacts

    if len(allEmails) == 0:
        return
    allContacts = []

    outText.config(state='normal')
    ClearTextContent(outText)

    nameStr=name.get()
    emailStr=email.get()
    phoneStr=phone.get()

    exampleEmail = allEmails[0]

    garbage=exampleEmail.replace(nameStr, "", 1)
    garbage=garbage.replace(emailStr, "", 1)
    garbage=garbage.replace(phoneStr, "", 1)

    garbageWords = re.split("\s+", garbage)

    for msg in allEmails:
        allMsgWords = re.split('\s+', msg)
        infoList = [info for info in allMsgWords if info not in garbageWords]

        fullName = " ".join(infoList[0:len(infoList)-2])
        fullName = re.sub(r'[^\w\s]', '', fullName)#remove punctuation
        email = infoList[-2]
        phone = infoList[-1]

        allContacts.append(Contact(fullName, email, phone))
        outText.insert(END, f"{fullName} | {email} | {phone}\n")
    outText.config(state='disabled')

def AutoExtractContactCmd(outText):
    global allEmails
    global allContacts
    outText.config(state='normal')
    ClearTextContent(outText)
    for msg in allEmails:
        fullName, email, phone = GetContactFromMsg(msg)
        allContacts.append(Contact(fullName, email, phone))
        outText.insert(END, f"{fullName} | {email} | {phone}\n")
    outText.config(state='disabled')

def ComposeMsgForContact(contact, body):
    fullname = contact.name
    name = fullname.split(" ")[0]
    bodyStr = body.get("1.0", END)
    bodyStr = bodyStr.replace("{name}", name)
    return bodyStr


def PreviewEmailCmd(subject, body, outText):
    global allContacts
    outText.config(state='normal')
    ClearTextContent(outText)
    contactCnt = len(allContacts)
    if contactCnt == 0:
        outText.insert(END, "no contact found to preview")
        return

    randIndex = random.randint(0, len(allContacts) - 1)
    bodyStr = ComposeMsgForContact(allContacts[randIndex], body)
    outText.insert(END, bodyStr)
    outText.config(state='disabled')


def GenerateMsgCmd(subject, body, outText):
    global allContacts
    outText.config(state='normal')
    ClearTextContent(outText)
    contactCnt = len(allContacts)
    if contactCnt == 0:
        outText.insert(END, "no contact found to preview")
        return

    for contact in allContacts:
        bodyStr = ComposeMsgForContact(contact, body)
        outText.insert(END, contact.phone + "\n\n")
        outText.insert(END, bodyStr)
        outText.insert(END, "--------------------------------------------\n\n")

    outText.config(state='disabled')


def SendCmd(subject, body):
    global allContacts
    for contact in allContacts:
        email = contact.email
        subjectStr = subject.get("1.0", END)
        bodyStr = ComposeMsgForContact(contact, body)

        SendOutlookEmailTo(email, subjectStr, bodyStr)


def GetTemplateBody():
    msg = """Dear {name},

This is Professor Li, director of the Master of Game Development program.

We have received a web inquiry from you, and thank you for your interest in the program.
If you have any questions about the program, please do not hesitate to reply to this email directly, and I am more than happy to answer them.

Thank you!

JT
"""
    return msg


def GetTemplateSMSBody():
    msg = """Dear {name}, this is Professor Li, director of the Master of Game Development program. We have received a web inquiry from you, and thank you for your interest in the program.If you have any questions about the program, please do not hesitate to reply to this message directly, and I am more than happy to answer them.

Thank you!
"""
    return msg


def GetTemplateSubject():
    return "Thank you for your interest in MGD!"


window = Tk()
window.title("Web Inquiry Replier")
window.config(background=winBg, height=1300, width=1080)

# Time Range
TimeRangeFrame = Frame(window, background=winBg)
TimeRangeFrame.place(x=10, y=0)

Label(TimeRangeFrame, text="Select the start date:", bg=winBg, fg=winFg, font=fnt).grid(row=0, column=0, sticky=W)
startDate = Calendar(TimeRangeFrame, date_pattern='yyyy-mm-dd')
startDate.grid(row=1, column=0, sticky=W)

Label(TimeRangeFrame, text="Select the end date:", bg=winBg, fg=winFg, font=fnt).grid(row=0, column=1, sticky=W)
endDate = Calendar(TimeRangeFrame, date_pattern='yyyy-mm-dd')
endDate.grid(row=1, column=1, sticky=W)

# info retrive
inforFrameWidth = 55
InfoFrame = Frame(window, background=winBg)
InfoFrame.place(x=10, y=220)
Label(InfoFrame, text="Search Subject:", bg=winBg, font=fnt, fg=winFg).grid(row=0, column=0, sticky=W)
subjectEntry = Entry(InfoFrame, width=inforFrameWidth, bg=tfBg, fg=winFg, font=fnt, insertbackground=insertbackgroundCd)
subjectEntry.insert(index=0, string="New Web Inquiry Received for Master of Game Development")
subjectEntry.grid(row=1, column=0)

SearchReportText = Text(InfoFrame, width=inforFrameWidth, height=12, wrap=WORD, background=tfBg, fg=winFg, font=fnt,insertbackground=insertbackgroundCd, state="disabled")
SearchBtn = Button(InfoFrame, text="Search Emails", width=inforFrameWidth - 6, background=btBg, font=fnt, fg=winFg,command=lambda: SearchEmailsCmd(startDate=startDate, subject=subjectEntry, endDate=endDate,OutMsgEntry=SearchReportText))
SearchBtn.grid(row=2, column=0, pady=5)
SearchReportText.grid(row=3, column=0)

Label(InfoFrame, text="Name:", bg=winBg, font=fnt, fg=winFg).grid(row=4, column=0, sticky=W)
NameEntry = Entry(InfoFrame, width=inforFrameWidth, bg=tfBg, fg=winFg, font=fnt, insertbackground=insertbackgroundCd)
NameEntry.grid(row=5, sticky=W)

Label(InfoFrame, text="Email:", bg=winBg, font=fnt, fg=winFg).grid(row=6, column=0, sticky=W)
EmailEntry = Entry(InfoFrame, width=inforFrameWidth, bg=tfBg, fg=winFg, font=fnt, insertbackground=insertbackgroundCd)
EmailEntry.grid(row=7, sticky=W)

Label(InfoFrame, text="Phone:", bg=winBg, font=fnt, fg=winFg).grid(row=8, column=0, sticky=W)
PhoneEntry = Entry(InfoFrame, width=inforFrameWidth, bg=tfBg, fg=winFg, font=fnt, insertbackground=insertbackgroundCd)
PhoneEntry.grid(row=9, sticky=W)

ExtractReportText = Text(InfoFrame, width=inforFrameWidth, height=10, wrap=WORD, background=tfBg, fg=winFg, font=fnt,insertbackground=insertbackgroundCd, state="disabled")
ExtractBtn = Button(InfoFrame, text="Extract Contact", width=inforFrameWidth - 6, background=btBg, font=fnt, fg=winFg,command=lambda: ExtractContactCmd(name=NameEntry, email=EmailEntry, phone=PhoneEntry ,outText=ExtractReportText))
ExtractBtn.grid(row=10, column=0, pady=5)
ExtractReportText.grid(row=11, column=0)

# out email
outFrameWidth = 60
OutFrame = Frame(window, background=winBg)
outBoxHeight = 20
OutFrame.place(x=520, y=0)

Label(OutFrame, text="Out Email Subject: ", bg=winBg, font=fnt, fg=winFg).grid(row=0, column=0, sticky=W)
OutEmailSubectEntry = Text(OutFrame, width=outFrameWidth, height=1, wrap=WORD, background=tfBg, fg=winFg, font=fnt, insertbackground=insertbackgroundCd)
OutEmailSubectEntry.grid(row=1, column=0)
OutEmailSubectEntry.insert(END, GetTemplateSubject())

Label(OutFrame, text="", background=winBg).grid(row=2)

Label(OutFrame, text="Out Email Body: ", bg=winBg, font=fnt, fg=winFg).grid(row=3, column=0, sticky=W)
OutEmailBodyEntry = Text(OutFrame, width=outFrameWidth, height=outBoxHeight, wrap=WORD, background=tfBg, fg=winFg, font=fnt,insertbackground=insertbackgroundCd)
OutEmailBodyEntry.grid(row=4, column=0)
OutEmailBodyEntry.insert(END, GetTemplateBody())

OutPreviewText = Text(OutFrame, width=outFrameWidth, height=outBoxHeight, wrap=WORD, background=tfBg, fg=winFg, font=fnt,insertbackground=insertbackgroundCd, state="disabled")
PreviewBtn = Button(OutFrame, text="Preview", width=outFrameWidth - 7, background=btBg, font=fnt, fg=winFg,command=lambda: PreviewEmailCmd(subject=OutEmailSubectEntry, body=OutEmailBodyEntry,outText=OutPreviewText))
PreviewBtn.grid(row=5, column=0, pady=5)
OutPreviewText.grid(row=6, column=0)

SendEmailBtn = Button(OutFrame, text="Send Email", width=outFrameWidth - 7, background=btBg, font=fnt, fg=winFg,command=lambda: SendCmd(subject=OutEmailSubectEntry, body=OutEmailBodyEntry))
SendEmailBtn.grid(row=7, column=0, pady=10)

# text msg data:
TextFrameWidth = 122
TextPreivewBoxWidth = 52
TextPreivewBoxHeight = 15
TextPreivewBtnMargin = 5
TextPreviewBtnWidth = TextFrameWidth - TextPreivewBoxWidth * 2 - TextPreivewBtnMargin * 2

TextFrame = Frame(window, background=winBg)
TextFrame.place(x=10, y=950)

Label(TextFrame, text="Out Messages:", bg=winBg, font=fnt, fg=winFg).grid(row=0, column=0, sticky=W)
OutMsgBodyEntry = Text(TextFrame, width=TextPreivewBoxWidth, height=TextPreivewBoxHeight, wrap=WORD, background=tfBg,fg=winFg, font=fnt, insertbackground=insertbackgroundCd)
OutMsgBodyEntry.grid(row=1, column=0, pady=10)
OutMsgBodyEntry.insert(END, GetTemplateSMSBody())

MsgPreviewText = Text(TextFrame, width=TextPreivewBoxWidth, height=TextPreivewBoxHeight, wrap=WORD, background=tfBg,fg=winFg, font=fnt, insertbackground=insertbackgroundCd, state="disabled")
MsgPGenerateBtn = Button(TextFrame, text="Generate", width=TextPreviewBtnWidth, height=TextPreivewBoxHeight - 2,background=btBg, font=fnt, fg=winFg,command=lambda: GenerateMsgCmd(subject=OutEmailSubectEntry, body=OutMsgBodyEntry, outText=MsgPreviewText))
MsgPGenerateBtn.grid(row=1, column=1, padx=TextPreivewBtnMargin, pady=TextPreivewBtnMargin)
MsgPreviewText.grid(row=1, column=2)

window.mainloop()