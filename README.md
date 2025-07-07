# Toll_Management
A full-stack CLI-based Toll Management System built with **Python** and **MySQL**, featuring:
- Admin & Customer Portals
- OTP-based Secure Login (Fallback Supported)
- Auto-triggered Violation Logging via SQL Triggers
- Real-time Toll Transactions & Vehicle Logs
- Staff Salary & Audit Tracking
- Interactive Graphs (Matplotlib)
- Clean Terminal UI using `tabulate`

---

## 🔧 Tech Stack
- **Backend:** Python 3
- **Database:** MySQL with Triggers & Foreign Keys
- **Visualization:** Matplotlib
- **Email Handling:** smtplib, EmailMessage (fallback OTP)
- **CLI Tables:** Tabulate

---

## 📂 Features

### 👨‍💼 Admin
- Secure Login with OTP
- Add/View Admins by Role
- Manage Booths, Staff, and Routes
- View Customer & Vehicle Data
- Track Transactions & Violations
- Staff Audit Logs
- Graphs: Vehicle Distribution, Booth Traffic

### 🚗 Customer
- Register New Account
- Secure Login (Password Protected)
- View Vehicle Info & Recharge Balance
- Toll Entry with Auto Transaction Logging
- Transaction History

---

## 📊 Graphs
- Vehicle Type Distribution (Pie Chart)
- Booth-wise Transaction Volume (Bar Chart)

---

## 🔐 Smart Trigger
Automatically logs a **violation** if a user’s balance is **insufficient** at toll entry — added using a MySQL **trigger**.
