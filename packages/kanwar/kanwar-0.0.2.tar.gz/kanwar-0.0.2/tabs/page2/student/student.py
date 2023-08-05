# Import Widgets
from tkinter import BOTH , NO , StringVar 
import ttkbootstrap as ttk
from kanwar import MessageBox
from tkinter import filedialog
from kanwar import envVars as myEnv

class Student:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        self.dname = StringVar()
        self.drollno = StringVar()
        self.classes = []
        self.columns = ('Sr','code','roll no','name') 

        self.root = ttk.LabelFrame(self.master , text='Student Managment')
        self.root.pack(expand=1, fill=BOTH)
        self.left_column = ttk.Frame(self.root)
        self.left_column.pack(expand=1,fill = BOTH)

        #### Row 1

        self.row1 = ttk.Frame(self.left_column)
        self.row1.pack(side = 'top' , fill = 'x', padx = 10 , pady = 10)

        self.lbl_course_code = ttk.Label(self.row1 , text='Class Code :   ')
        self.lbl_course_code.pack(side = 'left' , padx = 10)

        self.com_codes = ()

        self.com_course_code = ttk.Combobox(self.row1 , state='readonly' , values=self.com_codes , width=18)
        self.com_course_code.pack(side = 'left' , padx = 18)

        #### Row 1.1

        self.row1_1 = ttk.Frame(self.left_column)
        self.row1_1.pack(side = 'top' , fill = 'x', padx = 10 , pady = 10)

        self.lbl_rollno = ttk.Label(self.row1_1 , text = 'Roll No : ')
        self.lbl_rollno.pack(side = 'left' , padx = 11)

        self.txt_rollno = ttk.Entry(self.row1_1 , textvariable=self.drollno)
        self.txt_rollno.pack(side ='left' , padx = [42,10])

        self.lbl_student_name = ttk.Label(self.row1_1,text = 'Student Name : ')
        self.lbl_student_name.pack(side = 'left' , padx = 10)

        self.txt_student_name = ttk.Entry(self.row1_1 , textvariable=self.dname , width = 45)
        self.txt_student_name.pack(side = 'left' , padx = 10)

        #### Row 2
        self.row2 = ttk.Frame(self.left_column)
        self.row2.pack(fill = 'both' , padx = 10 , pady = 10, expand=1)

        self.scrollx = ttk.Scrollbar(self.row2 , orient='horizontal')
        self.scrolly = ttk.Scrollbar(self.row2 , orient='vertical')
        self.scrolly.pack(side = 'right',fill='y')
        self.scrollx.pack(side = 'bottom',fill='x')

        self.tree = ttk.Treeview(self.row2 , columns=self.columns,
                        xscrollcommand=self.scrollx.set,yscrollcommand=self.scrolly.set)
        self.tree.pack(fill=BOTH,expand=1)

        self.scrollx.config(command=self.tree.xview)
        self.scrolly.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("Sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("code" , text = 'Code' , anchor='w')
        self.tree.heading("roll no" , text = 'Name',anchor='w')
        self.tree.heading("name" , text = 'Roll No.' , anchor='w')

        self.tree.column('Sr' , width=200 , anchor='w')
        self.tree.column('code' , width=200 , anchor='w')
        self.tree.column('roll no' , width=200 , anchor='w')
        self.tree.column('name' , width=200 , anchor='w')

        #### Row 3
        ######## BUTTONS 

        self.row3 = ttk.Frame(self.left_column)
        self.row3.pack(fill = 'x' , padx = [0,0] , pady = 10)

        self.btn_add = ttk.Button(self.row3, text = 'Save' , width = 12 , command = self.add_student)
        self.btn_add.pack(side = 'left' , padx = 10)

        self.btn_clear = ttk.Button(self.row3 , text = 'Reset' , width = 12 , command = self.reset_student)
        self.btn_clear.pack(side = 'left' , padx  = 10)

        self.btn_update = ttk.Button(self.row3 , text = 'Update' , width = 12 , command = self.update_student)
        self.btn_update.pack(side = 'left' , padx = 10)

        self.btn_delete = ttk.Button(self.row3 , text = 'Delete' , width = 12 , command = self.delete_student)
        self.btn_delete.pack(side = 'left' , padx = 10)

        self.btn_sort = ttk.Button(self.row3 , text = 'Sort' , width = 12 , command = self.sort_student)
        self.btn_sort.pack(side = 'left' , padx  = 10)

        self.btn_export = ttk.Button(self.row3 , text = 'Export' , width = 12 , command = self.export_student)
        self.btn_export.pack(side = 'left' , padx = 10)

        self.txt_search = ttk.Entry(self.row3)
        self.txt_search.pack(padx=10,side='left',fill='x',expand=1)

        self.txt_search.bind("<KeyPress>",self.search_student)

        self.btn_delete.configure(state='disabled')
        self.btn_update.configure(state='disabled')
        self.btn_sort.configure(state='disabled')

        self.com_course_code.bind("<<ComboboxSelected>>",lambda e, : self.btn_sort.configure(state='active'))
        self.tree.bind("<ButtonRelease-1>",self.getdata_student)
        self.show_class()
        self.show_student()
    ####################################### DATA BASE START ##########################################

    def show_student(self,event=None):
        pass

    def show_student2(self,event=None):
        pass

    def sort_student(self,event=None):
        pass

    def export_student(self,event=None):
        pass

    ###############################################################################################
    def getdata_student(self,event=None):
        pass

    def reset_student(self,event=None):
        pass

    def search_student(self,event=None):
        pass

    def delete_student(self,event=None):
        pass

    def update_student(self,event=None):
        pass

    def add_student(self,event=None):
        pass

    def show_class(self,event=None):
        pass

    ####################################### DATA BASE END ##########################################


if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    app = Student(root,ttk.Frame(root).pack())
    root.focus_set()
    root.mainloop()

