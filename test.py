# import required modules
import datetime
import hashlib
import os
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import math

# create connection to sqlite to create db
connection = sqlite3.connect('employee.db')
cursor = connection.cursor()

hours = 8
clock = None


# cursor.execute('CREATE TABLE staff(name, password_salt, password_hash, time, days_present, total_working_days)')

# class app which contains blueprint of app. has four frames - homepage, login, signup and employee
class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry('360x500')
        self.homepage()

    def homepage(self):
        # this line of code destroys/erases the other frames before rendering the homepage frame
        for i in self.master.winfo_children():
            i.destroy()
        # create frame and other widgets for the gui
        self.frame1 = Frame(self.master, width=360, height=500)
        self.frame1.pack()
        self.title_text = ttk.Label(self.frame1, text='ETS App')
        self.title_text.grid(row=0, column=1, padx=5, pady=5)
        self.reg_text = ttk.Label(self.frame1, text='Ministry of Surveillance\n\nEmployee Tracker System')
        self.reg_text.grid(row=1, column=1, padx=5, pady=5)
        self.register_btn = ttk.Button(self.frame1, text='Sign In', command=self.login)
        self.register_btn.grid(row=4, column=1, padx=5, pady=5)

    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = Frame(self.master, width=360, height=500)
        self.frame2.pack()
        self.reg_text = ttk.Label(self.frame2, text='Welcome Back\n\nSign-into your account')
        self.reg_text.grid(row=0, column=1)
        self.sign_in_username_label = Label(self.frame2, text='Username')
        self.sign_in_username_label.grid(row=1, column=0)
        self.sign_in_username_input = Entry(self.frame2)
        self.sign_in_username_input.grid(row=1, column=1)
        self.sign_in_password_label = Label(self.frame2, text='Password')
        self.sign_in_password_label.grid(row=2, column=0)
        self.sign_in_password_input = Entry(self.frame2)
        self.sign_in_password_input.grid(row=2, column=1)
        self.sign_in_button = ttk.Button(self.frame2, text='Sign-In', command=self.sign_in)
        self.sign_in_button.grid(row=3, column=1)
        self.register_text = ttk.Label(self.frame2, text="Don't have an account? Create one!")
        self.register_text.grid(row=4, column=1)
        self.register_btn = ttk.Button(self.frame2, text='Create Account', command=self.register)
        self.register_btn.grid(row=5, column=1)

    def register(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master, width=360, height=500)
        self.frame3.pack()
        self.reg_text2 = ttk.Label(self.frame3, text='Create new Account')
        self.reg_text2.pack()
        self.register_username_label = Label(self.frame3, text='Username')
        self.register_username_label.pack()
        self.register_username_input = Entry(self.frame3)
        self.register_username_input.pack()
        self.password_label = Label(self.frame3, text='Password')
        self.password_label.pack()
        self.password_input = Entry(self.frame3)
        self.password_input.pack()
        self.confirm_password_label = Label(self.frame3, text='Confirm Password')
        self.confirm_password_label.pack()
        self.confirm_password_input = Entry(self.frame3)
        self.confirm_password_input.pack()
        self.register_button = Button(self.frame3, text='Register', command=self.register_new_user)
        self.register_button.pack()
        self.login_btn = ttk.Button(self.frame3, text='Sign-In', command=self.login)
        self.login_btn.pack()

    def employee(self, username):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master, width=360, height=500)
        self.frame3.pack()
        self.reg_text2 = ttk.Label(self.frame3, text=f'Welcome {username}')
        self.reg_text2.pack()
        self.canvas = Canvas(self.frame3, width=200, height=224, highlightthickness=0)
        self.tomato_image = PhotoImage(file='tomato.png')
        self.canvas.create_image(100, 112, image=self.tomato_image)
        self.timer_text = self.canvas.create_text(100, 130, text='08:00:00', fill='white', font=('Courier', 35, 'bold'))
        self.canvas.pack()
        self.start_button = Button(self.frame3, text='Start', command=self.start_cmd)
        self.start_button.pack()
        self.login_btn = ttk.Button(self.frame3, text='Log Out', command=self.login)
        self.login_btn.pack()

    def sign_in(self):
        username = self.sign_in_username_input.get()
        password = self.sign_in_password_input.get()
        if self.check_username(username):
            if self.validate_password(username, password):
                messagebox.showinfo('Login Successful')
                self.employee(username)
            else:
                messagebox.showerror('Wrong Password')
                self.login()
        else:
            messagebox.showerror('Incorrect Username')
            self.login()

    def check_username(self, username):
        cursor.execute('SELECT * FROM staff where name=?', (username,))
        result = cursor.fetchone()
        if result:
            print(result)
            return True
        else:
            return False

    def validate_password(self, username, password):
        cursor.execute('SELECT password_salt, password_hash FROM staff WHERE name=?', (username,))
        result = cursor.fetchone()
        if result:
            salt = result[0]
            stored_hash_password = result[1]
            hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()
            if hashed_password == stored_hash_password:
                return True
            else:
                return False

    def register_new_user(self):
        username = self.register_username_input.get()
        password = self.password_input.get()
        confirm_password = self.confirm_password_input.get()
        salt = hashlib.sha256(os.urandom(16)).hexdigest().encode('utf-8')
        hashed_password = hashlib.pbkdf2_hmac('sha256', confirm_password.encode('utf-8'), salt, 100000).hex()
        current_time = datetime.datetime.now()
        print(current_time)
        working_days = 270
        days_present = 0
        if password == confirm_password:
            data = [
                (username, salt, hashed_password, current_time, days_present, working_days)
            ]
            cursor.executemany('INSERT INTO staff VALUES(?,?,?,?,?,?)', data)
            connection.commit()
            self.employee(username)
        elif password != confirm_password:
            messagebox.showerror("Passwords don't match")
            self.register()

    def start_cmd(self):
        self.work_hours = hours * 60 * 60
        self.count_down(self.work_hours)

    def count_down(self, count):
        count_hrs = math.floor((count / 60) / 60)
        count_min = math.floor((count / 60) / 8)
        count_sec = count % 60

        if count_sec < 10:
            count_sec = f'0{count_sec}'
        self.canvas.itemconfig(self.timer_text, text=f'{count_hrs}:{count_min}:{count_sec}')
        if count > 0:
            global clock
            clock = root.after(1000, self.count_down, count - 1)
        else:
            self.start_cmd()


root = Tk()
app(root)
root.mainloop()
