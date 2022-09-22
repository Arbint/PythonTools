import os
import subprocess
import tkinter.filedialog
from tkinter import *
from os.path import join, getsize

winBg = "#080808"
winFg = "#bfbfbf"
tfBg = "#222222"
fnt = "none 12 bold"
winHeight = 300
winWidth = 300
def getAllFilesInDir(dir, sizeFilter=100):
    allFiles = []
    for path, currentDir, files in os.walk(dir):
        for file in files:
            size = getsize(join(path, file))
            print(size)
            if size/(1024*1024) >= sizeFilter:
                fullPath = join(path, file)
                relativePath = fullPath.replace(dir+"\\", "")
                relativePath = relativePath.replace("\\", "/")
                if ".git" not in relativePath:
                    allFiles.append(relativePath)
    return allFiles

def browseDirButtonCmd(entry):
    dir = tkinter.filedialog.askdirectory()
    entry.delete(0, END)
    entry.insert(0, dir)

def trackFiles(sizeEntryField, DirEntryField, outPut):
    size = int(sizeEntryField.get())
    dir = DirEntryField.get()
    allFiles = getAllFilesInDir(dir, size)
    cmd = ["git", "lfs", "track"]
    for file in allFiles:
        cmd.append(file)
        outPut.insert(END, file + "\n")

    subprocess.Popen(cmd, cwd=dir)

window = Tk()
window.title("Git Track LFS")
window.config(background=winBg, height=winHeight, width=winWidth)
window.resizable(False, True)

canvas = Canvas(width=winWidth, height=200, bg=winBg, highlightthickness=0)
uiw_img = PhotoImage(file="assets/LFS_Tracker_Label.gif")
canvas.create_image(winHeight/2, winWidth/2, image=uiw_img)
canvas.grid(row=0,column=0)

#Label(window, image=windowLabel, bg="black").grid(row=0, column=0, sticky=E)

Label(window, text="Please select the directory:", bg=winBg, fg=winFg, font=fnt).grid(row=1, column=0, sticky=W)
DirEntry = Entry(window, width=50, bg=tfBg, fg=winFg, font=fnt)
DirEntry.grid(row=2, column=0, sticky=W)
Button(window, text="...", command=lambda: browseDirButtonCmd(DirEntry), bg=winBg, fg=winFg, font=fnt, height=1).grid(
    row=2, column=1, sticky=W)

Label(window, text="Min Size: ", bg=winBg, fg=winFg, font=fnt).grid(row=3, column=0, sticky=W)
SizeEntry = Entry(window, width=53, bg=tfBg, fg=winFg, font=fnt)
SizeEntry.insert(0, "100")
SizeEntry.grid(row=4, column=0, columnspan=2)

OutScrollBar = Scrollbar(orient="vertical")
OutScrollBar.grid(row=6, column=2)

Output = Text(window, width=53, height=50,  wrap=WORD, background=tfBg, fg=winFg, font=fnt)
Output.grid(row=6, column=0, sticky=W)
Output['yscrollcommand'] = OutScrollBar.set


Button(window, text="Track", command=lambda: trackFiles(SizeEntry, DirEntry, Output), width=30, bg=winBg, fg=winFg,
       font=fnt, height=1).grid(row=5, column=0, sticky=W)
window.mainloop()
