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


# cursor.execute('CREATE TABLE staff(id VARCHAR(255), name VARCHAR(255), password_salt VARCHAR(255), password_hash VARCHAR(255), time VARCHAR(255), days_present int, total_working_days int)')
cursor.execute('CREATE TABLE attendance(name VARCHAR(255), time VARCHAR(255)')
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
        self.title_text = ttk.Label(self.frame1, text='ETS App')
        self.title_text.grid(row=0, column=1, padx=5, pady=5)
        self.reg_text = ttk.Label(self.frame1, text='Ministry of Surveillance\n\nEmployee Tracker System')
        self.reg_text.grid(row=1, column=1, padx=5, pady=5)
        self.register_btn = ttk.Button(self.frame1, text='Sign In', command=self.login)
        self.register_btn.grid(row=4, column=1, padx=5, pady=5)
        self.frame1.grid(column=0, row=0, sticky='nsew', padx=45, pady=5)

    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = Frame(self.master, width=360, height=500)
        self.reg_text = ttk.Label(self.frame2, text='Welcome Back\n\nSign-into your account')
        self.reg_text.grid(row=0, column=1, padx=5, pady=5)
        # self.sign_in_username_label = Label(self.frame2, text='Username')
        # self.sign_in_username_label.grid(row=1, column=0, padx=5, pady=5)
        self.sign_in_username_input = Entry(self.frame2)
        self.sign_in_username_input.grid(row=1, column=1, padx=5, pady=5)
        self.sign_in_username_input.insert(0, 'Username')
        # self.sign_in_password_label = Label(self.frame2, text='Password')
        # self.sign_in_password_label.grid(row=2, column=0, padx=5, pady=5)
        self.sign_in_password_input = Entry(self.frame2)
        self.sign_in_password_input.grid(row=2, column=1, padx=5, pady=5)
        self.sign_in_password_input.insert(0, 'Password')
        self.sign_in_button = ttk.Button(self.frame2, text='Sign-In', command=self.sign_in)
        self.sign_in_button.grid(row=3, column=1, padx=5, pady=5)
        self.register_text = ttk.Label(self.frame2, text="Don't have an account? Create one!")
        self.register_text.grid(row=4, column=1, padx=5, pady=5)
        self.register_btn = ttk.Button(self.frame2, text='Create Account', command=self.register)
        self.register_btn.grid(row=5, column=1, padx=5, pady=5)
        self.frame2.grid(row=0, column=0, sticky='nsew', padx=45, pady=5)

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
        cursor.execute('SELECT * FROM staff where name=?', (username,))
        result = cursor.fetchone()
        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master, width=360, height=500)
        self.frame3.grid(column=0, row=0, sticky='nsew', padx=40, pady=5)
        self.reg_text2 = ttk.Label(self.frame3, text=f'Welcome {username}')
        self.reg_text2.grid(column=1, row=0)
        self.num_of_days = ttk.Label(self.frame3, text=f'Days Present: {result[5]}')
        self.num_of_days.grid(column=1, row=1)
        self.canvas = Canvas(self.frame3, width=200, height=224, highlightthickness=0)
        self.tomato_image = PhotoImage(file='tomato.png')
        self.canvas.create_image(100, 112, image=self.tomato_image)
        self.timer_text = self.canvas.create_text(100, 130, text='08:00:00', fill='white', font=('Courier', 35, 'bold'))
        self.canvas.grid(column=1, row=2)
        self.start_button = Button(self.frame3, text='Start', command=self.start_cmd)
        self.start_button.grid(column=0, row=3)
        self.reset_button = Button(self.frame3, text='Reset', command=self.reset_cmd)
        self.reset_button.grid(column=0, row=4, padx=5, pady=5)
        self.logout_btn = ttk.Button(self.frame3, text='Log Out', command=self.logout)
        self.logout_btn.grid(column=1, row=5)

    def sign_in(self):
        username = self.sign_in_username_input.get()
        password = self.sign_in_password_input.get()
        date_time =datetime.datetime.now()
        current_time = date_time.strftime('%X')
        if "05:00:00" <= current_time <= '17:00:00':
            if self.check_username(username):
                if self.validate_password(username, password):
                    cursor.execute('SELECT days_present FROM staff WHERE name=?', (username,))
                    result = cursor.fetchone()
                    num_of_days = result[0]
                    num_of_days += 1
                    cursor.execute('UPDATE staff SET days_present=? WHERE name=?', (num_of_days, username))
                    print(type(num_of_days))
                    messagebox.showinfo('Login Successful')
                    self.employee(username)
                else:
                    messagebox.showerror('Wrong Password')
                    self.login()
            else:
                messagebox.showerror('Incorrect Username')
                self.login()
        else:
            messagebox.showinfo('Sign In', 'You can only sign into your account from 5am to 5pm. Try again later!')

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
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        print(current_time)
        id_num = 1
        if id_num >= 1:
            id_num += 1
        employee_id = f'emp_{id_num}'
        working_days = 270
        days_present = 0
        if password == confirm_password:
            data = [
                (employee_id, username, salt, hashed_password, current_time, days_present, working_days)
            ]
            cursor.executemany('INSERT INTO staff VALUES(?,?,?,?,?,?,?)', data)
            connection.commit()
            self.employee(username)
        elif password != confirm_password:
            messagebox.showerror("Passwords don't match")
            self.register()

    def start_cmd(self):
        self.work_hours = hours * 60 * 60
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        if current_time >= '08:00:00' and current_time <= '17:00:00':
            self.count_down(self.work_hours)
        else:
            messagebox.showerror('Not Yet Time', 'Timer can only be started at 8am')

    def count_down(self, count):
        count_hrs = math.floor((count / 60) / 60)
        count_min = math.floor((count % 3600) / 60)
        count_sec = count % 60

        if count_sec < 10:
            count_sec = f'0{count_sec}'
        if count_min < 10:
            count_min = f'0{count_min}'
        self.canvas.itemconfig(self.timer_text, text=f'{count_hrs}:{count_min}:{count_sec}')
        if count > 0:
            global clock
            clock = root.after(1000, self.count_down, count - 1)
        else:
            self.start_cmd()

    def reset_cmd(self):
        global clock
        root.after_cancel(clock)
        self.canvas.itemconfig(self.timer_text, text=f'00:00:00')
        # date_time = datetime.datetime.now()
        # current_time = date_time.strftime('%X')
        # if current_time >= '17:00:00':
        #     root.after_cancel(clock)
        #     self.canvas.itemconfig(self.timer_text, text=f'00:00:00')
        # else:
        #     messagebox.showwarning('Not Yet 5pm', 'It is not yet time to close from work')

    def logout(self):
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        if current_time >= '17:00:00':
            messagebox.showinfo('Goodbye for Now', 'Have a pleasant evening, and see you tomorrow')
            self.homepage()
        else:
            messagebox.showwarning('Not Yet 5pm', 'It is not yet time to close from work')


root = Tk()
root.config(padx=10, pady=5)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
app(root)
root.mainloop()
