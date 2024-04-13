# import required modules
import datetime
import hashlib
import os
import sqlite3
import random
from tkinter import *
from tkinter import ttk, messagebox
import math
import geocoder

# create connection to sqlite to create db
connection = sqlite3.connect('employee.db')
cursor = connection.cursor()

hours = 8
clock = None

cursor.execute(
    'CREATE TABLE IF NOT EXISTS staff(id VARCHAR(255), name VARCHAR(255), password_salt VARCHAR(255), password_hash VARCHAR(255), sign_in_date VARCHAR(255), days_present INTEGER, total_working_days INTEGER DEFAULT 0, is_admin INTEGER DEFAULT 0)')
cursor.execute(
    'CREATE TABLE IF NOT EXISTS attendance(date VARCHAR(255), name VARCHAR(255), time VARCHAR(255)), location VARCHAR(255))')


class app:
    """class app which contains blueprint of app. has four frames - homepage, login, signup and employee. It enables admins to be created and deleted"""

    def __init__(self, master):
        self.master = master
        self.master.geometry('400x650')
        # opens homepage frame when file is executed
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

    # displays the frame for logging into account
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

    # displays the register frame to create a new account 
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

    # once user is logged in, the employee frame is displayed 
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

    def admin(self, username):
        """This contains the frame for displaying the admin interface for the administrator or administrators of the
        interface"""
        cursor.execute('SELECT * FROM staff where name=?', (username,))
        result = cursor.fetchone()
        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master, width=360, height=500)

        # designing admin frame
        self.Top = Frame(self.master, width=360, height=50, bd=9, relief='raised')
        self.Top.pack(side=TOP)
        self.Button_Group = Frame(root, width=300, height=50, bd=8, relief="raised")
        self.Button_Group.pack(side=TOP)
        self.Buttons = Frame(self.Button_Group, width=300, height=20)
        self.Buttons.pack(side=LEFT)
        self.Button1 = Frame(self.Button_Group, width=300, height=20)
        self.Button1.pack(side=RIGHT)
        self.Body = Frame(self.master, width=360, height=700, bd=8, relief="raised")
        self.Body.pack(side=BOTTOM)

        # ========label widget =============
        self.txt_title = Label(self.Top, width=300, font=('arial', 24), text=f'Welcome {username}')
        self.txt_title.pack()

        # =============buttons ==================
        self.btn_display = Button(self.Buttons, width=15, text='Attendance',
                                  command=lambda: self.admin_view_staff_attendance(username))
        self.btn_display.pack(side=LEFT)
        self.btn_insert = Button(self.Buttons, text='All Staff', command=self.staff_table)
        self.btn_insert.pack(side=RIGHT)
        self.btn_insert = Button(self.Buttons, text='Create New Admin', command=lambda: self.create_admin(username))
        self.btn_insert.pack(side=RIGHT)
        self.btn_delete = Button(self.Buttons, text='Delete Staff', command=lambda: self.admin_delete(username))
        self.btn_delete.pack(side=RIGHT)

        # ==================List Widget ================
        self.scrollbarY = Scrollbar(self.Body, orient=VERTICAL)
        self.scrollbarX = Scrollbar(self.Body, orient=HORIZONTAL)
        self.tree = ttk.Treeview(self.Body, columns=('Staff ID', 'Full Name', 'Days Present'),
                                 selectmode='extended',
                                 height=300,
                                 yscrollcommand=self.scrollbarY.set, xscrollcommand=self.scrollbarX.set)
        self.scrollbarY.config(command=self.tree.yview)
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        self.scrollbarX.config(command=self.tree.xview)
        self.scrollbarX.pack(side=BOTTOM, fill=X)
        self.tree.heading('Staff ID', text='Staff ID', anchor=W)
        self.tree.heading('Full Name', text='Full Name', anchor=W)
        self.tree.heading('Days Present', text='Days Present', anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=NO, minwidth=0, width=100)
        self.tree.column('#3', stretch=NO, minwidth=0, width=100)

        self.tree.pack(side=LEFT)

    def admin_view_staff_attendance(self, username):
        """This function helps to view the frame containing the table for the attendance of employees"""
        cursor.execute('SELECT * FROM staff where name=?', (username,))
        result = cursor.fetchone()
        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master, width=360, height=500)

        # designing admin frame
        self.Top = Frame(self.master, width=360, height=50, bd=9, relief='raised')
        self.Top.pack(side=TOP)
        self.Button_Group = Frame(root, width=360, height=50, bd=8, relief="raised")
        self.Button_Group.pack(side=TOP)
        self.Buttons = Frame(self.Button_Group, width=360, height=20)
        self.Buttons.pack(side=LEFT)
        self.Button1 = Frame(self.Button_Group, width=360, height=20)
        self.Button1.pack(side=RIGHT)
        self.Body = Frame(self.master, width=360, height=700, bd=8, relief="raised")
        self.Body.pack(side=BOTTOM)

        # ========label widget =============
        self.txt_title = Label(self.Top, width=300, font=('arial', 24), text=f'Welcome {username}')
        self.txt_title.pack()

        # =============buttons ==================
        self.btn_home = Button(self.Buttons, width=15, text='Admin Homepage', command=lambda: self.admin(username))
        self.btn_home.pack(side=LEFT)
        self.btn_display = Button(self.Buttons, width=15, text='View Attendance', command=self.attendance_table)
        self.btn_display.pack(side=LEFT)

        # ==================List Widget ================
        self.scrollbary = Scrollbar(self.Body, orient=VERTICAL)
        self.scrollbarx = Scrollbar(self.Body, orient=HORIZONTAL)
        self.plant = ttk.Treeview(self.Body, columns=('Date', 'Full Name', 'Reporting Time'), selectmode='extended',
                                  height=300,
                                  yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)
        self.scrollbary.config(command=self.plant.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.scrollbarx.config(command=self.plant.xview)
        self.scrollbarx.pack(side=BOTTOM, fill=X)
        self.plant.heading('Date', text='Date', anchor=W)
        self.plant.heading('Full Name', text='Full Name', anchor=W)
        self.plant.heading('Reporting Time', text='Reporting Time', anchor=W)
        self.plant.column('#0', stretch=NO, minwidth=0, width=0)
        self.plant.column('#1', stretch=NO, minwidth=0, width=100)
        self.plant.column('#2', stretch=NO, minwidth=0, width=100)
        self.plant.column('#3', stretch=NO, minwidth=0, width=100)
        self.plant.pack(side=LEFT)

    def create_admin(self, username):
        """This function helps to create new administrators"""
        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master, width=360, height=500)
        self.frame3.pack()
        self.reg_text2 = ttk.Label(self.frame3, text='Create New Admin')
        self.reg_text2.pack()
        self.admn_view = Button(self.frame3, text='Back to Admin Homepage', command=lambda: self.admin(username))
        self.admn_view.pack(side=LEFT)
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
        self.register_button = Button(self.frame3, text='Register', command=self.register_new_admin)
        self.register_button.pack(side=LEFT)
        self.login_btn = ttk.Button(self.frame3, text='Sign-In', command=self.login)
        self.login_btn.pack(side=RIGHT)

    def admin_delete(self, username):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = Frame(self.master, width=360, height=500)
        self.reg_text = ttk.Label(self.frame2, text='Enter Username to be deleted')
        self.reg_text.grid(row=0, column=1, padx=5, pady=5)
        self.delete_query = Entry(self.frame2)
        self.delete_query.grid(row=1, column=1, padx=5, pady=5)
        self.delete_query.insert(0, 'Username')
        self.delete_button = ttk.Button(self.frame2, text='Delete User', command=self.delete_staff)
        self.delete_button.grid(row=3, column=1, padx=5, pady=5)
        self.admn_view = ttk.Button(self.frame2, text='Home', command=lambda: self.admin(username))
        self.admn_view.grid(row=4, column=1, padx=5, pady=5)
        self.frame2.grid(row=0, column=0, sticky='nsew', padx=45, pady=5)

    # function to handle signing into account of user
    def sign_in(self):
        # get() receives and stores input as variables username and password
        username = self.sign_in_username_input.get()
        password = self.sign_in_password_input.get()

        # the datetime module is used to get the current date and time
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        current_date = date_time.strftime('%x')

        # if statement to measure if current time is equal to given time
        if "05:00:00" <= current_time <= '23:00:00':
            if self.check_username(username):

                if self.validate_password(username, password):

                    cursor.execute('SELECT sign_in_date FROM staff WHERE name=?', (username,))
                    result = cursor.fetchone()

                    if result:
                        last_login = result[0]

                        if last_login != current_date:
                            cursor.execute('SELECT days_present FROM staff WHERE name=?', (username,))
                            result = cursor.fetchone()
                            num_of_days = result[0]

                            num_of_days += 1
                            cursor.execute('UPDATE staff SET days_present=? WHERE name=?', (num_of_days, username))
                            location = geocoder.ip('me').latlng

                            data = [
                                (current_date, username, current_time, location)
                            ]
                            cursor.executemany('INSERT INTO attendance VALUES(?,?,?,?)', data)
                            connection.commit()

                        else:
                            cursor.execute('UPDATE staff SET sign_in_date=? WHERE name=?', (current_date, username))

                    messagebox.showinfo('Login Successful')

                    cursor.execute('SELECT is_admin FROM staff WHERE name=?', (username,))
                    result = cursor.fetchone()
                    is_admin = result[0]

                    if is_admin == 1:
                        self.admin(username)
                    elif is_admin == 0:
                        self.employee(username)
                else:
                    messagebox.showerror('Wrong Password')
                    self.login()
            else:
                messagebox.showerror('Incorrect Username')
                self.login()
        else:
            # if time of sign in isn't 5: am - 5pm, user can't sign in 
            messagebox.showinfo('Sign In', 'You can only sign into your account from 5am to 5pm. Try again later!')

    def check_username(self, username):
        """ Function to check database if the given username exists. It returns true where user exists and false,
        where it doesn't"""
        cursor.execute('SELECT * FROM staff where name=?', (username,))
        result = cursor.fetchone()
        if result:
            print(result)
            return True
        else:
            return False

    def validate_password(self, username, password):
        """ Validate Password checks the salt and hashed password given by the user against the salted and hashed
        password of the user saved in the db"""
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

    def register_new_admin(self):
        """This function receives the input from the admin frame and uses it to create a new administrator"""
        username = self.register_username_input.get()
        password = self.password_input.get()
        confirm_password = self.confirm_password_input.get()
        salt = hashlib.sha256(os.urandom(16)).hexdigest().encode('utf-8')
        hashed_password = hashlib.pbkdf2_hmac('sha256', confirm_password.encode('utf-8'), salt, 100000).hex()
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        print(current_time)
        id_num = random.randint(1, 200)
        employee_id = f'emp_{id_num}'
        working_days = 270
        days_present = 0

        cursor.execute('SELECT * FROM staff WHERE name=?', (username,))
        result = cursor.fetchone()
        if result:
            messagebox.showerror('Registration Error', 'Username already taken')
            self.register()
        else:
            if password == confirm_password:
                data = [
                    (employee_id, username, salt, hashed_password, current_time, days_present, working_days, 1)
                ]
                cursor.executemany('INSERT INTO staff VALUES(?,?,?,?,?,?,?,?)', data)
                connection.commit()
                messagebox.showinfo('New Admin', 'New Admin Successfully Created')
            elif password != confirm_password:
                messagebox.showerror("Passwords don't match")
                self.create_admin()

    def register_new_user(self):
        """ This function receives new user input, salts and hashed the password, along with time of sign in and
        saves it into the database staff table"""
        username = self.register_username_input.get()
        password = self.password_input.get()
        confirm_password = self.confirm_password_input.get()
        salt = hashlib.sha256(os.urandom(16)).hexdigest().encode('utf-8')
        hashed_password = hashlib.pbkdf2_hmac('sha256', confirm_password.encode('utf-8'), salt, 100000).hex()
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        print(current_time)
        id_num = random.randint(1, 200)
        employee_id = f'emp_{id_num}'
        working_days = 270
        days_present = 0

        # CHECK IF ANY ADMIN USER EXISTS IN DATABASE
        cursor.execute('SELECT COUNT(*) FROM staff WHERE is_admin = 1')
        admin_count = cursor.fetchone()[0]
        if admin_count == 0:
            is_admin = True
            # check if username exists in database
            cursor.execute('SELECT * FROM staff WHERE name=?', (username,))
            result = cursor.fetchone()
            if result:
                messagebox.showerror('Registration Error', 'Username already taken')
                self.register()
            else:
                if password == confirm_password:
                    data = [
                        (employee_id, username, salt, hashed_password, current_time, days_present, working_days, 1)
                    ]
                    cursor.executemany('INSERT INTO staff VALUES(?,?,?,?,?,?,?,?)', data)
                    connection.commit()
                    self.admin(username)
                elif password != confirm_password:
                    messagebox.showerror("Passwords don't match")
                    self.register()
        else:
            # normal registration for non-admin users
            cursor.execute('SELECT * FROM staff WHERE name=?', (username,))
            result = cursor.fetchone()
            if result:
                messagebox.showerror('Registration Error', 'Username already taken')
                self.register()
            else:
                if password == confirm_password:
                    data = [
                        (employee_id, username, salt, hashed_password, current_time, days_present, working_days, 0)
                    ]
                    cursor.executemany('INSERT INTO staff VALUES(?,?,?,?,?,?,?,?)', data)
                    connection.commit()
                    self.employee(username)
                elif password != confirm_password:
                    messagebox.showerror("Passwords don't match")
                    self.register()

    def start_cmd(self):
        """ This function checks the time when button was clicked against the given time condition. if condition
        returns true, variable containing work hours is passed into the count down function, else,  an error message
        is displayed"""
        self.work_hours = hours * 60 * 60
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        if current_time >= '08:00:00' and current_time <= '17:00:00':
            self.count_down(self.work_hours)
        else:
            messagebox.showerror('Not Yet Time', 'Timer can only be started at 8am')

    def count_down(self, count):
        """Function receives count value in seconds, and is converted to hours and minutes and seconds that can be
        displayed onto screen"""
        count_hrs = math.floor((count / 60) / 60)
        count_min = math.floor((count % 3600) / 60)
        count_sec = count % 60

        # python's dynamic typing enables a string to be attached to an integer '
        if count_sec < 10:
            count_sec = f'0{count_sec}'
        if count_min < 10:
            count_min = f'0{count_min}'
        # canvas text is configured to display the time values
        self.canvas.itemconfig(self.timer_text, text=f'{count_hrs}:{count_min}:{count_sec}')
        if count > 0:
            global clock
            # tkinter's after() is used to reduce the work hours value, by 1 each second
            clock = root.after(1000, self.count_down, count - 1)
        else:
            self.start_cmd()

    def reset_cmd(self):
        """ Reset button cancels the count down and displays the time as 0s """
        global clock
        root.after_cancel(clock)
        self.canvas.itemconfig(self.timer_text, text=f'00:00:00')
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        if current_time >= '17:00:00':
            root.after_cancel(clock)
            self.canvas.itemconfig(self.timer_text, text=f'00:00:00')
        elif "09:00:00" < current_time < "17:00:00":
            messagebox.showwarning('Not Yet 5pm', 'It is not yet time to close from work')

    def logout(self):
        """ Function checks time when button is clicked, and if it matches the given condition, a goodbye message
        is displayed and user is logged out, else, Error message is displayed"""
        date_time = datetime.datetime.now()
        current_time = date_time.strftime('%X')
        if current_time >= '17:00:00':
            messagebox.showinfo('Goodbye for Now', 'Have a pleasant evening, and see you tomorrow')
            self.homepage()
        else:
            messagebox.showwarning('Not Yet 5pm', 'It is not yet time to close from work')

    def attendance_table(self):
        """These lines of code populates the admin table to enable the admin view the signin logs of the employees"""
        self.plant.delete(*self.plant.get_children())
        cursor.execute('SELECT * FROM attendance')
        fetch = cursor.fetchall()

        for data in fetch:
            self.plant.insert('', 'end', values=(data[0], data[1], data[2]))

    def staff_table(self):
        """This function populates the admin frame to enable the admin view all staff registered on the database"""
        self.tree.delete(*self.tree.get_children())
        cursor.execute('SELECT * FROM staff')
        fetch = cursor.fetchall()

        for data in fetch:
            self.tree.insert('', 'end', values=(data[0], data[1], data[5]))

    def delete_staff(self):
        """This function removes a user from the database"""
        user = self.delete_query.get()
        cursor.execute('SELECT * FROM staff WHERE name=?', (user,))
        result = cursor.fetchone()
        if result:
            cursor.execute('DELETE FROM staff WHERE name=?', (user,))
            connection.commit()
            messagebox.showinfo('Delete Staff From Database', f'{user} successfully deleted from database')
        else:
            messagebox.showerror('Delete Staff From Database', f'{user} not found in database')
        print(user)


root = Tk()
root.config(padx=10, pady=5)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
app(root)
root.mainloop()
