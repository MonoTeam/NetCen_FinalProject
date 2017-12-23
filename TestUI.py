from tkinter import *
from tkinter import *
from tkinter import messagebox 
class ChatUI():
    def __init__(self):
        #Create a window
        base = Tk()
        base.title("bra bra")
        base.geometry("400x500")
        base.resizable(width=FALSE, height=FALSE)

        ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
        ChatLog.config(state=DISABLED)

        scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
        ChatLog['yscrollcommand'] = scrollbar.set

        SendButton = Button(base, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E")

        EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")

        scrollbar.place(x=376,y=6, height=386)
        ChatLog.place(x=6,y=6, height=386, width=370)
        EntryBox.place(x=128, y=401, height=90, width=265)
        SendButton.place(x=6, y=401, height=90)
        base.mainloop()
test = ChatUI()
