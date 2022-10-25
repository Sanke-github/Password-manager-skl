import tkinter
import mysql.connector #pip install  mysql-connector
from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import ImageTk,Image
from cryptography.fernet import Fernet #pip install cryptography
from tkinter import ttk
import pyperclip #pip install pyperclip
import random
import pybase64


mydb = mysql.connector.connect(host="localhost", user = "root",passwd = "",database = 'pwd')
mycursor = mydb.cursor()

def unsuccess_msg():
    return messagebox.showinfo("error", "passwords cannot match!")

def validateLogin(a,b,c):
    a = username.get()
    b = password.get()
    c = sitename.get()
    return c,a,b

def validate_2(u,p1,p2):
    u = username1.get()
    p1 = pwd1.get()
    p2 = pwd2.get()
    return u,p1,p2

def success_msg():
    return messagebox.showinfo("saved", "Saved Successfully")

def copy():
    return messagebox.showinfo("clipboard","Copied to clipboard!")
#window
tkWindow = Tk()  
tkWindow.geometry('450x240')  
tkWindow.title('pwd manager')
tkWindow.configure(bg='#12c4c0')

global i 
def display():
    new = Toplevel(tkWindow)
    new.title('display')
    new.geometry('240x240')
    new.config(bg ='#5A5A5A' )
    global i
    my_cursor=mycursor.execute("SELECT * FROM data limit 0,10")
    i = 1
    for pwd in mycursor:
        for j in range(len(pwd)):
            e = Label(new,text = pwd[j],bg ='#5A5A5A')
            e.grid(row = i,column = j)

        i = i+1

def new_pass():
    global w
    w=Frame(tkWindow,width=400,height=240,bg='#5A5A5A')
    w.place(x=50,y=28)
    #site label and text entry box
    sitelabel = Label(tkWindow, text = "Site Name : ",height = 1,bg = '#5A5A5A',width = 17,font=('consolas','10','bold'),fg = 'cyan').place(x = 200, y = 40)
    global sitename
    sitename = StringVar()
    siteEntry = Entry(tkWindow,textvariable=sitename).place(x = 200, y = 60)
    #username label and text entry box
    global username
    usernameLabel = Label(tkWindow, text="User Name : ",height = 1,width = 17,bg = '#5A5A5A',font=('consolas','10','bold'),fg = 'cyan').place(x = 200,y=80)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).place(x = 200, y = 100)  
    #password label and password entry box
    passwordLabel = Label(tkWindow,text="Password : ",height = 1,width  = 17,bg = '#5A5A5A',font=('consolas','10','bold'),fg = 'cyan').place(x = 200,y = 120)  
    global password
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').place(x=200,y = 140)  
    saveButton = Button(tkWindow, text="save", command=success_msg,border = 5,bg = '#28b3c4',font = ('consolas','11','bold')).place(x =  160,y=180)
    display_button = Button(tkWindow,text = 'display records',command = display,border = 5,bg = '#28b3c4',font = ('consolas','11','bold')).place(x =  250,y=180)
    return sitename,username,password

def encrypt():
    s = Toplevel(tkWindow)
    s.title('encrypt')
    s.geometry('1000x300')
    s.config(bg ='#5A5A5A' )
    elabel = Label(s,text = 'enter text to be encrypted : ',bg = '#5A5A5A',font=('consolas','20','bold'),fg = 'cyan').place(x =300 ,y=50)
    eentry = ttk.Entry(s,width = 40,font = ('consolas 10 bold'))
    eentry.place(x=350,y=90)
    global key
    key = Fernet.generate_key()
    global fernet
    fernet = Fernet(key)

    def getvalue():
        eeval = eentry.get()
        global encMessage
        encMessage = fernet.encrypt(eeval.encode())
        enC = 'The encrypted value is : \n {}'.format(encMessage)
        Label(s, text=enC, font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=20, ipady=20, padx=20, pady=20,fill=tkinter.BOTH, expand=True)
        pyperclip.copy(str(encMessage))
        Button(s,text= 'copy to clipboard',width = 15,border = 3,bg = '#19474D',command=copy).place(x=450,y=170)

    button = Button(s,text = 'encrypt!',command = getvalue,width = 10,border = 5,bg = '#5A5A5A').place(x =450,y = 120)
    
