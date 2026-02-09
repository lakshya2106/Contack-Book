from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
from tkinter import filedialog
import csv
import sys


if sys.platform == 'win32':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass


LIGHT_THEME = {
    'bg_primary': '#f5f5f5',
    'bg_secondary': '#ffffff',
    'bg_header': '#2c3e50',

    'bg_button_primary': '#3498db',
    'bg_button_primary_hover': '#2980b9',

    'bg_button_success': '#27ae60',
    'bg_button_success_hover': '#229954',

    'bg_button_danger': '#e74c3c',
    'bg_button_danger_hover': '#c0392b',

    'bg_button_warning': '#f39c12',
    'bg_button_warning_hover': '#d68910',

    'text_primary': '#2c3e50',
    'text_secondary': '#7f8c8d',
    'text_light': '#ffffff',
    'accent': '#3498db'
}

DARK_THEME = {
    'bg_primary': '#121212',
    'bg_secondary': '#1e1e1e',
    'bg_header': '#1f2a36',

    'bg_button_primary': '#2980b9',
    'bg_button_primary_hover': '#2471a3',

    'bg_button_success': '#2ecc71',
    'bg_button_success_hover': '#27ae60',

    'bg_button_danger': '#e74c3c',
    'bg_button_danger_hover': '#c0392b',

    'bg_button_warning': '#f1c40f',
    'bg_button_warning_hover': '#d4ac0d',

    'text_primary': '#ecf0f1',
    'text_secondary': '#aaaaaa',
    'text_light': '#ffffff',
    'accent': '#3498db'
}


COLORS = LIGHT_THEME
current_theme = "light"



root = Tk()
root.title("Contact Management System")

if sys.platform == 'win32':
    try:
        root.tk.call('tk', 'scaling', 1.25)
    except:
        pass

width = 1200
height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(1, 1)
root.config(bg=COLORS['bg_primary'])
root.minsize(900, 500)

#============================VARIABLES===================================
# All the variable which are used.

FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()
SEARCH = StringVar()

#============================METHODS=====================================
# All the methods which are used in the program for its functianality.


def only_numbers(char):
    return char.isdigit()

vcmd_numbers = (root.register(only_numbers), '%S')


def Database():
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    RefreshCount()
    cursor.close()
    conn.close()

