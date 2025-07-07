# Toll Management System - Ultimate Portal
import mysql.connector as m
from datetime import datetime
from tabulate import tabulate
import getpass, random, os, smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt
import tempfile

s = m.connect(user='root', passwd='2007', host='localhost', database='toll_management', auth_plugin='mysql_native_password')
c = s.cursor()

otp_sessions = {}

# -------------------------- UTILS --------------------------
def clear(): os.system('cls' if os.name == 'nt' else 'clear')
def banner(txt): print(f"\n{'='*10} {txt} {'='*10}")

def send_otp(email, aid):
    otp = random.randint(100000, 999999)
    otp_sessions[aid] = str(otp)
    msg = EmailMessage()
    msg.set_content(f"Your OTP for Toll Management login is: {otp}")
    msg["Subject"] = "Toll Portal Login OTP"
    msg["From"] = "admin@tollsystem.com"
    msg["To"] = email
    try:
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
        print(f"OTP sent to {email}")
    except:
        print("⚠️ Email service not configured — using fallback OTP")
        print(f"Your OTP: {otp}")

def otp_verify(aid):
    entry = input("Enter OTP sent to your email: ")
    return entry == otp_sessions.get(aid, '')

# ------------------------- Charts -------------------------
def graph_vehicle_types():
    c.execute("SELECT type, COUNT(*) FROM Vehicle GROUP BY type")
    result = c.fetchall()
    types = [r[0] for r in result]
    counts = [r[1] for r in result]
    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=types, autopct='%1.1f%%', startangle=140)
    plt.title('Vehicle Distribution by Type')
    plt.show()

def graph_transaction_booths():
    c.execute("SELECT booth_id, COUNT(*) FROM Toll_Transaction GROUP BY booth_id")
    rows = c.fetchall()
    booths = [str(x[0]) for x in rows]
    txn = [x[1] for x in rows]
    plt.bar(booths, txn, color='green')
    plt.xlabel('Booth ID')
    plt.ylabel('Transactions')
    plt.title('Booth-wise Transaction Volume')
    plt.show()

# ------------------------- Admin Portal -------------------------
def login_admin():
    clear()
    banner("Admin Login")
    aid = int(input("Admin ID: "))
    key = input("Admin Key: ")
    c.execute("SELECT * FROM Admin WHERE Id=%s AND admin_key=%s", (aid, key))
    user = c.fetchone()
    if not user:
        print("❌ Invalid credentials")
        return
    email = input("Enter email to receive OTP: ")
    send_otp(email, aid)
    if not otp_verify(aid):
        print("❌ OTP Verification Failed")
        return
    while True:
        clear()
        print(f"Admin: {user[1]} | Role: {user[3]} | Salary: ₹{user[4]}")
        print("""
        1. Staff By Booth   2. Customers
        3. Add Admin       4. Admins By Role
        5. Transactions    6. Violations
        7. Add Booth       8. All Tables
        9. Staff Salary    10. Emergencies
        11. Routes         12. Audit Logs
        13. Graphs         0. Logout
        """)
        ch = input("Option: ")
        if ch == '1':
            b = int(input("Booth ID: "))
            c.execute("SELECT * FROM Staff WHERE booth_id=%s", (b,))
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '2':
            c.execute("SELECT * FROM Customer")
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '3':
            name = input("Name: "); des = input("Role: "); sal = int(input("Salary: "))
            aid = random.randint(100000, 999999)
            key = random.randint(1000000000,9999999999)
            c.execute("INSERT INTO Admin VALUES (%s,%s,%s,%s,%s)", (aid,name,key,des,sal))
            s.commit(); print(f"✅ ID: {aid}, KEY: {key}")
        elif ch == '4':
            d = input("Designation: ")
            c.execute("SELECT Name, Salary_per_month FROM Admin WHERE Designation=%s", (d,))
            print(tabulate(c.fetchall(), headers=["Admin","Salary"]))
        elif ch == '5':
            c.execute("SELECT * FROM Toll_Transaction")
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '6':
            c.execute("SELECT * FROM Violation_Log")
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '7':
            b = int(input("Booth ID: ")); loc = input("Location: "); lanes = int(input("Lanes: "))
            c.execute("INSERT INTO Booth VALUES (%s,%s,%s,%s)", (b,loc,lanes,True))
            s.commit(); print("✅ Booth Added")
        elif ch == '8':
            for t in ["Admin","Booth","Customer","Staff","Vehicle","Staff_Audit","Toll_Transaction","Violation_Log"]:
                print(f"\n📦 {t}"); c.execute(f"SELECT * FROM {t}")
                print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '9':
            c.execute("SELECT role, SUM(salary) FROM Staff GROUP BY role")
            print(tabulate(c.fetchall(), headers=["Role","Total Salary"], tablefmt="grid"))
        elif ch == '10':
            c.execute("SELECT * FROM Emergency_Vehicle")
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '11':
            c.execute("SELECT * FROM Route")
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '12':
            c.execute("SELECT * FROM Staff_Audit")
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '13':
            graph_vehicle_types(); graph_transaction_booths()
        elif ch == '0': break
        else: print("❌ Invalid")
        input("\nPress Enter...")

