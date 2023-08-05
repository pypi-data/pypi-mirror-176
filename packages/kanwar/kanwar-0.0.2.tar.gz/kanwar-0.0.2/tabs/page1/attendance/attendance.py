# Import Widgets
from tkinter import BOTH, NO , StringVar , W , E , S ,N
import ttkbootstrap as ttk
from kanwar import MessageBox
from kanwar import envVars as myEnv

# My Frame
from kanwar import MyFrame

class Attendance:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        self.classes = []
        self.columns = ('Sr','code','lecture','date','students','status') 
        self.obj = object
        self.students_information = []
        self.boxes_infomration = None
        self.took = None
        self.ddate = StringVar()

        self.root = ttk.LabelFrame(self.master , text = 'Attendance Management')
        self.root.pack(expand= 1 , fill =BOTH)

        self.left_column = ttk.Frame(self.root)

        self.left_column.pack(expand=1,fill = BOTH)
        self.root_row1 = ttk.LabelFrame(self.left_column , text='Configure')
        self.root_row1.grid(row = 0 , column = 0 , sticky=W+E , pady = [5,0],padx=10)

        self.lbl_date = ttk.Label(self.root_row1 , text = 'Date : ')
        self.lbl_date.grid(row=0,column=0, padx = [10,0] , pady = 5)

        self.txt_date = ttk.DateEntry(self.root_row1)
        self.txt_date.grid(row=0,column=1, padx = 10 , pady = 10,sticky=W+E)

        self.lbl_class = ttk.Label(self.root_row1 , text = 'Class :')
        self.lbl_class.grid(row=0, padx = 10 , pady = 10,column=2)

        self.com_class = ttk.Combobox(self.root_row1 , state='readonly' , values=self.classes)
        self.com_class.grid(row=0, padx = 10 , pady = 10,sticky=W+E,column=3)

        self.lbl_lecture = ttk.Label(self.root_row1 , text = 'Lecture : ')
        self.lbl_lecture.grid(row=0, padx = 10 , pady = 10,column=4)

        self.com_lecture = ttk.Combobox(self.root_row1 , state='readonly' , values=[]) # lectures
        self.com_lecture.grid(row=0, padx = 10 , pady = 10,sticky=E+W,column=5)

        self.root_row1.columnconfigure(tuple(range(6)), weight=1)

        self.root_row1_1 = ttk.LabelFrame(self.left_column , text='Record : ')
        self.root_row1_1.grid(row = 1 , column = 0 , sticky = W+E)

        self.left_column.columnconfigure(0,weight=1,uniform=1)

        self.lbl_total = ttk.Label(self.root_row1_1 , text='Total Students : ' , font=myEnv.font_lbl)
        self.lbl_total.grid(row = 0 , column=0 , pady=10 , padx = 10 )

        self.lbl_total_val = ttk.Label(self.root_row1_1 , text='#### ' , font=("Helvetica",12,'bold'))
        self.lbl_total_val.grid(row = 0 , column=1 , pady=10 , padx = 10 )

        self.lbl_present = ttk.Label(self.root_row1_1 , text='Present : '  , font=myEnv.font_lbl)
        self.lbl_present.grid(row = 0 , column=2 , pady=10 , padx = 10 )

        self.lbl_present_val = ttk.Label(self.root_row1_1 , text='#### ' , font=("Helvetica",12,'bold'))
        self.lbl_present_val.grid(row = 0 , column=3 , pady=10 , padx = 10 )

        self.lbl_absent = ttk.Label(self.root_row1_1 , text='Absent : ' , font=myEnv.font_lbl)
        self.lbl_absent.grid(row = 0 , column=4 , pady=10 , padx = 10 )

        self.lbl_absent_val = ttk.Label(self.root_row1_1 , text='#### ' , font=("Helvetica",12,'bold'))
        self.lbl_absent_val.grid(row = 0 , column=5 , pady=10 , padx = 10 )

        self.lbl_leave = ttk.Label(self.root_row1_1 , text='Leave : ' , font=myEnv.font_lbl)
        self.lbl_leave.grid(row = 0 , column=6 , pady=10 , padx = 10 )

        self.lbl_leave_val = ttk.Label(self.root_row1_1 , text='#### ' , font=("Helvetica",12,'bold'))
        self.lbl_leave_val.grid(row = 0 , column=7 , pady=10 , padx = 10 )

        self.root_row1_1.columnconfigure(tuple(range(8)),weight=1)

        self.lbls_information = [
            self.lbl_total,
            self.lbl_total_val,
            self.lbl_present,
            self.lbl_present_val,
            self.lbl_absent,
            self.lbl_absent_val,
            self.lbl_leave,
            self.lbl_leave_val,
        ]

        for i in self.lbls_information:
            i.grid_forget()

        self.root_row2 = ttk.LabelFrame(self.left_column , text = 'Attendance : ')
 
        self.root_row3 = ttk.Frame(self.left_column)

        self.root_row_2 = ttk.Frame(self.left_column)
        self.root_row_2.grid(row = 3 , column = 0,pady=[68,10] , sticky = S+N+W+E,padx=10)

        self.root_row_3_3 = ttk.Frame(self.left_column)
        self.root_row_3_3.grid(row = 4 , column = 0 , sticky = W+E,padx=2)

        self.btn_save = ttk.Button(self.root_row_3_3,text='Save' , width=12)
        self.btn_save.pack(side='left',padx=10,pady=10)

        self.btn_reset = ttk.Button(self.root_row_3_3,text='Reset' , width=12 , command = lambda : self.show_class() )
        self.btn_reset.pack(side='left',padx=10,pady=10)

        self.btn_update = ttk.Button(self.root_row_3_3,text='Update' , width=12)
        self.btn_update.pack(side='left',padx=10,pady=10)

        self.btn_delete = ttk.Button(self.root_row_3_3,text='Delete' , width=12)
        self.btn_delete.pack(side='left',padx=10,pady=10)

        self.scrollx = ttk.Scrollbar(self.root_row_2 , orient='horizontal')
        self.scrolly = ttk.Scrollbar(self.root_row_2 , orient='vertical')
        self.scrolly.pack(side = 'right',fill='y')
        self.scrollx.pack(side = 'bottom',fill='x')

        self.tree = ttk.Treeview(self.root_row_2 , columns=self.columns,
                        xscrollcommand=self.scrollx.set,yscrollcommand=self.scrolly.set)
        self.tree.pack(fill=BOTH,expand=1)

        self.scrollx.config(command=self.tree.xview)
        self.scrolly.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("Sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("code" , text = 'Class' , anchor='w')
        self.tree.heading("lecture" , text = 'Lecture' , anchor='w')
        self.tree.heading("date" , text = 'Date' , anchor='w')
        self.tree.heading("students" , text = 'Students' , anchor='w')
        self.tree.heading("status" , text = 'Status' , anchor='w')

        self.tree.column('Sr' , width= 200 , anchor='w')
        self.tree.column('code' , width= 200 , anchor='w')
        self.tree.column('lecture' , width=200 , anchor='w')
        self.tree.column('date' , width=200 , anchor='w')
        self.tree.column('students' , width=200 , anchor='w')
        self.tree.column('status' , width=200 , anchor='w')

        self.legend = ttk.Label(self.root_row3 , text='' , font=14)
        self.legend.pack(side = 'right' , padx = 10)

        self.btn_save_prime = ttk.Button(self.root_row3 , text = 'Save' , width = 12 , command = self.add_attendance)
        self.btn_save_prime.pack(side = 'left' , padx = 10 , pady = 5)

        self.btn_clear_prime = ttk.Button(self.root_row3 , text = 'Reset' , width = 12 , command = self.reset_page1)
        self.btn_clear_prime.pack(side = 'left' , padx = 10 , pady = 5)

        self.btn_update_prime = ttk.Button(self.root_row3 , text = 'Update' , width = 12 , command = self.update_attendance)
        self.btn_update_prime.pack(side = 'left' , padx = 10 , pady = 5)

        self.btn_delete_prime = ttk.Button(self.root_row3 , text = 'Delete' , width = 12 , command=self.delete_attendance)
        self.btn_delete_prime.pack(side = 'left' , padx = 10 , pady = 5)

        self.btn_save_prime.configure(state='disabled')
        self.btn_delete_prime.configure(state='disabled')

        self.txt_date.bind("<<DateEntrySelected>>", self.record) 
        self.com_class.bind('<<ComboboxSelected>>', lambda e : self.get_lectures(e,clear=True))
        self.com_lecture.bind('<<ComboboxSelected>>', self.record)
        self.tree.bind("<Double-1>",self.recordCsv)
        
        #self.tree.bind("<ButtonRelease-1>",self.recordCsv) # for single click
        self.left_column.rowconfigure((3),weight=1)

        self.get_lectures(clear=True)
        self.get_lectures()
        self.show_attendance()
        self.show_class()


    def show_attendance(self,event=None):
        pass
    #########################################################################################

    def clear_classes(self):
        pass

    def make_tuples_to_list(self,data):
        newData =  [list(i) for i in data]
        return newData

    def add_item(self,data,item):
        pass

    def pop_first(self,data):
        pass

    def get_lectures(self,event=None,clear=True):
        pass

    def get_classes(self,event=None):
        pass

    def get_students(self,event=None):
        pass

    def get_studentsCsv(self,row):
        pass


    def update_attendance(self,event=None):
        pass

    def add_attendance(self,event=None):
        pass

    def reset_page1(self,event=None):
        pass

    def delete_attendance(self,event=None):
        pass

    def record(self,event=None,get=True,*args):
        pass

    def recordCsv(self,event=None,*args):
        pass

    def show_class(self,event=None):
        pass


    ############################################################################

if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    app = Attendance(root,ttk.Frame(root).pack())
    root.focus_set()
    root.mainloop()
