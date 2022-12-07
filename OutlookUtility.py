#https://www.codeforests.com/2021/05/16/python-reading-email-from-outlook-2/#:~:text=5%20Useful%20Tips%20for%20Reading%20Email%20From%20Outlook,Filtering%20...%205%20Include%2FExclude%20Multiple%20Email%20Domains%20
import win32com.client as win32
import re
from datetime import datetime, timedelta

def GetInboxMsg(subject, startingDate, endDate):
    outlook = win32.Dispatch('outlook.application')
    mapi = outlook.GetNamespace('MAPI')

    messages = mapi.Folders(1).Folders("Inbox").Items
    messages = messages.Restrict(f'[Subject] = {subject}')

    messages = messages.Restrict("[ReceivedTime] >= '" + startingDate + "' And [ReceivedTime] <= '" + endDate + "'")

    return messages


def GetIboxMsgBodyAsList(subject, startingDate, endDate):
    EmailMsgs = GetInboxMsg(subject=subject, startingDate=startingDate, endDate=endDate)
    allEmails = []
    for msg in list(EmailMsgs):
        allEmails.append(msg.body)

    return allEmails


def GetContactFromMsg(msg):
    #'\s+' means all white space, including newline and such
    allWords = re.split('\s+', msg)

    nameEndPos = allWords.index('has')
    fullName = " ".join(allWords[:nameEndPos])

    emailStartPos = allWords.index('Email:')
    email = allWords[emailStartPos+1]

    phoneStartPos = allWords.index('Phone:')
    phone = allWords[phoneStartPos+1]

    return fullName, email, phone

def ComposeEmail(name):
    msg = f"""Dear {name},
This is Professor Li, director of the Master of Game Development program.
We have received a web inquiry from you, and thank you for your interest in the program.
If you have any questions about the program, please do not hesitate to reply to this email directly, and I am more than happy to answer them.
Thank you!
JT
"""
    return msg

def SendOutlookEmailTo(address, subject, msg):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.To = address
    mail.Body = msg
    mail.Send()

def getDateTimeImport(msg):
    dateStr = input(f"{msg}(format: mm/dd/yyyy)\n>>>")
    monthDayYear = dateStr.split("/")
    dateTime = datetime(month=int(monthDayYear[0]), day=int(monthDayYear[1]), year=int(monthDayYear[2]))
    return dateTime.strftime('%Y-%m-%d %H:%M %p')



