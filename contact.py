import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# DATABASE
# ============================================================

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

conn.commit()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Contact Book")
root.geometry("850x600")
root.minsize(750, 500)


# ============================================================
# VARIABLES
# ============================================================

name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()

selected_id = None


# ============================================================
# FUNCTIONS
# ============================================================

def clear_fields():
    global selected_id

    selected_id = None

    name_var.set("")
    phone_var.set("")
    email_var.set("")

    name_entry.focus()


def load_contacts(search=""):
    # Clear table
    for item in contact_table.get_children():
        contact_table.delete(item)

    if search:
        cursor.execute("""
            SELECT id, name, phone, email
            FROM contacts
            WHERE name LIKE ?
               OR phone LIKE ?
               OR email LIKE ?
            ORDER BY name
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("""
            SELECT id, name, phone, email
            FROM contacts
            ORDER BY name
        """)

    contacts = cursor.fetchall()

    for contact in contacts:
        contact_table.insert(
            "",
            tk.END,
            values=contact
        )


def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if not name:
        messagebox.showwarning(
            "Missing Information",
            "Please enter a name."
        )
        return

    cursor.execute("""
        INSERT INTO contacts (name, phone, email)
        VALUES (?, ?, ?)
    """, (name, phone, email))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Contact added successfully!"
    )

    clear_fields()
    load_contacts()


def select_contact(event):
    global selected_id

    selected = contact_table.selection()

    if not selected:
        return

    values = contact_table.item(
        selected[0],
        "values"
    )

    selected_id = values[0]

    name_var.set(values[1])
    phone_var.set(values[2])
    email_var.set(values[3])


def update_contact():
    global selected_id

    if selected_id is None:
        messagebox.showwarning(
            "No Selection",
            "Please select a contact first."
        )
        return

    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if not name:
        messagebox.showwarning(
            "Missing Information",
            "Name cannot be empty."
        )
        return

    cursor.execute("""
        UPDATE contacts
        SET name = ?, phone = ?, email = ?
        WHERE id = ?
    """, (
        name,
        phone,
        email,
        selected_id
    ))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Contact updated successfully!"
    )

    clear_fields()
    load_contacts()


def delete_contact():
    global selected_id

    if selected_id is None:
        messagebox.showwarning(
            "No Selection",
            "Please select a contact first."
        )
        return

    confirm = messagebox.askyesno(
        "Delete Contact",
        "Are you sure you want to delete this contact?"
    )

    if not confirm:
        return

    cursor.execute("""
        DELETE FROM contacts
        WHERE id = ?
    """, (selected_id,))

    conn.commit()

    messagebox.showinfo(
        "Deleted",
        "Contact deleted successfully!"
    )

    clear_fields()
    load_contacts()


def search_contacts(*args):
    search_text = search_var.get().strip()

    load_contacts(search_text)


def clear_search():
    search_var.set("")
    load_contacts()


def close_app():
    conn.close()
    root.destroy()


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Title.TLabel",
    font=("Arial", 24, "bold")
)

style.configure(
    "Subtitle.TLabel",
    font=("Arial", 10)
)

style.configure(
    "Treeview",
    rowheight=30,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)

style.configure(
    "Action.TButton",
    font=("Arial", 10, "bold"),
    padding=8
)


# ============================================================
# HEADER
# ============================================================

header = ttk.Frame(root, padding=20)
header.pack(fill="x")

title = ttk.Label(
    header,
    text="Contact Book",
    style="Title.TLabel"
)

title.pack(anchor="w")

subtitle = ttk.Label(
    header,
    text="Manage your contacts easily",
    style="Subtitle.TLabel"
)

subtitle.pack(anchor="w")


# ============================================================
# INPUT FRAME
# ============================================================

input_frame = ttk.LabelFrame(
    root,
    text="Contact Information",
    padding=15
)

input_frame.pack(
    fill="x",
    padx=20,
    pady=5
)


# Name

ttk.Label(
    input_frame,
    text="Name"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

name_entry = ttk.Entry(
    input_frame,
    textvariable=name_var,
    width=30
)

name_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# Phone

ttk.Label(
    input_frame,
    text="Phone"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5,
    sticky="w"
)

phone_entry = ttk.Entry(
    input_frame,
    textvariable=phone_var,
    width=25
)

phone_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


# Email

ttk.Label(
    input_frame,
    text="Email"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

email_entry = ttk.Entry(
    input_frame,
    textvariable=email_var,
    width=30
)

email_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# BUTTONS
# ============================================================

button_frame = ttk.Frame(
    root,
    padding=(20, 10)
)

button_frame.pack(fill="x")


ttk.Button(
    button_frame,
    text="Add Contact",
    style="Action.TButton",
    command=add_contact
).pack(
    side="left",
    padx=5
)

ttk.Button(
    button_frame,
    text="Update",
    style="Action.TButton",
    command=update_contact
).pack(
    side="left",
    padx=5
)

ttk.Button(
    button_frame,
    text="Delete",
    style="Action.TButton",
    command=delete_contact
).pack(
    side="left",
    padx=5
)

ttk.Button(
    button_frame,
    text="Clear",
    style="Action.TButton",
    command=clear_fields
).pack(
    side="left",
    padx=5
)


# ============================================================
# SEARCH
# ============================================================

search_frame = ttk.Frame(
    root,
    padding=(20, 5)
)

search_frame.pack(fill="x")


ttk.Label(
    search_frame,
    text="Search:"
).pack(side="left")


search_entry = ttk.Entry(
    search_frame,
    textvariable=search_var,
    width=35
)

search_entry.pack(
    side="left",
    padx=10
)

search_var.trace_add(
    "write",
    search_contacts
)

ttk.Button(
    search_frame,
    text="Clear Search",
    command=clear_search
).pack(side="left")


# ============================================================
# CONTACT TABLE
# ============================================================

table_frame = ttk.Frame(
    root,
    padding=(20, 10)
)

table_frame.pack(
    fill="both",
    expand=True
)


columns = (
    "ID",
    "Name",
    "Phone",
    "Email"
)

contact_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


contact_table.heading(
    "ID",
    text="ID"
)

contact_table.heading(
    "Name",
    text="Name"
)

contact_table.heading(
    "Phone",
    text="Phone"
)

contact_table.heading(
    "Email",
    text="Email"
)


contact_table.column(
    "ID",
    width=50,
    anchor="center"
)

contact_table.column(
    "Name",
    width=200
)

contact_table.column(
    "Phone",
    width=150
)

contact_table.column(
    "Email",
    width=300
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=contact_table.yview
)

contact_table.configure(
    yscrollcommand=scrollbar.set
)


contact_table.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# Select contact

contact_table.bind(
    "<<TreeviewSelect>>",
    select_contact
)


# ============================================================
# DOUBLE CLICK
# ============================================================

def double_click_contact(event):
    selected = contact_table.selection()

    if selected:
        select_contact(event)


contact_table.bind(
    "<Double-1>",
    double_click_contact
)


# ============================================================
# LOAD DATA
# ============================================================

load_contacts()

name_entry.focus()


# ============================================================
# CLOSE EVENT
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()