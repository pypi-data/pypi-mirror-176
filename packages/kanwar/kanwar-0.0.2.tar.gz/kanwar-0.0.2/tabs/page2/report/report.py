# Import Widgets
# This tab needs construction
from tkinter import * 
import ttkbootstrap as ttk
from kanwar import MessageBox
from kanwar import envVars as myEnv

class Report:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        self.classes = []
        self.rollnumbers = []
        self.dates = []

        self.root = ttk.LabelFrame(self.master  , text ='Report')
        self.root.pack(expand=1,fill='both')

        self.leftColumn = ttk.Frame(self.root)
        self.leftColumn.pack(expand=1,fill='both')

        self.leftColumn_row1 = ttk.Frame(self.leftColumn)
        self.leftColumn_row1.pack(side='top',fill='x',padx=10)

        self.lbl_class_report = ttk.Label(self.leftColumn_row1 , text='Class Code :')
        self.lbl_class_report.grid(row=0,column=0)

        self.com_class_report = ttk.Combobox(self.leftColumn_row1,state='readonly',values=self.classes , width=18)
        self.com_class_report.grid(row=0,column=1,pady=10 , sticky='ew')

        self.lbl_rollno_report = ttk.Label(self.leftColumn_row1 , text='Roll No :')
        self.lbl_rollno_report.grid(row=0,column=2)

        self.com_rollno_report = ttk.Combobox(self.leftColumn_row1,values=[],state='readonly' , width=18) # rollnumbers
        self.com_rollno_report.grid(row=0,column=3,pady=10 , sticky='ew')

        self.lbl_lecture_report = ttk.Label(self.leftColumn_row1 , text='Lecture :')
        self.lbl_lecture_report.grid(row=0,column=4)

        self.com_lecture_report = ttk.Combobox(self.leftColumn_row1,values=() , width=18,state='readonly')
        self.com_lecture_report.grid(row=0,column=5,pady=10 , sticky='ew')

        self.lbl_month_report = ttk.Label(self.leftColumn_row1 , text='Month :  ')
        self.lbl_month_report.grid(row=1,column=0)

        self.com_month_report = ttk.Combobox(self.leftColumn_row1,values=() , width=18,state='readonly')
        self.com_month_report.grid(row=1,column=1,pady=10 , sticky='ew')

        self.leftColumn_row1.columnconfigure((0,1,2,3,4,5),weight=1)

        self.com_class_report.bind("<<ComboboxSelected>>",self.get_rollnumbers_report)
        self.com_month_report.bind("<<ComboboxSelected>>",self.get_details)
        ###################################################
        self.leftColumn_row2 = ttk.Frame(self.leftColumn)
        self.leftColumn_row2.pack(expand=1,fill = BOTH,pady=10,padx=10)

        #### Row 1

        self.scrollx = ttk.Scrollbar(self.leftColumn_row2 , orient='horizontal')
        self.scrolly = ttk.Scrollbar(self.leftColumn_row2 , orient='vertical')
        self.scrolly.pack(side = 'right',fill='y')
        self.scrollx.pack(side = 'bottom',fill='x')

        self.class_columns_page8 = ('sr' ,'lecture','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','aa','ab','ac','ad') 

        self.tree = ttk.Treeview(self.leftColumn_row2 , columns=self.class_columns_page8,
                        xscrollcommand=self.scrollx.set,yscrollcommand=self.scrolly.set)
        self.tree.pack(fill='both',expand=1)

        self.scrollx.config(command=self.tree.xview)
        self.scrolly.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("lecture" , text = 'Lecture' , anchor='w')
        self.tree.heading("a" , text = '1' , anchor='w')
        self.tree.heading("b" , text = '2' , anchor='w')
        self.tree.heading("c" , text = '3' , anchor='w')
        self.tree.heading("d" , text = '4' , anchor='w')
        self.tree.heading("e" , text = '5' , anchor='w')
        self.tree.heading("f" , text = '6' , anchor='w')
        self.tree.heading("g" , text = '7' , anchor='w')
        self.tree.heading("h" , text = '9' , anchor='w')
        self.tree.heading("i" , text = '10' , anchor='w')
        self.tree.heading("j" , text = '11' , anchor='w')
        self.tree.heading("k" , text = '12' , anchor='w')
        self.tree.heading("l" , text = '13' , anchor='w')
        self.tree.heading("m" , text = '14' , anchor='w')
        self.tree.heading("n" , text = '15' , anchor='w')
        self.tree.heading("o" , text = '16' , anchor='w')
        self.tree.heading("p" , text = '17' , anchor='w')
        self.tree.heading("q" , text = '18' , anchor='w')
        self.tree.heading("r" , text = '19' , anchor='w')
        self.tree.heading("s" , text = '20' , anchor='w')
        self.tree.heading("t" , text = '21' , anchor='w')
        self.tree.heading("u" , text = '22' , anchor='w')
        self.tree.heading("v" , text = '23' , anchor='w')
        self.tree.heading("w" , text = '24' , anchor='w')
        self.tree.heading("x" , text = '25' , anchor='w')
        self.tree.heading("y" , text = '26' , anchor='w')
        self.tree.heading("z" , text = '27' , anchor='w')
        self.tree.heading("aa" , text = '28' , anchor='w')
        self.tree.heading("ab" , text = '29' , anchor='w')
        self.tree.heading("ac" , text = '30' , anchor='w')
        self.tree.heading("ad" , text = '31' , anchor='w')

        for i in self.class_columns_page8:
            self.tree.column(i , width=50 , anchor='w')

        self.tree.column('sr' , width=200 , anchor='w')
        self.tree.column('lecture' , width=200 , anchor='w')

        self.show_class()

    ###################################################

    def make_tuples_to_list(self,data):
        newData =  [list(i) for i in data]
        return newData

    def get_lectures_for_report(self,event=None,clear=True):
        pass

    def convert_to_tree(self,list_):
        pass

    def get_details(self,event=None):
        pass

    def get_months_report(self,event=None):
        pass

    def get_rollnumbers_report(self,event=None,clear=True):
        pass

    def show_class(self,event=None):
        pass


if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    app = Report(root,ttk.Frame(root).pack())
    root.focus_set()
    root.mainloop()
