import tkinter as tk
from tkinter import ttk
import sqlite3

def perform_calculation(*args):
    if len(args) != 3:
        return "Error: Not enough arguments"
    
    operation, num1_str, num2_str = args
    
    try:
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        return "Error: Invalid number input"
    
    if operation == "Add":
        return num1 + num2
    elif operation == "Subtract":
        return num1 - num2
    elif operation == "Multiply":
        return num1 * num2
    elif operation == "Divide":
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2
    else:
        return "Error: Unknown operation"

def calculate():
    operation = operation_var.get()
    num1 = entry_num1.get()
    num2 = entry_num2.get()
    result = perform_calculation(operation, num1, num2)
    result_label.config(text=f"Result: {result}")
    if isinstance(result, (int, float)):
        save_result(result)

def clear_fields():
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)
    operation_cb.current(0)
    result_label.config(text="Result:")
    entry_num1.focus()

def save_result(result):
    conn = sqlite3.connect('calculator.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL)")
    cursor.execute("INSERT INTO results (value) VALUES (?)", (result,))
    cursor.execute("SELECT id, value FROM results ORDER BY id DESC LIMIT 5")
    recent = cursor.fetchall()
    conn.commit()
    conn.close()
    update_saved_answers(recent)

def load_recent_results():
    conn = sqlite3.connect('calculator.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL)")
    cursor.execute("SELECT id, value FROM results ORDER BY id DESC LIMIT 5")
    recent = cursor.fetchall()
    conn.close()
    return recent

def update_saved_answers(recent):
    for widget in saved_answers_frame.winfo_children():
        widget.destroy()
    ttk.Label(saved_answers_frame, text="Recent Answers:").grid(row=0, column=0, sticky=tk.W, pady=(0,5))
    for idx, (id, value) in enumerate(recent, start=1):
        btn = ttk.Button(saved_answers_frame, text=str(value), command=lambda val=value: use_saved_value(val))
        btn.grid(row=idx, column=0, sticky=tk.W, pady=2)

def use_saved_value(value):
    focused_widget = root.focus_get()
    if focused_widget == entry_num1:
        entry_num1.delete(0, tk.END)
        entry_num1.insert(0, str(value))
    elif focused_widget == entry_num2:
        entry_num2.delete(0, tk.END)
        entry_num2.insert(0, str(value))
    else:
        entry_num2.delete(0, tk.END)
        entry_num2.insert(0, str(value))

root = tk.Tk()
root.title("Simple Calculator App")

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Number 1:").grid(column=0, row=0, sticky=tk.W)
entry_num1 = ttk.Entry(frame, width=15)
entry_num1.grid(column=1, row=0)

ttk.Label(frame, text="Number 2:").grid(column=0, row=1, sticky=tk.W)
entry_num2 = ttk.Entry(frame, width=15)
entry_num2.grid(column=1, row=1)

ttk.Label(frame, text="Operation:").grid(column=0, row=2, sticky=tk.W)
operation_var = tk.StringVar()
operation_cb = ttk.Combobox(frame, textvariable=operation_var, values=["Add", "Subtract", "Multiply", "Divide"])
operation_cb.grid(column=1, row=2)
operation_cb.current(0)

button_frame = ttk.Frame(frame)
button_frame.grid(column=0, row=3, columnspan=2, pady=10)

calc_button = ttk.Button(button_frame, text="Calculate", command=calculate)
calc_button.grid(column=0, row=0, padx=5)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_fields)
clear_button.grid(column=1, row=0, padx=5)

result_label = ttk.Label(frame, text="Result:")
result_label.grid(column=0, row=4, columnspan=2)

saved_answers_frame = ttk.Frame(frame)
saved_answers_frame.grid(column=0, row=5, columnspan=2, pady=10, sticky=tk.W)

recent_results = load_recent_results()
update_saved_answers(recent_results)

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

entry_num1.focus()

root.mainloop()
