# Toll Management System DB Setup
import mysql.connector as m

s = m.connect(user='root', host='localhost', passwd='2007', charset='utf8', auth_plugin='mysql_native_password')
c = s.cursor()

c.execute('CREATE DATABASE IF NOT EXISTS toll_management')
c.execute('USE toll_management')

# Admin Table
def Table_for_admins():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Admin (
            Id INT(6) PRIMARY KEY,
            Name VARCHAR(40),
            admin_key BIGINT,
            Designation VARCHAR(30),
            Salary_per_month INT
        )
    """)
    c.executemany("INSERT INTO Admin VALUES (%s, %s, %s, %s, %s)", [
        (100001, 'Ravi Nair', 9834567812, 'Owner', 150000),
        (100002, 'Anita Sharma', 9745623481, 'Supervisor', 95000),
        (100003, 'Jitendra Yadav', 9682456731, 'Clerk', 45000)
    ])

# Booth Table
def Table_for_booths():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Booth (
            booth_id INT(5) PRIMARY KEY,
            location VARCHAR(100),
            lane_count INT,
            is_active BOOLEAN
        )
    """)
    c.executemany("INSERT INTO Booth VALUES (%s, %s, %s, %s)", [
        (101, 'Delhi-Gurgaon Expressway', 8, True),
        (102, 'Mumbai-Pune Highway', 6, True),
        (103, 'NH48 - Vapi Checkpost', 4, True),
        (104, 'Bangalore Outer Ring Rd', 5, True)
    ])

# Vehicle Table
def Table_for_vehicles():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Vehicle (
            vehicle_id INT(10) PRIMARY KEY,
            plate_number VARCHAR(15),
            type VARCHAR(20),
            owner_name VARCHAR(40),
            registered_on DATE
        )
    """)
    c.executemany("INSERT INTO Vehicle VALUES (%s, %s, %s, %s, %s)", [
        (20001, 'DL3CAB1234', 'Car', 'Suresh Kumar', '2023-01-15'),
        (20002, 'MH12CD5678', 'SUV', 'Neha Jain', '2022-11-10'),
        (20003, 'GJ05KL4321', 'Truck', 'Irfan Shaikh', '2023-02-22'),
        (20004, 'KA01MN8888', 'Van', 'Lakshmi Rao', '2023-03-30'),
        (20005, 'TN22OP3344', 'Bus', 'Joseph Raj', '2022-09-18'),
        (20006, 'RJ14QR9988', 'Car', 'Meera Mehta', '2023-06-10'),
        (20007, 'PB10ST1234', 'Truck', 'Gurpreet Singh', '2023-04-04'),
        (20008, 'HR26UV5678', 'SUV', 'Divya Arora', '2022-12-20'),
        (20009, 'WB06WX3456', 'Bike', 'Rakesh Dey', '2023-07-01'),
        (20010, 'CH01YZ7890', 'Car', 'Kritika Bansal', '2023-05-11')
    ])

# Toll Rate Table
def Table_for_rates():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Toll_Rate (
            type VARCHAR(20) PRIMARY KEY,
            peak_rate DECIMAL(6,2),
            offpeak_rate DECIMAL(6,2)
        )
    """)
    c.executemany("INSERT INTO Toll_Rate VALUES (%s, %s, %s)", [
        ('Car', 120.00, 80.00),
        ('SUV', 150.00, 100.00),
        ('Truck', 200.00, 150.00),
        ('Bus', 180.00, 130.00),
        ('Bike', 50.00, 30.00),
        ('Van', 100.00, 70.00)
    ])

# Customer Account Table
def Table_for_customers():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            account_id INT PRIMARY KEY,
            name VARCHAR(40),
            balance DECIMAL(10,2),
            vehicle_id INT(10),
            password VARCHAR(40),
            FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id)
        )
    """)
    c.executemany("INSERT INTO Customer VALUES (%s, %s, %s, %s, %s)", [
        (501, 'Suresh Kumar', 350.00, 20001, 'suresh@123'),
        (502, 'Neha Jain', 180.00, 20002, 'neha@456'),
        (503, 'Irfan Shaikh', 50.00, 20003, 'irfan@789'),
        (504, 'Lakshmi Rao', 95.00, 20004, 'lakshmi@321'),
        (505, 'Joseph Raj', 125.00, 20005, 'joseph@654'),
        (506, 'Meera Mehta', 250.00, 20006, 'meera@987')
    ])

# Route Table
def Table_for_routes():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Route (
            route_id INT PRIMARY KEY AUTO_INCREMENT,
            entry_booth INT,
            exit_booth INT,
            distance_km DECIMAL(5,2),
            FOREIGN KEY (entry_booth) REFERENCES Booth(booth_id),
            FOREIGN KEY (exit_booth) REFERENCES Booth(booth_id)
        )
    """)
    c.executemany("INSERT INTO Route(entry_booth, exit_booth, distance_km) VALUES (%s, %s, %s)", [
        (101, 102, 140.50),
        (102, 103, 230.00),
        (103, 104, 120.75),
        (104, 101, 310.30)
    ])

