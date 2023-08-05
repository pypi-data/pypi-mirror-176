from kanwar import MessageBox
from kanwar import Login_Page
from kanwar import SignUp_Page
from tkinter import Toplevel , BOTH
from time import strftime

DATABASE = "Database.db"
DATABASEATTENDNACE = "Database2.db"

DEFAULT_ROLE = 'Admin'
DEFAULT_ADMIN = 'admin'
DEFAULT_PASSWORD = '123'
DEFAULT_EMAIL = 'admin'
DEFAULT_CLASS = 'IT-G2'
DEFAULT_LECTURE = 'DLD'

DEFAULT_ROLE_USER = 'Teacher'

LOGGER = 'Admin'

def Login_System(root,nb):
    root.withdraw()

    page_login = Toplevel(root)
    page_login.geometry("660x200+200+200")
    page_login.resizable(False,False)

    page_login_object = Login_Page(page_login)
    page_login_object.pack(expand=1,fill='both')
    page_login_object.txt_pass.configure(show="*")

    def Sign_up_page(event=None):
        page_login.withdraw()

        page_signup = Toplevel(page_login)
        page_signup.focus()
        page_signup.geometry("660x240+200+200")
        page_signup.resizable(False,False)

        page_signup_object = SignUp_Page(page_signup)
        page_signup_object.pack(expand=1,fill='both',padx= 10 , pady =10)
        page_signup_object.txt_name.focus()

        page_signup_object.txt_pass.configure(show="*")
        page_signup_object.txt_cpass.configure(show="*")
        def create_account():
            pass
        page_signup_object.btn_create.configure(command=create_account)
        def del_window(event=None):
            page_login.deiconify()
            page_signup.destroy()
        page_signup.protocol("WM_DELETE_WINDOW",del_window)
        page_signup.wait_window()

    def confirm_login(event=None):
        pass
    # ASSIGNING CUSTOM FUNCTIONS TO BUTTONS
    page_login_object.btn_sign_up.configure(command=Sign_up_page)
    page_login_object.btn_sign_in.configure(command=confirm_login)

    # LAST THING TO BIND
    page_login.protocol("WM_DELETE_WINDOW",lambda : root.destroy())
    page_login.after(100,lambda : page_login.focus_set())
    page_login.wait_window()
    return LOGGER

def check_previous_Login(root,nb):
    pass
def redirect(user,password,root,nb):
    pass

if __name__ == '__main__':
     # IMPORT MODERN TTK LIB
    from ttkbootstrap import Style

    # MAKING IT'S OBJECT SETTINGS
    style = Style('united')

    # MAKING ROOT OBJECT    
    root = style.master
    root.withdraw()
    root.title("Kanwar Adnan")
    MessageBox("Information","Authentication system of Kanwar Adnan (Kanwaradnanrajput@gmail.com)",b2='Close')