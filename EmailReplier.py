from OutlookUtility import *
def CheckAndSendWebInqReplyMsg():
    startTime = getDateTimeImport("please specify the starting time")
    endTime = getDateTimeImport("please specify the ending time")
    EmailMsgs = GetIboxMsgBodyAsList(subject='New Web Inquiry Received for Master of Game Development', startingDate=startTime, endDate=endTime)
    msgCount = len(EmailMsgs)
    if msgCount == 0:
        print("there are not messages found")
        return

    print("this is how the msg will look like: \n")
    testName, textEmail, testPhone = GetContactFromMsg(EmailMsgs[0])
    print(ComposeEmail(testName.split(' ')[0]))

    confirm = input(f"{msgCount} messages will be send out, confirm msg?(y/n)\n")

    if confirm == 'y':
        for Emailmsg in EmailMsgs:
            name, email, phone = GetContactFromMsg(Emailmsg)
            msg = ComposeEmail(name.split(' ')[0])

            SendOutlookEmailTo(email, "Thank you for your interest in MGD!", msg)

CheckAndSendWebInqReplyMsg()
