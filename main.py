import mysql.connector
import tkinter as tk
from tkinter import ttk
import json  
import mysql.connector  


with open('true.json') as json_file:  
    data = json.load(json_file)  


columns = []  
for item in data:  
    ip_address = item.split(' - - ')[0]  
    request_time = item.split('[')[1].split(']')[0]  
    status_code = item.split('" ')[1].split(' ')[0]  
    user_agent = item.split('"')[len(item.split('"'))-2]  
    columns.append((ip_address, request_time, status_code, user_agent))  


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)  


c = conn.cursor()  


c.execute('''CREATE TABLE IF NOT EXISTS my_table
             (ip_address TEXT, request_time TEXT, status_code TEXT, user_agent TEXT)''')  


c.executemany('INSERT INTO my_table VALUES (%s, %s, %s, %s)', columns)  



conn.commit() 
conn.close()  



def filter_data():
    
    keyword = entry_filter.get().strip()
    
    
    table.delete(*table.get_children())
    
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = connection.cursor()
    
    
    cursor.execute("SELECT * FROM my_table WHERE ip_address LIKE %s OR request_time LIKE %s OR status_code LIKE %s OR user_agent LIKE %s",
                   ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    

    for row in rows:
        table.insert("", tk.END, text="", values=row)
    
    
    connection.close()

#
def filter_by_status_code():
    
    table.delete(*table.get_children())
    
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = connection.cursor()
    
    
    cursor.execute("SELECT * FROM my_table WHERE status_code = %s", ('200',))
    rows = cursor.fetchall()
    

    for row in rows:
        table.insert("", tk.END, text="", values=row)
    
    
    connection.close()
#

win = tk.Tk()
win.title("Практика")
win.geometry("400x400")


frame_filter = tk.Frame(win)
frame_filter.pack(pady=10)


label_filter = tk.Label(frame_filter, text="Filter:")
label_filter.pack(side=tk.LEFT)

entry_filter = tk.Entry(frame_filter)
entry_filter.pack(side=tk.LEFT, padx=5)


button_filter = tk.Button(frame_filter, text="Apply Filter", command=filter_data, background="#fff5db")
button_filter.pack(side=tk.LEFT)

#
button_filter_by_status_code = tk.Button(win, text="Filter by Status Code 200", command=filter_by_status_code, background="#fff5db")
button_filter_by_status_code.pack(pady=10)
#

table = ttk.Treeview(win)
table["columns"] = ("ip_address", "request_time", "status_code", "user_agent")
table.column("#0", width=0, stretch=tk.NO)
table.column("ip_address", anchor=tk.CENTER, width=120)
table.column("request_time", anchor=tk.CENTER, width=120)
table.column("status_code", anchor=tk.CENTER, width=80)
table.column("user_agent", anchor=tk.CENTER, width=180)

table.heading("#0", text="")
table.heading("ip_address", text="IP Address")
table.heading("request_time", text="Request Time")
table.heading("status_code", text="Status Code")
table.heading("user_agent", text="User Agent")

table.pack(fill=tk.BOTH, expand=True)

table.configure(style="Custom.Treeview")
style = ttk.Style(win)
style.configure("Custom.Treeview", background="#fff5db")



connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
cursor = connection.cursor()


cursor.execute("SELECT * FROM my_table")
rows = cursor.fetchall()

for row in rows:
    table.insert("", tk.END, text="", values=row)


connection.close()


win.mainloop()