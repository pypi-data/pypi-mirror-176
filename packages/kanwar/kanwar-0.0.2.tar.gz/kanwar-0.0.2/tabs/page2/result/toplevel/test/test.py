# Import Widgets
from tkinter import BOTH , NO , StringVar , Toplevel
import ttkbootstrap as ttk
from kanwar import MessageBox
from kanwar import envVars as myEnv
from kanwar import Department

class Test:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        #####################
        #VARS
        self.dcourse = StringVar()
        self.dcourse_code = StringVar()
        self.dlecture = StringVar()
        self.dname_test = StringVar()
        self.dtotal_marks_test = StringVar()
        self.dpassing_marks_test = StringVar()
        self.dname_test_desc = StringVar()
        self.ddate_test = StringVar()
        #####################
        self.classes = [] 
        self.lectures= []
        self.tests = []

        self.makeGUI()
        self.show_class()
        self.show_test()

        self.root.bind("<Return>",self.add_test)
        self.root.bind("<Control-u>",self.update_test)
        self.root.bind("<Control-d>",self.delete_test)
        self.root.bind("<Control-r>",self.reset_test)
        self.root.bind("<Control-s>",self.export_test)
        self.root.bind("<Control-f>",lambda e  : self.txt_search_test.focus_set())

        self.root.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.root.wait_window()


    def quit_me(self,e=None):
        op = MessageBox('Confirm',"Do you really wish to close this tab?",b1='Yes',b2='No')
        if op.choice=='Yes':
            self.root.destroy()

    def setClassTab(self,classTab):
        self.classTab = classTab

    def makeGUI(self,event=None):
        self.root = Toplevel(self.grandMaster)
        self.root.minsize(940,600)

        self.root.geometry("940x600+50+80")
        self.root.focus()

        self.main_frame  = ttk.LabelFrame(self.root , text='Test Configurations')
        self.main_frame.pack(expand=1,fill='both' , padx = 10 , pady = 10)

        self.first_frame = ttk.Frame(self.main_frame)
        self.first_frame.pack(side='top',fill='x')

        self.lbl_test_name = ttk.Label(self.first_frame , text= 'Test Name :')
        self.lbl_test_name.grid(row=0 , column = 0 , padx=10 , pady=10)

        self.txt_test_name = ttk.Entry(self.first_frame , textvariable=self.dname_test)
        self.txt_test_name.grid(row=0 , column = 1 , padx=10 , pady=10 , sticky='ew')

        self.lbl_test_name_desc = ttk.Label(self.first_frame , text= 'Description :')
        self.lbl_test_name_desc.grid(row=0 , column = 2 , padx=10 , pady=10)

        self.txt_test_name_desc = ttk.Entry(self.first_frame , textvariable=self.dname_test_desc)
        self.txt_test_name_desc.grid(row=0 , column = 3 , padx=10 , pady=10 , sticky='ew',columnspan=3)

        self.lbl_date = ttk.Label(self.first_frame , text= 'Date :')
        self.lbl_date.grid(row=1 , column = 0 , padx=10 , pady=10)


        self.ent_date = ttk.DateEntry(self.first_frame , width=18)
        self.ent_date.grid(row=1 , column = 1 , padx=10 , pady=10 , sticky='ew')

        self.lbl_class = ttk.Label(self.first_frame, text='Class Code  :   ')
        self.lbl_class.grid(row=1 , column = 2 , padx=10 , pady=10)

        self.com_class_test = ttk.Combobox(self.first_frame , values=self.classes, width=18,state='readonly')
        self.com_class_test.grid(row=1 , column = 3 , padx=10 , pady=10 , sticky='ew')

        self.lbl_lecture = ttk.Label(self.first_frame, text='Lecture : ')
        self.lbl_lecture.grid(row=1 , column = 4 , padx=10 , pady=10)

        self.com_lecture_test = ttk.Combobox(self.first_frame , values=self.lectures, width=18,state='readonly')
        self.com_lecture_test.grid(row=1 , column = 5 , padx=10 , pady=10 , sticky='ew')

        self.com_class_test.bind("<<ComboboxSelected>>",self.get_lectures_for_test)

        self.lbl_total_marks = ttk.Label(self.first_frame,text='Total Marks : ')
        self.lbl_total_marks.grid(row=2 , column = 0 , padx=10 , pady=10)

        self.txt_total_marks = ttk.Entry(self.first_frame , textvariable=self.dtotal_marks_test)
        self.txt_total_marks.grid(row=2 , column = 1 , padx=10 , pady=10 , sticky='ew')

        self.lbl_passing_marks = ttk.Label(self.first_frame,text='Passing Marks : ')
        self.lbl_passing_marks.grid(row=2 , column = 2 , padx=10 , pady=10)

        self.txt_passing_marks = ttk.Entry(self.first_frame,textvariable=self.dpassing_marks_test)
        self.txt_passing_marks.grid(row=2 , column = 3 , padx=10 , pady=10 , sticky='ew')

        self.first_frame.columnconfigure((0,1,2,3,4,5) , weight=1)

        self.second_frame = ttk.Frame(self.main_frame)
        self.second_frame.pack(expand=1,fill='both')

        #### Row 1

        self.scrollx_test = ttk.Scrollbar(self.second_frame , orient='horizontal')
        self.scrolly_test = ttk.Scrollbar(self.second_frame , orient='vertical')
        self.scrolly_test.pack(side = 'right',fill='y')
        self.scrollx_test.pack(side = 'bottom',fill='x')

        self.class_columns_test = ('sr','test','test_desc' , 'code','subject','date','total_marks','passing_marks') 

        self.tree = ttk.Treeview(self.second_frame , columns=self.class_columns_test,
                        xscrollcommand=self.scrollx_test.set,yscrollcommand=self.scrolly_test.set)
        self.tree.pack(fill=BOTH,expand=1)

        self.scrollx_test.config(command=self.tree.xview)
        self.scrolly_test.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("test" , text = 'Test Title' , anchor='w')
        self.tree.heading("test_desc" , text = 'Test' , anchor='w')
        self.tree.heading("code" , text = 'Class' , anchor='w')
        self.tree.heading("subject" , text = 'Lecture' , anchor='w')
        self.tree.heading("date" , text = 'Date' , anchor='w')
        self.tree.heading("total_marks" , text = 'Total Marks' , anchor='w')
        self.tree.heading("passing_marks" , text = 'Passing Marks' , anchor='w')

        self.tree.column('sr' , width=200 , anchor='w')
        self.tree.column('test' , width=200 , anchor='w')
        self.tree.column('test_desc' , width=200 , anchor='w')
        self.tree.column('code' , width=200 , anchor='w')
        self.tree.column('subject' , width=200 , anchor='w')
        self.tree.column('date' , width=200 , anchor='w')
        self.tree.column('total_marks' , width=200 , anchor='w')
        self.tree.column('passing_marks' , width=200 , anchor='w')

        #### Row 3
        ######## BUTTONS 
        self.third_frame = ttk.Frame(self.main_frame)
        self.third_frame.pack(fill = 'x' , padx = [0,0] , pady = [10,10])

        self.btn_add_test = ttk.Button(self.third_frame, text = 'Save' , width = 12,command=self.add_test)
        self.btn_add_test.pack(side = 'left' , padx = 10)

        self.btn_clear_test = ttk.Button(self.third_frame , text = 'Reset' , width = 12,command=self.reset_test)
        self.btn_clear_test.pack(side = 'left' , padx  = 10)

        self.btn_update_test = ttk.Button(self.third_frame , text = 'Update' , width = 12,command=self.update_test)
        self.btn_update_test.pack(side = 'left' , padx = 10)

        self.btn_delete_test = ttk.Button(self.third_frame , text = 'Delete' , width = 12,command=self.delete_test)
        self.btn_delete_test.pack(side = 'left' , padx = 10)

        self.btn_sort_test = ttk.Button(self.third_frame , text = 'Sort' , width = 12,state='disabled')
        self.btn_sort_test.pack(side = 'left' , padx = 10)

        self.btn_export_test = ttk.Button(self.third_frame , text = 'Export' , width = 12,command=self.export_test)
        self.btn_export_test.pack(side = 'left' , padx = 10)

        self.txt_search_test = ttk.Entry(self.third_frame)
        self.txt_search_test.pack(side='left',padx=10,pady=10,fill='x',expand=1)

        self.txt_search_test.bind("<KeyPress>",self.search_test)

        self.btn_update_test.configure(state='disabled')
        self.btn_delete_test.configure(state='disabled')
        self.get_lectures_for_test()
        self.tree.bind("<ButtonRelease-1>",self.getdata_test)

        ###############################################################################

    def make_tuples_to_list(self,data):
        newData =  [list(i) for i in data]
        return newData

    def get_lectures_for_test(self,event=None):
        pass

    def show_test(self,event=None):
        pass

    def search_test(self,event=None):
        pass


    def export_test(self,event=None):
        pass

    ###############################################################################################
    def getdata_test(self,event=None):
        pass

    def reset_test(self,event=None):
        pass

    ####################################### FUNCTIONS ##############################################
    def update_data(self,event=None):
        pass

    def update_test(self,event=None):
        pass

    def delete_test(self,event=None):
        pass

    def add_test(self,event=None):
        pass

    def show_class(self,event=None):
        pass


    ###############################################################################

if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    frame = Frame(root)
    frame.pack()
    testTab = Test(root,frame)
    #testTab.setClassTab(classTab)
    root.mainloop()