# ------------------------- Customer + Register --------------
def login_customer():
    aid = int(input("Account ID: "))
    pwd = getpass.getpass("Password: ")
    c.execute("SELECT * FROM Customer WHERE account_id=%s AND password=%s", (aid, pwd))
    u = c.fetchone()
    if not u:
        print("❌ Invalid")
        return
    while True:
        clear(); print(f"👤 {u[1]} | Balance ₹{u[2]}")
        print("1. Recharge  2. Transactions  3. Toll Entry  4. Vehicle Info  0. Exit")
        ch = input("Option: ")
        if ch == '1':
            amt = float(input("Recharge ₹: "))
            c.execute("UPDATE Customer SET balance = balance + %s WHERE account_id=%s", (amt, aid)); s.commit()
        elif ch == '2':
            c.execute("SELECT * FROM Toll_Transaction WHERE account_id=%s", (aid,))
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '3':
            vid = u[3]; bid = int(input("Booth ID: "))
            c.execute("SELECT type FROM Vehicle WHERE vehicle_id=%s", (vid,))
            vtype = c.fetchone()[0]
            c.execute("SELECT offpeak_rate FROM Toll_Rate WHERE type=%s", (vtype,))
            toll = float(c.fetchone()[0])
            now = datetime.now()
            c.execute("""
                INSERT INTO Toll_Transaction(account_id, vehicle_id, booth_id, timestamp, toll_amount, payment_mode)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (aid, vid, bid, now, toll, 'FASTag'))
            s.commit(); print("✅ Toll Recorded")
        elif ch == '4':
            c.execute("SELECT * FROM Vehicle WHERE vehicle_id=%s", (u[3],))
            print(tabulate(c.fetchall(), headers=[i[0] for i in c.description]))
        elif ch == '0': break
        else: print("❌ Invalid")
        input("\nPress Enter...")

def register_customer():
    name = input("Full Name: ")
    email = input("Email: ")
    vid = int(input("Vehicle ID: "))
    bal = float(input("Initial Balance ₹: "))
    pwd = getpass.getpass("Set Password: ")
    aid = random.randint(700,999)
    c.execute("INSERT INTO Customer(account_id, name, balance, vehicle_id, password) VALUES (%s,%s,%s,%s,%s)",
              (aid,name,bal,vid,pwd)); s.commit()
    print(f"✅ Account ID: {aid}")
    input("Enter to return...")

# ------------------------- Entry Portal ---------------------
def portal():
    while True:
        clear(); banner("TOLL SYSTEM PORTAL")
        print("1. Admin Login  2. Customer Login  3. New Registration  0. Exit")
        ch = input("Choose option: ")
        if ch == '1': login_admin()
        elif ch == '2': login_customer()
        elif ch == '3': register_customer()
        elif ch == '0': break
        else: print("❌ Invalid")
        input("\nPress Enter...")

if __name__ == '__main__':
    portal()
    s.close()
