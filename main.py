import tkinter as tk
from tkinter import ttk
import sqlite3


def is_valid_name(name):
    return not any(char.isdigit() for char in name)


def is_valid_phone(phone):
    return not any(char.isalpha() for char in phone)


def on_full_name_entry_change(event):
    full_name = full_name_entry.get()
    if not is_valid_name(full_name):
        error_label.config(text="Имя не должно содержать цифры")
    else:
        error_label.config(text="")


def on_phone_number_entry_change(event):
    phone_number = phone_number_entry.get()
    if not is_valid_phone(phone_number):
        phone_error_label.config(text="Номер телефона не должен содержать буквы")
    else:
        phone_error_label.config(text="")


def search_employee():
    keyword = search_entry.get()

    for row in employee_tree.get_children():
        employee_tree.delete(row)

    cursor.execute("SELECT * FROM employees WHERE full_name LIKE ?", ('%' + keyword + '%',))
    employees = cursor.fetchall()

    for employee in employees:
        employee_tree.insert("", "end", values=employee[1:])


def delete_employee():
    selected_item = employee_tree.selection()
    if selected_item:
        full_name = employee_tree.item(selected_item, "values")[0]
        cursor.execute("DELETE FROM employees WHERE full_name = ?", (full_name,))
        conn.commit()
        refresh_employee_list()
    else:
        error_label.config(text="Выберите сотрудника для удаления")


conn = sqlite3.connect("employee_database.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
''')
conn.commit()


def add_employee():
    full_name = full_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    cursor.execute("INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)",
                   (full_name, phone_number, email, salary))
    conn.commit()

    full_name_entry.delete(0, "end")
    phone_number_entry.delete(0, "end")
    email_entry.delete(0, "end")
    salary_entry.delete(0, "end")

    refresh_employee_list()


def refresh_employee_list():
    for row in employee_tree.get_children():
        employee_tree.delete(row)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    for employee in employees:
        employee_tree.insert("", "end", values=employee[1:])


root = tk.Tk()
root.title("Управление списком сотрудников компании")

employee_tree = ttk.Treeview(root, columns=("Full Name", "Phone Number", "Email", "Salary"), show="headings")
employee_tree.heading("Full Name", text="Full Name")
employee_tree.heading("Phone Number", text="Phone Number")
employee_tree.heading("Email", text="Email")
employee_tree.heading("Salary", text="Salary")
employee_tree.pack()

full_name_label = tk.Label(root, text="Full Name:")
full_name_label.pack()
full_name_entry = tk.Entry(root)
full_name_entry.pack()

full_name_entry.bind("<KeyRelease>", on_full_name_entry_change)

phone_number_label = tk.Label(root, text="Phone Number:")
phone_number_label.pack()
phone_number_entry = tk.Entry(root)
phone_number_entry.pack()

phone_number_entry.bind("<KeyRelease>", on_phone_number_entry_change)

email_label = tk.Label(root, text="Email:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

salary_label = tk.Label(root, text="Salary:")
salary_label.pack()
salary_entry = tk.Entry(root)
salary_entry.pack()

add_button = tk.Button(root, text="Добавить сотрудника", command=add_employee)
add_button.pack()

search_label = tk.Label(root, text="Поиск (ФИО):")
search_label.pack()
search_entry = tk.Entry(root)
search_entry.pack()

search_button = tk.Button(root, text="Поиск", command=search_employee)
search_button.pack()

delete_button = tk.Button(root, text="Удалить сотрудника", command=delete_employee)
delete_button.pack()

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

phone_error_label = tk.Label(root, text="", fg="red")
phone_error_label.pack()

refresh_employee_list()

root.mainloop()