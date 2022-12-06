import EmailReplier
from tkinter import *
from tkcalendar import Calendar

#colorGlobals:
winBg = "#101010"
winFg = "#bfbfbf"
tfBg = "#222222"
fnt = "none 12 bold"

window = Tk()
window.title("Web Inquiry Replier")
window.config(background=winBg, height=200, width=200)

Label(window, text="Please select the start date:", bg=winBg, fg=winFg, font=fnt).grid(row=1, column=0, sticky=W)
startDate = Calendar(window)
startDate.grid(row=2, column=0, sticky=W)

Label(window, text="Please select the end date:", bg=winBg, fg=winFg, font=fnt).grid(row=1, column=1, sticky=W)
startDate = Calendar(window)
startDate.grid(row=2, column=1, sticky=W)

Label(window, text="Specify subject:", bg=winBg, font=fnt, fg=winFg).grid(row=3, column=0, sticky=W)
subjectEntry = Entry(window, width=50, bg=tfBg, fg=winFg, font=fnt)
subjectEntry.grid(row=4, column=0, columnspan=2)

window.mainloop()