def delete():
    query = 'delete from data'
    mycursor.execute(query)
    mydb.commit()


def decrypt():
    z = Toplevel(tkWindow)
    z .title('decrypt')
    z.geometry('1000x300')
    z.config(bg ='#5A5A5A' )
    dlabel = Label(z,text = 'enter text to be decrypted : ',bg = '#5A5A5A',font=('consolas','20','bold'),fg = 'cyan').place(x =300 ,y=50)
    dentry = ttk.Entry(z,width = 85,font = ('consolas 10 bold'))
    dentry.place(x=230,y=90)
    
    def getvalue(): 
        deval = dentry.get()
        decMessage = fernet.decrypt(encMessage).decode()
        dnC = ('The decrypted value is : \n {} ').format(decMessage)
        Label(z, text=dnC, font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=20, ipady=20, padx=20, pady=20,fill=tkinter.BOTH, expand=True)
        
    button = Button(z,text = 'decrypt!',command = getvalue,width = 10,border = 5,bg = '#5A5A5A').place(x =450,y = 120)


def random_pass():
    x = Toplevel(tkWindow)
    x .title('generate a random password')
    x.geometry('450x240')
    x.config(bg ='#5A5A5A' )
    dlabel = Label(x,text = 'enter difficulty of the password : ',bg = '#5A5A5A',font=('consolas','11','bold'),fg = 'cyan').place(x =100 ,y=50)
    button = Button(x,text = 'easy!',width = 10,border = 5,bg = '#5A5A5A').place(x =450,y = 120)
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()<>.,"
    def pwd():
        for i in range(0,5):
            password = ""
            for i in range(0,5):
                password_char = random.choice(char[:52])
                password = password + password_char
        q = 'your password is : {}'.format(password)
        Label(x,text = q,font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=10, ipady=10, padx=10, pady=10,fill=tkinter.BOTH, expand=True)
        B = Button(x,text= 'copy to clipboard',width = 15,border = 3,bg = '#19474D',command=copy)
        B.place(x =170,y = 140)
        pyperclip.copy(password)

    def pwd0():
        for i in range(0,10):
            password = ""
            for i in range(0,10):
                password_char = random.choice(char[:62])
                password = password + password_char
        q = 'your password is : {}'.format(password)
        Label(x,text = q,font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=10, ipady=10, padx=10, pady=10,fill=tkinter.BOTH, expand=True)
        B = Button(x,text= 'copy to clipboard',width = 15,border = 3,bg = '#19474D',command=copy)
        B.place(x =170,y = 140)
        pyperclip.copy(password)

    def pwd1():
        for i in range(0,15):
            password = ""
            for i in range(0,15):
                password_char = random.choice(char)
                password = password + password_char
        q = 'your password is : {}'.format(password)
        Label(x,text = q,font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=10, ipady=10, padx=10, pady=10,fill=tkinter.BOTH, expand=True)
        B = Button(x,text= 'copy to clipboard',width = 15,border = 3,bg = '#19474D',command=copy)
        B.place(x =170,y = 140)
        pyperclip.copy(password)

    Button(x,text = 'easy',command = pwd,width = 10,border = 5,bg = '#5A5A5A').place(x =75,y = 120)
    Button(x,text = 'medium',command = pwd0,width = 10,border = 5,bg = '#5A5A5A').place(x =180,y = 120)
    Button(x,text = 'hard',command = pwd1,width = 10,border = 5,bg = '#5A5A5A').place(x=295,y=120)  # type: ignore


