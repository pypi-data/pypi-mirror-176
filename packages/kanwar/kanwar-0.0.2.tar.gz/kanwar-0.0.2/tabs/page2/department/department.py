# Import Widgets
from tkinter import BOTH , NO , StringVar
import ttkbootstrap as ttk
from kanwar import MessageBox
from kanwar import envVars as myEnv

class Department:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        self.classes = [] 
        self.dcourse = StringVar()
        self.dcourse_code = StringVar()
        self.dlecture = StringVar()

        self.root = ttk.LabelFrame(self.master , text = 'Class Management')
        self.root.pack(fill = BOTH, expand=1)

        self.left_column = ttk.Frame(self.root)
        self.left_column.pack(expand=1,fill = BOTH)

        #### Row 1

        self.row1 = ttk.Frame(self.left_column)
        self.row1.pack(side = 'top' , fill = 'x', padx = 10 , pady = 10)

        self.lbl_course_code = ttk.Label(self.row1 , text = 'Class Code :   ')
        self.lbl_course_code.pack(side = 'left' , padx = 10)

        self.txt_course_code = ttk.Entry(self.row1 , textvariable=self.dcourse_code)
        self.txt_course_code.pack(side='left' , padx = 18)

        self.lbl_course = ttk.Label(self.row1 , text = 'Description : ')
        self.lbl_course.pack(side = 'left' , padx = 10)

        self.txt_course = ttk.Entry(self.row1 , textvariable=self.dcourse)
        self.txt_course.pack(side = 'left' , padx = 10,fill='x',expand=1)

        self.row2 = ttk.Frame(self.left_column)
        self.row2.pack(side = 'top' , fill = 'x', padx = 10 , pady = 10)

        self.lbl_lecture = ttk.Label(self.row2 , text = 'Lectures : ')
        self.lbl_lecture.pack(side = 'left' , padx = 10)

        self.txt_lecture = ttk.Entry(self.row2 , textvariable=self.dlecture , width = 45)
        self.txt_lecture.pack(side = 'left',fill='x',padx=[35,10],expand=1)

        #### Row 3

        self.row3 = ttk.Frame(self.left_column)
        self.row3.pack(fill = 'both' , padx = 10 , pady = 10, expand=1)

        self.scrollx = ttk.Scrollbar(self.row3 , orient='horizontal')
        self.scrolly = ttk.Scrollbar(self.row3 , orient='vertical')
        self.scrolly.pack(side = 'right',fill='y')
        self.scrollx.pack(side = 'bottom',fill='x')

        self.class_columns = ('Sr','Class','Code','lecture') 

        self.tree = ttk.Treeview(self.row3 , columns=self.class_columns,
                        xscrollcommand=self.scrollx.set,yscrollcommand=self.scrolly.set)
        self.tree.pack(fill=BOTH,expand=1)

        self.scrollx.config(command=self.tree.xview)
        self.scrolly.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("Sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("Class" , text = 'Code' , anchor='w')
        self.tree.heading("Code" , text = 'Description' , anchor='w')
        self.tree.heading("lecture" , text = 'Lectures' , anchor='w')

        self.tree.column('Sr' , width= 200 , anchor='w')
        self.tree.column('Class' , width= 200 , anchor='w')
        self.tree.column('Code' , width= 200 , anchor='w')
        self.tree.column('lecture' , width=200 , anchor='w')

        #### Row 3
        ######## BUTTONS 
        self.row4 = ttk.Frame(self.left_column)
        self.row4.pack(fill = 'both' , padx = [0,0] , pady = 10)

        self.btn_add = ttk.Button(self.row4, text = 'Save' , width = 12 , command=self.add_class)
        self.btn_add.pack(side = 'left' , padx = 10)

        self.btn_clear = ttk.Button(self.row4 , text = 'Reset' , width = 12 , command=self.reset_class)
        self.btn_clear.pack(side = 'left' , padx  = 10)

        self.btn_update = ttk.Button(self.row4 , text = 'Update' , width = 12 , command=self.update_class)
        self.btn_update.pack(side = 'left' , padx = 10)

        self.btn_delete = ttk.Button(self.row4 , text = 'Delete' , width = 12 , command=self.delete_class)
        self.btn_delete.pack(side = 'left' , padx = 10)

        self.btn_sort = ttk.Button(self.row4 , text = 'Sort' , width = 12 , state='disabled')
        self.btn_sort.pack(side = 'left' , padx = 10)

        self.btn_export = ttk.Button(self.row4 , text = 'Export' , width = 12 , command=self.export_class)
        self.btn_export.pack(side = 'left' , padx = 10)

        self.txt_search = ttk.Entry(self.row4)
        self.txt_search.pack(side='left',fill='x',expand=1,padx=10)

        self.txt_search.bind("<KeyPress>",self.search_class)

        self.btn_update.configure(state='disabled')
        self.btn_delete.configure(state='disabled')
        self.tree.bind("<ButtonRelease-1>",self.getData)
        self.show_class()

        ####################################### DATA BASE START ##########################################
    def getClasses(self):
        return self.classes

    def show_class(self,event=None):
        pass

    def search_class(self,event=None):
        pass


    def export_class(self,event=None):
        pass

    ###############################################################################################            
    def reset_class(self,event=None):
        pass

    def getData(self,event=None):
        pass

    ####################################### FUNCTIONS ##############################################

    def delete_class(self,event=None):
        pass

    def update_class(self,event=None):
        pass

    def add_class(self,event=None):
        pass
        ####################################### DATA BASE END ##########################################

if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    app = Department(root,ttk.Frame(root).pack())
    root.focus_set()
    root.mainloop()