def SubmitData():
    if  FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('Validation Error', 'Please complete all required fields.', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get()), str(CONTACT.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")
        if 'NewWindow' in globals():
            NewWindow.destroy()
        tkMessageBox.showinfo("Success", "Contact added successfully!")
        RefreshCount()

def UpdateData():
    if not tkMessageBox.askyesno("Confirm Update", "Save changes to this contact?"):
        return

    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
       result = tkMessageBox.showwarning('Validation Error', 'Please complete all required fields.', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` =?, `age` = ?,  `address` = ?, `contact` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(AGE.get()), str(ADDRESS.get()), str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")
        if 'UpdateWindow' in globals():
            UpdateWindow.destroy()
        tkMessageBox.showinfo("Success", "Contact updated successfully!")
        RefreshCount()
    
def OnSelected(event):
    if not tree.selection():
        return

    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Update Contact")
    width = 550
    height = 580
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    UpdateWindow.config(bg=COLORS['bg_primary'])
    if 'NewWindow' in globals():
        NewWindow.destroy()

    #===================FRAMES==============================
    FormTitle = Frame(UpdateWindow, bg=COLORS['bg_header'], height=70)
    FormTitle.pack(side=TOP, fill=X)
    ContactForm = Frame(UpdateWindow, bg=COLORS['bg_secondary'], padx=35, pady=25)
    ContactForm.pack(side=TOP, fill=BOTH, expand=True, padx=25, pady=25)
    RadioGroup = Frame(ContactForm, bg=COLORS['bg_secondary'])
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", 
                      font=('Segoe UI', 13), bg=COLORS['bg_secondary'], 
                      fg=COLORS['text_primary'], selectcolor=COLORS['bg_secondary'],
                      activebackground=COLORS['bg_secondary'], activeforeground=COLORS['text_primary'])
    Male.pack(side=LEFT, padx=15)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", 
                        font=('Segoe UI', 13), bg=COLORS['bg_secondary'],
                        fg=COLORS['text_primary'], selectcolor=COLORS['bg_secondary'],
                        activebackground=COLORS['bg_secondary'], activeforeground=COLORS['text_primary'])
    Female.pack(side=LEFT, padx=15)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Update Contact", font=('Segoe UI', 22, 'bold'), 
                     bg=COLORS['bg_header'], fg=COLORS['text_light'], pady=18)
    lbl_title.pack()
    lbl_firstname = Label(ContactForm, text="First Name:", font=('Segoe UI', 13), 
                         bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_firstname.grid(row=0, column=0, sticky=W, pady=10, padx=8)
    lbl_lastname = Label(ContactForm, text="Last Name:", font=('Segoe UI', 13), 
                        bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_lastname.grid(row=1, column=0, sticky=W, pady=10, padx=8)
    lbl_gender = Label(ContactForm, text="Gender:", font=('Segoe UI', 13), 
                      bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_gender.grid(row=2, column=0, sticky=W, pady=10, padx=8)
    lbl_age = Label(ContactForm, text="Age:", font=('Segoe UI', 13), 
                   bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_age.grid(row=3, column=0, sticky=W, pady=10, padx=8)
    lbl_address = Label(ContactForm, text="Address:", font=('Segoe UI', 13), 
                       bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_address.grid(row=4, column=0, sticky=W, pady=10, padx=8)
    lbl_contact = Label(ContactForm, text="Contact:", font=('Segoe UI', 13), 
                       bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_contact.grid(row=5, column=0, sticky=W, pady=10, padx=8)

    #===================ENTRY===============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('Segoe UI', 13), 
                     relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
                     fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    firstname.grid(row=0, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('Segoe UI', 13), 
                    relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
                    fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    lastname.grid(row=1, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    RadioGroup.grid(row=2, column=1, sticky=W, pady=10, padx=8)
    age = Entry(ContactForm, textvariable=AGE, font=('Segoe UI', 13), 
               relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
               fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    age.grid(row=3, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    address = Entry(ContactForm, textvariable=ADDRESS, font=('Segoe UI', 13), 
                   relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
                   fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    address.grid(row=4, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('Segoe UI', 13), 
                   relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
                   fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    contact.grid(row=5, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    
    ContactForm.columnconfigure(1, weight=1)

    #==================BUTTONS==============================
    btn_frame = Frame(ContactForm, bg=COLORS['bg_secondary'])
    btn_frame.grid(row=6, column=0, columnspan=2, pady=25)
    btn_updatecon = Button(btn_frame, text="Update Contact", width=22, height=2, 
                          command=UpdateData, font=('Segoe UI', 13, 'bold'),
                          bg=COLORS['bg_button_primary'], fg=COLORS['text_light'],
                          relief=FLAT, cursor='hand2',
                          activebackground=COLORS['bg_button_primary_hover'],
                          activeforeground=COLORS['text_light'])
    btn_updatecon.pack()

def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('No Selection', 'Please select a contact to delete.', icon="warning")
    else:
        result = tkMessageBox.askquestion('Confirm Delete', 'Are you sure you want to delete this contact?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
            tkMessageBox.showinfo("Success", "Contact deleted successfully!")
            RefreshCount()
    
def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Add New Contact")
    width = 550
    height = 580
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    NewWindow.config(bg=COLORS['bg_primary'])
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow, bg=COLORS['bg_header'], height=70)
    FormTitle.pack(side=TOP, fill=X)
    ContactForm = Frame(NewWindow, bg=COLORS['bg_secondary'], padx=35, pady=25)
    ContactForm.pack(side=TOP, fill=BOTH, expand=True, padx=25, pady=25)
    RadioGroup = Frame(ContactForm, bg=COLORS['bg_secondary'])
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", 
                      font=('Segoe UI', 13), bg=COLORS['bg_secondary'], 
                      fg=COLORS['text_primary'], selectcolor=COLORS['bg_secondary'],
                      activebackground=COLORS['bg_secondary'], activeforeground=COLORS['text_primary'])
    Male.pack(side=LEFT, padx=15)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", 
                        font=('Segoe UI', 13), bg=COLORS['bg_secondary'],
                        fg=COLORS['text_primary'], selectcolor=COLORS['bg_secondary'],
                        activebackground=COLORS['bg_secondary'], activeforeground=COLORS['text_primary'])
    Female.pack(side=LEFT, padx=15)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Add New Contact", font=('Segoe UI', 22, 'bold'), 
                     bg=COLORS['bg_header'], fg=COLORS['text_light'], pady=18)
    lbl_title.pack()
    lbl_firstname = Label(ContactForm, text="First Name:", font=('Segoe UI', 13), 
                         bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_firstname.grid(row=0, column=0, sticky=W, pady=10, padx=8)
    lbl_lastname = Label(ContactForm, text="Last Name:", font=('Segoe UI', 13), 
                        bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_lastname.grid(row=1, column=0, sticky=W, pady=10, padx=8)
    lbl_gender = Label(ContactForm, text="Gender:", font=('Segoe UI', 13), 
                      bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_gender.grid(row=2, column=0, sticky=W, pady=10, padx=8)
    lbl_age = Label(ContactForm, text="Age:", font=('Segoe UI', 13), 
                   bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_age.grid(row=3, column=0, sticky=W, pady=10, padx=8)
    lbl_address = Label(ContactForm, text="Address:", font=('Segoe UI', 13), 
                       bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_address.grid(row=4, column=0, sticky=W, pady=10, padx=8)
    lbl_contact = Label(ContactForm, text="Contact:", font=('Segoe UI', 13), 
                       bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], anchor='w')
    lbl_contact.grid(row=5, column=0, sticky=W, pady=10, padx=8)

    #===================ENTRY===============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('Segoe UI', 13), 
                     relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
                     fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    firstname.grid(row=0, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('Segoe UI', 13), 
                    relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
                    fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    lastname.grid(row=1, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    RadioGroup.grid(row=2, column=1, sticky=W, pady=10, padx=8)
    age = Entry(
    ContactForm,
    textvariable=AGE,
    font=('Segoe UI', 13),
    validate='key',
    validatecommand=vcmd_numbers,
    relief=SOLID,
    borderwidth=1,
    bg=COLORS['bg_primary'],
    fg=COLORS['text_primary'],
    insertbackground=COLORS['text_primary']
)

    age.grid(row=3, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    address = Entry(ContactForm, textvariable=ADDRESS, font=('Segoe UI', 13), 
                   relief=SOLID, borderwidth=1, bg=COLORS['bg_primary'], 
                   fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'])
    address.grid(row=4, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    contact = Entry(
    ContactForm,
    textvariable=CONTACT,
    font=('Segoe UI', 13),
    validate='key',
    validatecommand=vcmd_numbers,
    relief=SOLID,
    borderwidth=1,
    bg=COLORS['bg_primary'],
    fg=COLORS['text_primary'],
    insertbackground=COLORS['text_primary']
)

    contact.grid(row=5, column=1, sticky=EW, pady=10, padx=8, ipady=7)
    
    ContactForm.columnconfigure(1, weight=1)

    #==================BUTTONS==============================
    btn_frame = Frame(ContactForm, bg=COLORS['bg_secondary'])
    btn_frame.grid(row=6, column=0, columnspan=2, pady=25)
    btn_addcon = Button(btn_frame, text="Save Contact", width=22, height=2, 
                       command=SubmitData, font=('Segoe UI', 13, 'bold'),
                       bg=COLORS['bg_button_success'], fg=COLORS['text_light'],
                       relief=FLAT, cursor='hand2',
                       activebackground=COLORS['bg_button_success_hover'],
                       activeforeground=COLORS['text_light'])
    btn_addcon.pack()

def on_enter(btn, color):
    btn['background'] = color

def on_leave(btn, color):
    btn['background'] = color

def RefreshCount():
    try:
        count = len(tree.get_children())
    except Exception:
        count = 0
    if 'status_label' in globals():
        status_label.config(text=f"Total contacts: {count}")

def SearchData(event=None):
    query = SEARCH.get().strip()
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    if query == "":
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
    else:
        like = f"%{query}%"
        cursor.execute("SELECT * FROM `member` WHERE firstname LIKE ? OR lastname LIKE ? OR contact LIKE ? ORDER BY `lastname` ASC", (like, like, like))
        fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()
    RefreshCount()

def ClearSearch():
    SEARCH.set("")
    SearchData()

def ExportCSV():
    try:
        file = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if not file:
            return
        with open(file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["mem_id", "firstname", "lastname", "gender", "age", "address", "contact"])
            for item in tree.get_children():
                vals = tree.item(item)['values']
                # values may be a tuple containing a tuple
                if vals and isinstance(vals[0], (list, tuple)):
                    vals = vals[0]
                writer.writerow(vals)
        tkMessageBox.showinfo('Export Successful', f'Contacts exported to {file}')
    except Exception as e:
        tkMessageBox.showerror('Error', f'Failed to export CSV: {e}')

def ImportCSV():
    try:
        file = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if not file:
            return
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            for row in reader:
                if not row:
                    continue
                # Accept rows with or without mem_id
                if len(row) >= 6:
                    # If first column is id and there are 7 columns
                    if len(row) >= 7:
                        firstname = row[1]
                        lastname = row[2]
                        gender = row[3]
                        age = row[4]
                        address = row[5]
                        contact = row[6]
                    else:
                        firstname, lastname, gender, age, address, contact = row[:6]
                    cursor.execute("INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", (firstname, lastname, gender, age, address, contact))
            conn.commit()
            cursor.close()
            conn.close()
        SearchData()
        tkMessageBox.showinfo('Import Successful', f'Contacts imported from {file}')
    except Exception as e:
        tkMessageBox.showerror('Error', f'Failed to import CSV: {e}')

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    try:
        # try numeric sort
        l.sort(key=lambda t: int(t[0]) if str(t[0]).isdigit() else str(t[0]).lower(), reverse=reverse)
    except Exception:
        l.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def edit_selected():
    if not tree.selection():
        return
    # simulate double click edit
    OnSelected(None)

def apply_theme():
    root.config(bg=COLORS['bg_primary'])
    Top.config(bg=COLORS['bg_header'])
    Mid.config(bg=COLORS['bg_primary'])
    ButtonFrame.config(bg=COLORS['bg_primary'])
    SearchFrame.config(bg=COLORS['bg_primary'])
    TreeFrame.config(bg=COLORS['bg_secondary'])

    lbl_title.config(bg=COLORS['bg_header'], fg=COLORS['text_light'])
    lbl_search.config(bg=COLORS['bg_primary'], fg=COLORS['text_primary'])
    status_label.config(bg=COLORS['bg_primary'], fg=COLORS['text_secondary'])

    # Treeview styling
    style = ttk.Style()
    style.configure(
        "Treeview",
        background=COLORS['bg_secondary'],
        foreground=COLORS['text_primary'],
        fieldbackground=COLORS['bg_secondary'],
        rowheight=42,
        font=('Segoe UI', 12)
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS['bg_header'],
        foreground=COLORS['text_light'],
        font=('Segoe UI', 13, 'bold')
    )
    style.map(
        "Treeview",
        background=[('selected', COLORS['accent'])],
        foreground=[('selected', COLORS['text_light'])]
    )

def toggle_theme():
    global COLORS, current_theme

    if current_theme == "light":
        COLORS = DARK_THEME
        current_theme = "dark"
        theme_btn.config(text="☀ Light Mode")
    else:
        COLORS = LIGHT_THEME
        current_theme = "light"
        theme_btn.config(text="🌙 Dark Mode")

    apply_theme()




#============================FRAMES======================================
# for ui design 



Top = Frame(root, bg=COLORS['bg_header'], height=80)
Top.pack(side=TOP, fill=X)
Mid = Frame(root, bg=COLORS['bg_primary'], padx=20, pady=15)
Mid.pack(side=TOP, fill=X)
ButtonFrame = Frame(Mid, bg=COLORS['bg_primary'])
ButtonFrame.pack(side=TOP, fill=X, pady=10)
SearchFrame = Frame(Mid, bg=COLORS['bg_primary'])
SearchFrame.pack(side=TOP, fill=X)
lbl_search = Label(SearchFrame, text="Search:", font=('Segoe UI', 12), bg=COLORS['bg_primary'], fg=COLORS['text_primary'])
lbl_search.pack(side=LEFT, padx=(4,6))
entry_search = Entry(SearchFrame, textvariable=SEARCH, font=('Segoe UI', 12), width=34, relief=SOLID, borderwidth=1)
entry_search.pack(side=LEFT, padx=(0,6), ipady=4)
entry_search.bind('<KeyRelease>', SearchData)
btn_search_clear = Button(SearchFrame, text="Clear", command=ClearSearch, font=('Segoe UI', 11), bg=COLORS['bg_button_warning'], fg=COLORS['text_light'], relief=FLAT, cursor='hand2')
btn_search_clear.pack(side=LEFT, padx=6)
TableMargin = Frame(root, bg=COLORS['bg_primary'], padx=20, pady=10)
TableMargin.pack(side=TOP, fill=BOTH, expand=True)

# this is the button to toggle between light and dark themes. It is placed in the top frame on the right side.
theme_btn = Button(
    Top,
    text="🌙 Dark Mode",
    command=toggle_theme,
    font=('Segoe UI', 11, 'bold'),
    bg=COLORS['bg_button_primary'],
    fg=COLORS['text_light'],
    relief=FLAT,
    cursor='hand2'
)
theme_btn.pack(side=RIGHT, padx=20)


#============================LABELS======================================
lbl_title = Label(Top, text="Contact Management System", font=('Segoe UI', 28, 'bold'), 
                 bg=COLORS['bg_header'], fg=COLORS['text_light'], pady=25)
lbl_title.pack()

#============================BUTTONS=====================================
btn_add = Button(ButtonFrame, text="+ Add New Contact", width=20, height=2, 
                command=AddNewWindow, font=('Segoe UI', 13, 'bold'),
                bg=COLORS['bg_button_success'], fg=COLORS['text_light'],
                relief=FLAT, cursor='hand2',
                activebackground=COLORS['bg_button_success_hover'],
                activeforeground=COLORS['text_light'])
btn_add.pack(side=LEFT, padx=8)

btn_delete = Button(ButtonFrame, text="Delete Selected", width=20, height=2, 
                   command=DeleteData, font=('Segoe UI', 13, 'bold'),
                   bg=COLORS['bg_button_danger'], fg=COLORS['text_light'],
                   relief=FLAT, cursor='hand2',
                   activebackground=COLORS['bg_button_danger_hover'],
                   activeforeground=COLORS['text_light'])
btn_delete.pack(side=LEFT, padx=8)

btn_export = Button(ButtonFrame, text="Export CSV", width=14, height=2,
                    command=ExportCSV, font=('Segoe UI', 11, 'bold'),
                    bg=COLORS['bg_button_primary'], fg=COLORS['text_light'],
                    relief=FLAT, cursor='hand2')
btn_export.pack(side=LEFT, padx=6)

btn_import = Button(ButtonFrame, text="Import CSV", width=14, height=2,
                    command=ImportCSV, font=('Segoe UI', 11, 'bold'),
                    bg=COLORS['bg_button_primary'], fg=COLORS['text_light'],
                    relief=FLAT, cursor='hand2')
btn_import.pack(side=LEFT, padx=6)

btn_add.bind("<Enter>", lambda e: on_enter(btn_add, COLORS['bg_button_success_hover']))
btn_add.bind("<Leave>", lambda e: on_leave(btn_add, COLORS['bg_button_success']))

#============================TABLES======================================
# container for table

TreeFrame = Frame(
    TableMargin,
    bg=COLORS['bg_secondary'],
    bd=1,
    relief=SOLID
)
TreeFrame.pack(fill=BOTH, expand=True)

# Inner padding so table doesn't touch border
TreeInner = Frame(
    TreeFrame,
    bg=COLORS['bg_secondary'],
    padx=8,
    pady=8
)
TreeInner.pack(fill=BOTH, expand=True)

# Scrollbars
scrollbary = Scrollbar(TreeInner, orient=VERTICAL)
scrollbarx = Scrollbar(TreeInner, orient=HORIZONTAL)

# Treeview
tree = ttk.Treeview(
    TreeInner,
    columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"),
    show='headings',
    selectmode="browse",
    yscrollcommand=scrollbary.set,
    xscrollcommand=scrollbarx.set
)

scrollbary.config(command=tree.yview)
scrollbarx.config(command=tree.xview)

scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.pack(fill=BOTH, expand=True)

#============================HEADINGS====================================

tree.heading("MemberID", text="ID", anchor=CENTER,
             command=lambda: treeview_sort_column(tree, "MemberID", False))
tree.heading("Firstname", text="First Name", anchor=W,
             command=lambda: treeview_sort_column(tree, "Firstname", False))
tree.heading("Lastname", text="Last Name", anchor=W,
             command=lambda: treeview_sort_column(tree, "Lastname", False))
tree.heading("Gender", text="Gender", anchor=CENTER,
             command=lambda: treeview_sort_column(tree, "Gender", False))
tree.heading("Age", text="Age", anchor=CENTER,
             command=lambda: treeview_sort_column(tree, "Age", False))
tree.heading("Address", text="Address", anchor=W,
             command=lambda: treeview_sort_column(tree, "Address", False))
tree.heading("Contact", text="Contact", anchor=W,
             command=lambda: treeview_sort_column(tree, "Contact", False))

#============================COLUMNS=====================================

tree.column("MemberID", width=70, anchor=CENTER, stretch=NO)
tree.column("Firstname", width=160, anchor=W)
tree.column("Lastname", width=160, anchor=W)
tree.column("Gender", width=100, anchor=CENTER)
tree.column("Age", width=80, anchor=CENTER)
tree.column("Address", width=220, anchor=W)
tree.column("Contact", width=180, anchor=W)

#============================STYLE=======================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=COLORS['bg_secondary'],
    foreground=COLORS['text_primary'],
    fieldbackground=COLORS['bg_secondary'],
    font=('Segoe UI', 12),
    rowheight=42,
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background=COLORS['bg_header'],
    foreground=COLORS['text_light'],
    font=('Segoe UI', 13, 'bold'),
    relief=FLAT
)

style.map(
    "Treeview",
    background=[('selected', COLORS['bg_button_primary'])],
    foreground=[('selected', COLORS['text_light'])]
)

# Bind double-click edit
tree.bind('<Double-Button-1>', OnSelected)

def show_context_menu(event):
    row_id = tree.identify_row(event.y)
    if row_id:
        tree.selection_set(row_id)
        tree.focus(row_id)
        menu.tk_popup(event.x_root, event.y_root)

# Windows & Linux
tree.bind("<Button-3>", show_context_menu)

# macOS support (optional)
tree.bind("<Control-Button-1>", show_context_menu)


# ============================ RIGHT CLICK MENU ============================

menu = Menu(root, tearoff=0)
menu.add_command(label="✏️ Edit Contact", command=lambda: edit_selected())
menu.add_separator()
menu.add_command(label="🗑 Delete Contact", command=lambda: DeleteData())

#============================STATUS BAR==================================

status_label = Label(
    root,
    text="Total contacts: 0",
    bg=COLORS['bg_primary'],
    fg=COLORS['text_secondary'],
    font=('Segoe UI', 11)
)
status_label.pack(side=TOP, anchor='e', padx=26, pady=(6, 12))


#============================INITIALIZATION==============================
if __name__ == '__main__':
    Database()
    apply_theme()
    root.mainloop()

    