def toggle_win():
    f1=Frame(tkWindow ,width=250,height=500,bg='#12c4c0')
    f1.place(x=0,y=0)


    #buttons
    def bttn(x,y,text,bcolor,fcolor,cmd):
     
        def on_entera(e):
            myButton1['background'] = bcolor #ffcc66
            myButton1['foreground']= '#5A5A5A'  #000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground']= '#5A5A5A'

        myButton1 = Button(f1,text=text,
                       width=35,
                       height=2,
                       fg='#262626',
                       border=0,
                       bg=fcolor,
                       activeforeground='#262626',
                       activebackground=bcolor,            
                        command=cmd)
                      
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x,y=y)

    bttn(0,43,'E N C R Y P T','#0f9d9a','#12c4c0',encrypt)
    bttn(0,80,'D E C R Y P T ','#0f9d9a','#12c4c0',decrypt)
    bttn(0,117,'G E N E R A T E   A   P A S S W O R D ','#0f9d9a','#12c4c0',random_pass)
    bttn(0,154,'D E L E T E   R E C O R D S ','#0f9d9a','#12c4c0',delete)

    #
    def dele():
        f1.destroy()

    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png"))

    Button(f1,
           image=img2,
           border=0,
           command=dele,
           bg='#12c4c0',
           activebackground='#12c4c0').place(x=0,y=0)
    

img1 = ImageTk.PhotoImage(Image.open("open5.png"))

Button(tkWindow,image=img1,
       command=toggle_win,
       border=0,
       bg='#12c4c0',
       activebackground='#12c4c0').place(x=0,y=0)

def update_password():
    w=Frame(tkWindow,width=400,height=240,bg='#28b3c4')
    w.place(x=50,y=28)
    #site label and text entry box
    usernamelabel = Label(tkWindow, text = "User name : ",height = 1,bg = '#28b3c4',width = 17,font=('consolas','10','bold')).place(x = 200, y = 40)
    global username1
    username1 = StringVar()
    userentry = Entry(tkWindow,textvariable=username1).place(x = 200, y = 60)
    #username label and text entry box
    usernameLabel = Label(tkWindow, text="Old password : ",height = 1,width = 17,bg = '#28b3c4',font=('consolas','10','bold')).place(x = 200,y=80)
    global pwd1
    pwd1 = StringVar()
    pwd1Entry = Entry(tkWindow, textvariable=pwd1).place(x = 200, y = 100)  

    #password label and password entry box
    passwordLabel = Label(tkWindow,text="New password : ",height = 1,width  = 17,bg = '#28b3c4',font=('consolas','10','bold')).place(x = 200,y = 120)  
    global pwd2
    pwd2 = StringVar()
    pwd2Entry = Entry(tkWindow, textvariable=pwd2, show='*').place(x=200,y = 140)  
    saveButton = Button(tkWindow, text="save", command=success_msg,border = 5,bg = '#5A5A5A').place(x =  240,y=180) 
    return username1,pwd1,pwd2

l,m,n  = update_password()
validate_2 = partial(validate_2,l,m,n)

e,f,g = new_pass()
validateLogin = partial(validateLogin,e,f,g)

Button(tkWindow,width=28,height=0,text='U P D A T E   P A S S W O R D',pady=4,border=0, command = update_password,bg='#28b3c4',fg='black',activebackground='dark red',activeforeground='white').place(x=250,y=0)
Button(tkWindow,width=28,height=0,text='S T O R E  P A S S W O R D',pady=4,border=0, command = new_pass,bg='#5A5A5A',fg='cyan',activebackground='#EFAD29',activeforeground='white').place(x=50,y=0)


tkWindow.mainloop()
n,p,o = validateLogin()
mycursor = mydb.cursor()

d,r,s = validate_2()
print(d,r,s)

query = "INSERT INTO data(site_name,user_name,password)values('{}','{}','{}')".format(n,p,o)
mycursor.execute(query)
mydb.commit()


query = "UPDATE data SET password = %s WHERE  user_name = %s"
val=(s,d)
mycursor.execute(query,val)
mydb.commit()

mycursor.execute("select * from data")
for i in  mycursor:
    print(i)
