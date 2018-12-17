#-*- coding: utf-8 -*-
from Tkinter import *



class Window():
    def __init__(self, root):
        self.root = root
        self.root.title("Server")
        Label(text="_____    Відмічено на початку заняття", fg="green", 
              ).grid(row=0, column=0, columnspan=3, 
                     sticky=W, padx=10, pady=3)
        Label(text="_____    Відмічено вкінці заняття", fg="green4", 
              ).grid(row=1, column=0, columnspan=3, sticky=W, 
                     padx=10, pady=3)
        Label(text="_____    Не відмічено через невідповідність розкладу",
              fg="blue",).grid(row=2, column=0, columnspan=3, sticky=W, 
                               padx=10, pady=3)
        Label(text="_____    Немає учня у базі даних", fg="red", 
              ).grid(row=3, column=0, columnspan=3, sticky=W, 
                     padx=10, pady=3)
        
        scrollbarV = Scrollbar(root, width=25)
        scrollbarV.grid(row=5, column=3, rowspan=2, sticky=NS)

        scrollbarH = Scrollbar(root, orient=HORIZONTAL, width=20)
        scrollbarH.grid(row=4, column=0, columnspan=4, sticky=EW)
        self.log_list = Listbox(root,  width=60, yscrollcommand=scrollbarV.set,
                                xscrollcommand=scrollbarH.set)
        self.log_list.grid(row=5, column=0, columnspan=3, rowspan=2)

        scrollbarV.config(command=self.log_list.yview)
        scrollbarH.config(command=self.log_list.xview)
        #self.log_list.insert(END, "111111111")

        self.clear_but = Button(root, width=53, text="Clear log" ,command=self.clear)
        self.clear_but.grid(row=7, column=0, columnspan=4)

    def clear(self):
        self.log_list.delete(0, END)

    def print_log(self, s):
        self.log_list.insert(END, s)

if __name__ == '__main__':
    root = Tk()
    root.geometry("350x300")
    Window(root)
    root.mainloop()