import tkinter as tk
import sqlite3
from tkinter import ttk
#Creating main window
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.view_main()
        self.db = db
        self.view_record()
    #Method for displaying the main window
    def view_main(self):
        #Toolbar
        toolbar = tk.Frame(bg = 'black', bd = 2)
        toolbar.pack(side = tk.TOP, fill = tk.X)
        #Buttons for the tools panel
        btn_add = tk.Button(toolbar, text = 'Добавить сотрудника', bg = 'grey', fg = 'white', bd = 0, command = self.open_add, cursor = 'hand2')
        btn_add.pack(padx = 9, side = tk.LEFT)
        btn_del = tk.Button(toolbar, text = 'Удалить сотрудника', bg = 'grey', fg = 'white', bd = 0, command = self.delete, cursor = 'hand2')
        btn_del.pack(padx = 9, side = tk.LEFT)
        btn_edit = tk.Button(toolbar, text = 'Изменить запись о сотруднике', bg = 'grey', bd = 0, fg = 'white', command = self.open_edit, cursor = 'hand2')
        btn_edit.pack(padx = 9, side = tk.LEFT)
        btn_search = tk.Button(toolbar, text = 'Поиск сотрудников', bg = 'grey', fg = 'white', bd = 0, command = self.open_search, cursor = 'hand2')
        btn_search.pack(padx = 9, side = tk.LEFT)
        btn_refresh = tk.Button(toolbar, text = 'Перезагрузить', bg = 'grey', bd = 0, fg = 'white', command = self.view_record)
        btn_refresh.pack(padx = 9, side = tk.LEFT)
        #Creating table
        self.tree = ttk.Treeview(
            root,
            columns = ('id', 'name', 'phone', 'email'),
            show = 'headings',
            height = 45
            )
        
        self.tree.column('id', width = 30, anchor = tk.CENTER)
        self.tree.column('name', width = 300, anchor = tk.CENTER)
        self.tree.column('phone', width = 150, anchor = tk.CENTER)
        self.tree.column('email', width = 150, anchor = tk.CENTER)
        self.tree.heading('id', text = 'id')
        self.tree.heading('name', text = 'ФИО сотрудника')
        self.tree.heading('phone', text = 'Номер телефона')
        self.tree.heading('email', text = 'E-mail')
        self.tree.pack()
    #Method of deleting a record
    def delete(self):
        for i in self.tree.selection():
            id = self.tree.set(i, '#1')
            self.db.delete_data(id)
        self.db.conn.commit()
        self.view_record()
    #Method of searching records
    def search(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM personal WHERE name LIKE ?', 
                            ('%' + name + '%',))
        
        for i in self.db.cur.fetchall():
            self.tree.insert('', 'end', values = i)
    #Method of changing records
    def edit(self, name, phone, mail):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute(
            '''
                UPDATE personal SET name = ?, phone = ?, email = ? WHERE id = ?
            ''', (name, phone, mail, id)
        )
        self.db.conn.commit()
        self.view_record()
    
    # Method of displaying records
    def view_record(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM personal')
        [self.tree.insert('', 'end', values = i) for i in self.db.cur.fetchall()]
        
    # Method for opening the Add Records window
    def open_add(self):
        Add()
    # Method of opening the record search window
    def open_search(self):
        Search()
    # Method of opening the Record Change window
    def open_edit(self):
        Edit()
# Creating an Add window
class Add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.view_add()
    # Method of displaying the add window
    def view_add(self):
        self.title('Добавление сотрудника')
        self.resizable(False, False)
        self.geometry('400x200')
        self.grab_set()
        self.focus()
        # Captions to input windows
        self.label_name = tk.Label(self, text = 'ФИО')
        self.label_name.place(x = 50, y = 50)
        self.label_tel = tk.Label(self, text = 'Телефон')
        self.label_tel.place(x = 50, y = 80)
        self.label_email = tk.Label(self, text = 'E-Mail')
        self.label_email.place(x = 50, y = 110)
        # Input Windows
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x = 200, y = 50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x = 200, y = 80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x = 200, y = 110)
        self.btn_ok = tk.Button(self, text = 'Создать', cursor = 'hand2', command = self.record)
        self.btn_ok.place(x = 100, y = 150)
        self.btn_exit = tk.Button(self, text = 'Закрыть', cursor = 'hand2')
        self.btn_exit.bind('<Button-1>', lambda ev: self.destroy())
        self.btn_exit.place(x = 200, y = 150)
    # Recording method
    def record(self):
        self.view.db.insert_data(self.entry_name.get(), self.entry_phone.get(), self.entry_email.get())
        self.view.view_record()
        self.destroy()
