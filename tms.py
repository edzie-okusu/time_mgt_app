from tkinter import *
from tkinter import messagebox
import sqlite3
import datetime

connection = sqlite3.connect('employee.db')
cursor = connection.cursor()

# cursor.execute('CREATE TABLE staff(name, password, time, days_present, total_working_days)')

response = cursor.execute('SELECT name FROM sqlite_master')
print(response.fetchone())
def register():
    username = register_username_input.get()
    password = password_input.get()
    current_time = datetime.datetime.now()
    print(current_time)
    working_days = 270
    days_present = 0
    data = [
        (username, password, current_time, days_present, working_days)
    ]
    cursor.executemany('INSERT INTO staff VALUES(?,?,?,?,?)', (data))
    connection.commit()

def check_username(username, password):
    find_user = ('SELECT * FROM staff where name=? AND password=?')
    cursor.execute(find_user, [username, password])
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
def login():
    username = sign_in_username_input.get()
    password = sign_in_password_input.get()
    if check_username(username, password):
        messagebox.showinfo('Login Successful')
    else:
        messagebox.showerror('Incorrect username of password')

# UI INTERFACE
window = Tk()
window.title('Employee Time Management System')
window.minsize(width=360, height=720)

register_username_label = Label(window, text='Username')
register_username_label.pack()
register_username_input = Entry(window)
register_username_input.pack()
password_label = Label(window, text='Password')
password_label.pack()
password_input = Entry(window)
password_input.pack()
register_button = Button(window, text='Register', command=register)
register_button.pack()
sign_in_username_label = Label(window, text='Username')
sign_in_username_label.pack()
sign_in_username_input = Entry(window)
sign_in_username_input.pack()
sign_in_password_label = Label(window, text='Password')
sign_in_password_label.pack()
sign_in_password_input = Entry(window)
sign_in_password_input.pack()
sign_in_button = Button(window, text='Sign-In', command=login)
sign_in_button.pack()

window.mainloop()