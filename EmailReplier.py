#https://www.codeforests.com/2021/05/16/python-reading-email-from-outlook-2/#:~:text=5%20Useful%20Tips%20for%20Reading%20Email%20From%20Outlook,Filtering%20...%205%20Include%2FExclude%20Multiple%20Email%20Domains%20
import win32com.client as win32
import re

def GetInboxMsg(**kwargs):
    subject = kwargs.get('subject')
    onlyUnRead = kwargs.get('onlyUnRead')

    outlook = win32.Dispatch('outlook.application')
    mapi = outlook.GetNamespace('MAPI')

    for account in mapi.Accounts:
        print(account.DeliveryStore.DisplayName)

    messages = mapi.Folders(1).Folders("Inbox").Items
    messages = messages.Restrict(f'[Subject] = {subject}')
    messages = messages.Restrict(f'[Unread] = {onlyUnRead}')
    return messages


def GetIboxMsgBodyAsList(**kwargs):
    subject = kwargs.get('subject')
    onlyUnRead = kwargs.get('onlyUnRead')
    EmailMsgs = GetInboxMsg(subject=subject, onlyUnRead=onlyUnRead)
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

EmailMsgs = GetIboxMsgBodyAsList(subject='New Web Inquiry Received for Master of Game Development', onlyUnRead=True)

for Emailmsg in EmailMsgs:
    name, email, phone = GetContactFromMsg(Emailmsg)
    print(f"found student {name} with email: {email}, and phone: {phone}")