# Creating a search box
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.view_search()
    # Method of displaying the search box
    def view_search(self):
        self.title('Добавление сотрудника')
        self.resizable(False, False)
        self.geometry('400x100')
        self.grab_set()
        self.focus()
        label_search = tk.Label(self, text = 'Введите ваш запрос: ')
        label_search.place(x = 50, y = 20)
        self.entry_search = tk.Entry(self)
        self.entry_search.place(x = 200, y = 20)
        search_btn = tk.Button(self, text = 'Поиск', cursor = 'hand2', command = self.search)
        search_btn.place(x = 100, y = 60)
        close_btn = tk.Button(self, text = 'Закрыть', cursor = 'hand2')
        close_btn.bind('<Button-1>', lambda ev: self.destroy())
        close_btn.place(x = 250, y = 60)
    # Search method
    def search(self):
        self.view.search(self.entry_search.get())
        self.destroy()
# Creating an Edit window
class Edit(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.view_edit()
        self.paste_first()
    
    # Method of displaying the edit window
    def view_edit(self):
        self.title = 'Редактировать запись о сотруднике'
        
        self.resizable(False, False)
        self.geometry('400x200')
        self.grab_set()
        self.focus()
        self.label_name = tk.Label(self, text = 'ФИО')
        self.label_name.place(x = 50, y = 50)
        self.label_tel = tk.Label(self, text = 'Телефон')
        self.label_tel.place(x = 50, y = 80)
        self.label_email = tk.Label(self, text = 'E-Mail')
        self.label_email.place(x = 50, y = 110)
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x = 200, y = 50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x = 200, y = 80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x = 200, y = 110)
        self.btn_ok = tk.Button(self, text = 'Изменить', cursor = 'hand2', command = self.edit)
        self.btn_ok.place(x = 100, y = 150)
        self.btn_exit = tk.Button(self, text = 'Закрыть', cursor = 'hand2')
        self.btn_exit.bind('<Button-1>', lambda ev: self.destroy())
        self.btn_exit.place(x = 200, y = 150)
    # Method for adding the initial values of the input window
    def paste_first(self):
        self.view.db.cur.execute(
            '''
                SELECT * FROM personal WHERE id = ?
            ''', self.view.tree.set(self.view.tree.selection()[0], '#1')
        )
        data = self.view.db.cur.fetchone()
        
        self.entry_name.insert(0, data[1])
        self.entry_phone.insert(0, data[2])
        self.entry_email.insert(0, data[3])
    # Method of changing records
    def edit(self):
        self.view.edit(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get()
        )
        self.destroy()
# Creating a class for a database
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('personal.db')
        self.cur = self.conn.cursor()
        # Creating database tables
        self.cur.execute(
            '''
                CREATE TABLE IF NOT EXISTS personal(
                    id INTEGER NOT NULL PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT
                )
            '''
        )
    # Adding data to the database
    def insert_data(self, name, phone, email):
        self.cur.execute(
            '''
                INSERT INTO personal(name, phone, email)
                VALUES(?, ?, ?)
            ''', (name, phone, email)
        )
        self.conn.commit()
    # Deleting records from the database
    def delete_data(self, id):
        self.cur.execute(
            '''
                DELETE FROM personal WHERE id = ?
            ''', (id)
        )
        
# Launching the program
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.geometry('750x400')
    root.title('Список сотрудников компании')
    root.resizable(False, False)
    root.mainloop()