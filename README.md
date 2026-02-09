# 📇 Contact Management System  
### Desktop Application using Python, Tkinter & SQLite

A **modern, desktop-based Contact Management System** developed using **Python (Tkinter GUI)** and **SQLite database**.  
This application provides an intuitive and professional interface to **manage contacts efficiently** with support for **CRUD operations, search, CSV import/export, dark & light themes, and context menus**.

---

## 🚀 Project Overview

The Contact Management System is designed to store, manage, and organize contact information in a structured and user-friendly way.  
It is suitable for **personal use, small organizations, and academic purposes**.

The project focuses on:
- Clean UI design
- Smooth user experience
- Data persistence using SQLite
- Practical desktop application development using Python

---

## ✨ Key Features

- ➕ **Add New Contacts**
- ✏️ **Edit / Update Existing Contacts**
- 🗑 **Delete Contacts with Confirmation**
- 🔍 **Real-Time Search Functionality**
- 📊 **Sortable Table Columns**
- 🖱 **Right-Click Context Menu (Edit / Delete)**
- 📤 **Export Contacts to CSV**
- 📥 **Import Contacts from CSV**
- 🌗 **Light & Dark Theme Toggle**
- 📈 **Live Total Contact Counter**
- 💾 **SQLite Database Integration**
- 🖥 **High-DPI Awareness (Windows Support)**
- 🎨 **Modern & Professional UI Design**

---

## 🛠 Technologies Used

| Category | Technology |
|--------|------------|
| Language | Python 3 |
| GUI Framework | Tkinter & ttk |
| Database | SQLite3 |
| File Handling | CSV |
| Platform | Windows / Cross-platform |

---

## 📂 Project Structure

Contact-Management-System/
│
├── index.py          # Main application file
├── pythontut.db      # SQLite database (auto-generated)
├── README.md         # Project documentation
└── assets/           # Screenshots & resources



---

## 🗃 Database Design

### Table: `member`

| Field Name | Data Type | Description |
|----------|----------|-------------|
| mem_id | INTEGER | Primary Key (Auto Increment) |
| firstname | TEXT | First Name |
| lastname | TEXT | Last Name |
| gender | TEXT | Gender |
| age | TEXT | Age |
| address | TEXT | Address |
| contact | TEXT | Contact Number |

---

## ⚙️ How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Contact-Management-System.git
cd Contact-Management-System
