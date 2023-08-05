# Import Widgets
from tkinter import BOTH , NO , StringVar
import ttkbootstrap as ttk
from kanwar import MessageBox
from kanwar import envVars as myEnv
from kanwar import CreateToolTip

# Import tab
try:
    from test import Test
except:
    from kanwar import Test


class Result:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        self.tests = []
        self.rollnumbers = []
        self.columns = ('sr' ,'testname', 'date' ,'student_name' ,'rollno' ,  'code' , 'lecture' ,'grade', 'total_marks', 'obtained_marks', 'passing_marks','status') 

        self.root = ttk.LabelFrame(self.master , text = 'Results Management')
        self.root.pack(expand=1, fill='both')

        self.left_column = ttk.Frame(self.root)
        self.left_column.pack(side='left',fill='both')

        self.row1 = ttk.Frame(self.left_column)
        self.row1.pack(side = 'top' , fill = 'x',padx=10)

        self.lbl_test = ttk.Label(self.row1 , text = 'Test Code : ')
        self.lbl_test.pack(side = 'left' , padx=[10,26] , pady=10)

        self.com_test = ttk.Combobox(self.row1 , values=() , width=18,state='readonly')
        self.com_test.pack(side='left' , padx=15 , pady =10)

        self.lbl_conf = ttk.Label(self.row1,text='Manage Test : ')
        self.lbl_conf.pack(side='left' , padx=10 , pady=10)

        self.btn_conf = ttk.Button(self.row1 , text ='Configure' , width=18 , style='Outline.TButton' , command=self.addTab)
        self.btn_conf.pack(side = 'left' , padx =5 , pady = 10)

        self.row2 = ttk.Frame(self.left_column)
        self.row2.pack(side = 'top' , fill = 'x',padx=12)

        self.lbl_rollno = ttk.Label(self.row2 , text = "Roll No :" )
        self.lbl_rollno.pack(side = 'left' ,padx=10, pady = 10)

        self.com_rollno_values = ()

        self.com_rollno = ttk.Combobox(self.row2 , width = 18 , values=self.com_rollno_values,state='readonly')
        self.com_rollno.pack(side = 'left' , padx = [45,10] , pady = 10)
        self.com_test.bind("<Enter>",self.get_test_info)

        self.com_rollno.bind("<Enter>",self.get_student_name)

        self.lbl_obtained_marks = ttk.Label(self.row2 , text = "Obtained Marks :" )
        self.lbl_obtained_marks.pack(side = 'left' , padx = [10,0] , pady = 10)

        self.txt_obtained_marks = ttk.Entry(self.row2)
        self.txt_obtained_marks.pack(side = 'left' , padx =5 , pady =10)

        #### Row 2
        self.row3 = ttk.Frame(self.left_column)
        self.row3.pack(expand=1,fill = BOTH,pady=10,padx=10)

        self.scrollx = ttk.Scrollbar(self.row3 , orient='horizontal')
        self.scrolly = ttk.Scrollbar(self.row3 , orient='vertical')
        self.scrolly.pack(side = 'right',fill='y')
        self.scrollx.pack(side = 'bottom',fill='x')

        self.tree = ttk.Treeview(self.row3 , columns=self.columns,
                        xscrollcommand=self.scrollx.set,yscrollcommand=self.scrolly.set)
        self.tree.pack(fill='both',expand=1)

        self.scrollx.config(command=self.tree.xview)
        self.scrolly.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("student_name" , text = 'Student Name' , anchor='w')
        self.tree.heading("rollno" , text = 'Roll No' , anchor='w')
        self.tree.heading("code" , text = 'Class' , anchor='w')
        self.tree.heading("lecture" , text = 'Subject' , anchor='w')
        self.tree.heading("testname" , text = 'Test Title' , anchor='w')
        self.tree.heading("date" , text = 'Test Date' , anchor='w')
        self.tree.heading("total_marks" , text = 'Total Marks' , anchor='w')
        self.tree.heading("obtained_marks" , text = 'Obtained Marks' , anchor='w')
        self.tree.heading("passing_marks" , text = 'Passing Marks' , anchor='w')
        self.tree.heading("status" , text = 'Status' , anchor='w')
        self.tree.heading("grade" , text = 'Percentage' , anchor='w')

        self.tree.column('sr' , width=200 , anchor='w')
        self.tree.column('student_name' , width=200 , anchor='w')
        self.tree.column('rollno' , width=200 , anchor='w')
        self.tree.column('code' , width=200 , anchor='w')
        self.tree.column('lecture' , width=200 , anchor='w')
        self.tree.column('testname' , width=200 , anchor='w')
        self.tree.column('date' , width=200 , anchor='w')
        self.tree.column('total_marks' , width=200 , anchor='w')
        self.tree.column('obtained_marks' , width=200 , anchor='w')
        self.tree.column('passing_marks' , width=200 , anchor='w')
        self.tree.column('status' , width=200 , anchor='w')
        self.tree.column('grade' , width=200 , anchor='w')

        self.tree.bind("<ButtonRelease-1>",self.getdata_result)
        self.tree["displaycolumns"]=('sr', 'student_name' , 'rollno', 'testname','obtained_marks','status') 

        self.com_test.bind("<<ComboboxSelected>>",self.get_rollnumbers)

        #### Row 3
        ######## BUTTONS 

        self.row4 = ttk.Frame(self.left_column)
        self.row4.pack(fill = 'x' , padx = [0,0] , pady = 10)

        self.btn_add = ttk.Button(self.row4, text = 'Save' , width = 12 , command=self.add_result)
        self.btn_add.pack(side = 'left' , padx = 10)

        self.btn_clear = ttk.Button(self.row4 , text = 'Reset' , width = 12 , command=self.reset_result)
        self.btn_clear.pack(side = 'left' , padx  = 10)

        self.btn_update = ttk.Button(self.row4 , text = 'Update' , width = 12 , command=self.update_result)
        self.btn_update.pack(side = 'left' , padx = 10)

        self.btn_delete = ttk.Button(self.row4 , text = 'Delete' , width = 12 , command=self.delete_result)
        self.btn_delete.pack(side = 'left' , padx = 10)

        self.btn_sort = ttk.Button(self.row4 , text = 'Sort' , width = 12 , command=self.sort_result)
        self.btn_sort.pack(side = 'left' , padx = 10)

        self.btn_export = ttk.Button(self.row4 , text = 'Export' , width = 12 , command=self.export_result)
        self.btn_export.pack(side = 'left' , padx = 10)

        self.txt_search = ttk.Entry(self.row4)
        self.txt_search.pack(side='left',fill='x',expand=1,padx=10)

        self.txt_search.bind("<KeyPress>",self.search_result)
        self.btn_sort.configure(state='disabled')
        self.btn_delete.configure(state='disabled')
        self.btn_update.configure(state='disabled')

        self.show_test()
        self.show_result()

    def addTab(self):
        # is binded with the button configure
        # it will be added when that button will be pressed
        testTab = Test(self.grandMaster,self.root)

    def get_test_info(self,event=None):
        pass

    def get_student_name(self,event=None):
        pass

## come
##############################################################################################
    def show_result(self,event=None):
        pass

    def show_result2(self,event=None):
        pass

    def search_result(self,event=None):
        pass


    def sort_result(self,event=None):
        pass

    ##############################################################################################
    def export_result(self,event=None):
        pass

    ###############################################################################################
    def getdata_result(self,event=None):
        pass

    def reset_result(self,event=None):
        pass

    def reset_result3(self,event=None):
        pass


    def reset_result2(self,event=None):
        pass
    ####################################### FUNCTIONS ##############################################

    def update_result(self,event=None):
        pass


    def delete_result(self,event=None):
        pass

    def add_result(self,event=None):
        pass

    def show_test(self,event=None):
        pass

    def get_rollnumbers(self,event=None,clear=True):
        pass

###################################################################################

if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    app = Result(root,ttk.Frame(root).pack())
    root.mainloop()