# Emergency Vehicles Table
def Table_for_emergency():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Emergency_Vehicle (
            vehicle_id INT PRIMARY KEY,
            department VARCHAR(40),
            exemption_type VARCHAR(30),
            FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id)
        )
    """)
    c.executemany("INSERT INTO Emergency_Vehicle VALUES (%s, %s, %s)", [
        (20007, 'Fire Department', 'Toll-Free'),
        (20009, 'Ambulance Services', 'Toll-Free')
    ])

# Staff Table
def Table_for_staff():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Staff (
            staff_id INT PRIMARY KEY,
            name VARCHAR(40),
            booth_id INT,
            shift VARCHAR(20),
            role VARCHAR(30),
            salary INT,
            FOREIGN KEY (booth_id) REFERENCES Booth(booth_id)
        )
    """)
    c.executemany("INSERT INTO Staff VALUES (%s, %s, %s, %s, %s, %s)", [
        (601, 'Amit Verma', 101, 'Morning', 'Collector', 30000),
        (602, 'Priya Desai', 102, 'Night', 'Supervisor', 42000),
        (603, 'Karan Patel', 103, 'Evening', 'Security', 25000),
        (604, 'Sneha Rana', 104, 'Morning', 'Operator', 28000)
    ])

# Staff Shift Audit Table
def Table_for_audits():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Staff_Audit (
            audit_id INT AUTO_INCREMENT PRIMARY KEY,
            staff_id INT,
            booth_id INT,
            shift_start DATETIME,
            shift_end DATETIME,
            total_collection DECIMAL(10,2),
            FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
            FOREIGN KEY (booth_id) REFERENCES Booth(booth_id)
        )
    """)
    c.executemany("INSERT INTO Staff_Audit(staff_id, booth_id, shift_start, shift_end, total_collection) VALUES (%s, %s, %s, %s, %s)", [
        (601, 101, '2024-07-06 06:00:00', '2024-07-06 14:00:00', 15000.00),
        (602, 102, '2024-07-06 22:00:00', '2024-07-07 06:00:00', 18000.00),
        (603, 103, '2024-07-06 14:00:00', '2024-07-06 22:00:00', 12000.00)
    ])

# NEW: Violation Log Table
def Table_for_violation_log():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Violation_Log (
            violation_id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id INT,
            booth_id INT,
            violation_type VARCHAR(50),
            timestamp DATETIME,
            fine_amount DECIMAL(7,2),
            is_paid BOOLEAN,
            detected_by VARCHAR(50),
            FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
            FOREIGN KEY (booth_id) REFERENCES Booth(booth_id)
        )
    """)
    c.executemany("""
        INSERT INTO Violation_Log(vehicle_id, booth_id, violation_type, timestamp, fine_amount, is_paid, detected_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, [
        (20003, 103, 'Insufficient Balance', '2024-07-07 10:10:00', 200.00, False, 'AutoTrigger'),
        (20009, 101, 'Wrong Lane Entry', '2024-07-06 09:00:00', 500.00, False, 'CCTV'),
        (20007, 102, 'Overspeeding', '2024-07-06 14:30:00', 1000.00, True, 'SpeedGun'),
        (20004, 104, 'No FASTag Detected', '2024-07-07 11:32:00', 150.00, False, 'RFID'),
        (20010, 101, 'Barrier Tampering', '2024-07-07 12:00:00', 2000.00, True, 'Operator'),
        (20002, 103, 'Reverse Entry', '2024-07-05 08:45:00', 1200.00, False, 'SecurityCam'),
        (20006, 104, 'Unregistered Entry', '2024-07-06 15:15:00', 750.00, True, 'SystemScan')
    ])


# Transactions Table
def Table_for_transactions():
    c.execute("""
        CREATE TABLE IF NOT EXISTS Toll_Transaction (
            txn_id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT,
            vehicle_id INT(10),
            booth_id INT,
            timestamp DATETIME,
            toll_amount DECIMAL(7,2),
            payment_mode VARCHAR(20),
            FOREIGN KEY (account_id) REFERENCES Customer(account_id),
            FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
            FOREIGN KEY (booth_id) REFERENCES Booth(booth_id)
        )
    """)
    c.executemany("""
        INSERT INTO Toll_Transaction(account_id, vehicle_id, booth_id, timestamp, toll_amount, payment_mode)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, [
        (501, 20001, 101, '2024-07-07 08:20:00', 80.00, 'FASTag'),
        (502, 20002, 102, '2024-07-07 09:15:00', 150.00, 'Cash'),
        (503, 20003, 103, '2024-07-07 10:10:00', 200.00, 'FASTag'),
        (504, 20004, 104, '2024-07-07 11:30:00', 100.00, 'Card'),
        (505, 20005, 101, '2024-07-07 12:45:00', 180.00, 'Cash'),
        (506, 20006, 102, '2024-07-07 13:55:00', 80.00, 'FASTag')
    ])

# Smart Trigger
def Create_auto_fine_trigger():
    c.execute("DROP TRIGGER IF EXISTS auto_fine_insufficient_balance")
    c.execute("""
        CREATE TRIGGER auto_fine_insufficient_balance
        BEFORE INSERT ON Toll_Transaction
        FOR EACH ROW
        BEGIN
            DECLARE current_balance DECIMAL(10,2);
            SELECT balance INTO current_balance FROM Customer WHERE account_id = NEW.account_id;
            IF current_balance < NEW.toll_amount THEN
                INSERT INTO Violation_Log(vehicle_id, booth_id, violation_type, timestamp, fine_amount, is_paid, detected_by)
                VALUES (NEW.vehicle_id, NEW.booth_id, 'Insufficient Balance', NOW(), NEW.toll_amount, FALSE, 'AutoTrigger');
            END IF;
        END;
    """)

# Run All Setup
Table_for_admins()
Table_for_booths()
Table_for_vehicles()
Table_for_rates()
Table_for_customers()
Table_for_routes()
Table_for_emergency()
Table_for_staff()
Table_for_audits()
Table_for_violation_log()
Table_for_transactions()
Create_auto_fine_trigger()

s.commit()
print("✅ FULL ADVANCED Toll Management System DB — All tables preserved, linked, populated")
