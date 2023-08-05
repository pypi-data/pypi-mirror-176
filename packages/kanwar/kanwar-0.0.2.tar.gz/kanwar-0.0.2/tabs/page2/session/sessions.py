# Import Widgets
from tkinter import BOTH , NO
import ttkbootstrap as ttk
from kanwar import MessageBox
from kanwar import envVars as myEnv

class Session:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        self.root = ttk.LabelFrame(self.master , text = 'Sessions')
        self.root.pack(fill = BOTH, expand=1)

        self.leftColumn = ttk.Frame(self.root)
        self.leftColumn.pack(expand=1,fill = BOTH,padx=10)

        #### Row 1

        self.scrollx = ttk.Scrollbar(self.leftColumn , orient='horizontal')
        self.scrolly = ttk.Scrollbar(self.leftColumn , orient='vertical')
        self.scrolly.pack(side = 'right',fill='y')
        self.scrollx.pack(side = 'bottom',fill='x')

        self.columns = ('sr', 'email' , 'pass' , 'role' , 'date' , 'time' , 'rem') 

        self.tree = ttk.Treeview(self.leftColumn , columns=self.columns,
                        xscrollcommand=self.scrollx.set,yscrollcommand=self.scrolly.set)
        self.tree.pack(fill=BOTH,expand=1)

        self.scrollx.config(command=self.tree.xview)
        self.scrolly.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("email" , text = 'Email' , anchor='w')
        self.tree.heading("pass" , text = 'Password' , anchor='w')
        self.tree.heading("role" , text = 'Role',anchor='w')
        self.tree.heading("date" , text = 'Date' , anchor='w')
        self.tree.heading("time" , text = 'Time' , anchor='w')
        self.tree.heading("rem" , text = 'Keep Logged In' , anchor='w')

        self.tree.column('sr' , width=200 , anchor='w')
        self.tree.column('email' , width=200 , anchor='w')
        self.tree.column('pass' , width=200 , anchor='w')
        self.tree.column('role' , width=200 , anchor='w')
        self.tree.column('date' , width=200 , anchor='w')
        self.tree.column('time' , width=200 , anchor='w')
        self.tree.column('rem' , width=200 , anchor='w')
        self.tree["displaycolumns"]=('sr', 'email' , 'role' , 'date' , 'time' , 'rem') 
        self.show_sessions()
    ####################################### FUNCTIONS ##############################################
    def show_sessions(self,event=None):
        pass
if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    frame = Frame(root)
    frame.pack()
    sessionTab = Session(root,frame)
    root.mainloop()
