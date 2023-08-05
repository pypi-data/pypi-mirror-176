# Import Widgets
import ttkbootstrap as ttk
from tkinter import BOTH , StringVar , NO
from kanwar import MessageBox
from kanwar import envVars as myEnv

class Staff:
    def __init__(self,grandMaster,master):
        self.grandMaster = grandMaster
        self.master = master
        self.classes = [] 
        self.lectures = []
        self.root = ttk.LabelFrame(self.master , text = 'Staff Management')
        self.root.pack(fill = BOTH, expand=1)

        self.dteacher_name = StringVar()
        self.demail = StringVar()
        self.dpassword = StringVar()

        self.left_column_page5 = ttk.Frame(self.root)
        self.left_column_page5.pack(expand=1,fill = BOTH)

        #### Row 1
        self.left_column_page5_row1 = ttk.Frame(self.left_column_page5)
        self.left_column_page5_row1.pack(side = 'top' , fill = 'x', padx = 10)

        self.lbl_class_page5 = ttk.Label(self.left_column_page5_row1 , text='Class Code :   ')
        self.lbl_class_page5.grid(row=0,column=0,pady=10)

        self.com_class_page5 = ttk.Combobox(self.left_column_page5_row1 , state='readonly',values=self.classes , width=23)
        self.com_class_page5.grid(row=0,column=1,pady=10)

        self.lbl_lecture_page5 = ttk.Label(self.left_column_page5_row1, text='Lecture : ')
        self.lbl_lecture_page5.grid(row=0,column=2,pady=10)

        self.com_lecture_page5 = ttk.Combobox(self.left_column_page5_row1 , state='readonly' , values=self.lectures, width = 23)
        self.com_lecture_page5.grid(row=0,column=3,pady=10)

        self.lbl_role = ttk.Label(self.left_column_page5_row1 , text = 'Role : ')
        self.lbl_role.grid(row=0,column=4)

        self.com_roles = ('Admin','Teacher','Assistant')

        self.com_role = ttk.Combobox(self.left_column_page5_row1 , state='readonly',values=self.com_roles , width = 23)
        self.com_role.grid(row=0,column=5)

        self.com_class_page5.bind('<<ComboboxSelected>>', lambda e :self.get_lectures_for_staff(e))

        self.lbl_teacher_name = ttk.Label(self.left_column_page5_row1 , text = 'Teacher Name : ')
        self.lbl_teacher_name.grid(row=1,column=0,pady=10)

        self.txt_teacher_name = ttk.Entry(self.left_column_page5_row1 , width = 25 , textvariable=self.dteacher_name)
        self.txt_teacher_name.grid(row=1,column=1,pady=10)

        self.lbl_email = ttk.Label(self.left_column_page5_row1 , text = 'Email Address : ')
        self.lbl_email.grid(row=1,column=2,pady=10)

        self.txt_email = ttk.Entry(self.left_column_page5_row1 , width = 25 , textvariable=self.demail)
        self.txt_email.grid(row=1,column=3,pady=10)

        self.lbl_password = ttk.Label(self.left_column_page5_row1 , text = 'Password : ')
        self.lbl_password.grid(row=1,column=4,pady=10)

        self.txt_password = ttk.Entry(self.left_column_page5_row1 , width = 25 , textvariable=self.dpassword)
        self.txt_password.grid(row=1,column=5,pady=10)

        self.left_column_page5_row1.columnconfigure((0,1,2,3,4,5),weight=1)

        self.left_column_page5_row2 = ttk.Frame(self.left_column_page5)
        self.left_column_page5_row2.pack(fill = 'both' , padx = 10 , pady = [10,20], expand=1)

        self.scrollx_page5 = ttk.Scrollbar(self.left_column_page5_row2 , orient='horizontal')
        self.scrolly_page5 = ttk.Scrollbar(self.left_column_page5_row2 , orient='vertical')
        self.scrolly_page5.pack(side = 'right',fill='y')
        self.scrollx_page5.pack(side = 'bottom',fill='x')

        self.class_columns_page5 = ('Sr','name','role','code','lecture','email','pass') 

        self.tree = ttk.Treeview(self.left_column_page5_row2 , columns=self.class_columns_page5,
                        xscrollcommand=self.scrollx_page5.set,yscrollcommand=self.scrolly_page5.set)
        self.tree.pack(fill=BOTH,expand=1)

        self.scrollx_page5.config(command=self.tree.xview)
        self.scrolly_page5.config(command=self.tree.yview)

        self.tree.column("#0" , width = 0 , stretch=NO)

        self.tree.heading("Sr" , text = 'Sr.' , anchor='w')
        self.tree.heading("name" , text = 'Name' , anchor='w')
        self.tree.heading("role" , text = 'Role' , anchor='w')
        self.tree.heading("code" , text = 'Class',anchor='w')
        self.tree.heading("lecture" , text = 'Lecture' , anchor='w')
        self.tree.heading("email" , text = 'Email' , anchor='w')
        self.tree.heading("pass" , text = 'Password' , anchor='w')

        self.tree.column('Sr' , width=200 , anchor='w')
        self.tree.column('code' , width=200 , anchor='w')
        self.tree.column('lecture' , width=200 , anchor='w')
        self.tree.column('name' , width=200 , anchor='w')
        self.tree.column('role' , width=200 , anchor='w')
        self.tree.column('email' , width=200 , anchor='w')
        self.tree.column('pass' , width=200 , anchor='w')

        self.tree["displaycolumns"]=('Sr', 'code' , 'lecture' , 'name' , 'role' , 'email')

        #### Row 3
        ######## BUTTONS 

        self.left_column_page5_row3 = ttk.Frame(self.left_column_page5)
        self.left_column_page5_row3.pack(fill = 'x' , padx = [0,0] , pady = [0,10])

        self.btn_add_page5 = ttk.Button(self.left_column_page5_row3, text = 'Save' , width = 12 , command=self.add_user)
        self.btn_add_page5.pack(side = 'left' , padx = 10)

        self.btn_clear_page5 = ttk.Button(self.left_column_page5_row3 , text = 'Reset' , width = 12 , command=self.reset_user)
        self.btn_clear_page5.pack(side = 'left' , padx  = 10)

        self.btn_update_page5 = ttk.Button(self.left_column_page5_row3 , text = 'Update' , width = 12 , command=self.update_user)
        self.btn_update_page5.pack(side = 'left' , padx = 10)

        self.btn_delete_page5 = ttk.Button(self.left_column_page5_row3 , text = 'Delete' , width = 12 , command=self.delete_user)
        self.btn_delete_page5.pack(side = 'left' , padx = 10)

        self.btn_sort_page5 = ttk.Button(self.left_column_page5_row3 , text = 'Sort' , width = 12 , command=self.sort_user)
        self.btn_sort_page5.pack(side = 'left' , padx  = 10)

        self.btn_export_page5 = ttk.Button(self.left_column_page5_row3 , text = 'Export' , width = 12 , command=self.export_user)
        self.btn_export_page5.pack(side = 'left' , padx  = 10)

        self.txt_search_page5= ttk.Entry(self.left_column_page5_row3)
        self.txt_search_page5.pack(side='left',padx=10,fill='x',expand=1)

        self.txt_search_page5.bind('<KeyPress>',self.search_user)
        self.btn_update_page5.configure(state='disabled')
        self.btn_delete_page5.configure(state='disabled')
        self.btn_sort_page5.configure(state='disabled')

        self.tree.bind("<ButtonRelease-1>",self.getdata_user)
        self.show_class()
        self.show_user()
    ###############################################################################################

    def make_tuples_to_list(self,data):
        newData =  [list(i) for i in data]
        return newData

    def get_lectures_for_staff(self,event=None):
        pass

    def show_user(self,event=None):
        pass

    def show_user2(self,event=None):
        pass

    def sort_user(self,event=None):
        pass

    def export_user(self,event=None):
        pass

    def getdata_user(self,event=None):
        pass

    def reset_user(self,event=None):
        pass

    def reset_user2(self,event=None):
        pass

    def search_user(self,event=None):
        pass

    ####################################### FUNCTIONS ##############################################
    ###############################################################################

    def delete_user(self,event=None):
        pass

    def update_user(self,event=None):
        pass

    def add_user(self,event=None):
        pass

    def show_class(self,event=None):
        pass


    ###############################################################################

if __name__ == "__main__":
    root = ttk.Window('Kanwar Adnan','united')
    root.focus_set()
    app = Staff(root,ttk.Frame(root).pack())
    root.mainloop()

