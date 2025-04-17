import mysql.connector
from getpass import getpass
import hashlib


class LoginService:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def admin_login(self):
        print("\n🔐 Admin Login")
        username = input("Enter admin name: ")
        password = getpass("Enter password: ")

        hashed_pwd = password

        # Debugging print for query
        print(f"Executing query: SELECT * FROM admins WHERE username='{username}' AND password='{hashed_pwd}'")

        self.cursor.execute(
            "SELECT * FROM admins WHERE username=%s AND password=%s",
            (username, hashed_pwd)
        )
        admin = self.cursor.fetchone()
        if admin:
            print("✅ Admin login successful!\n")
            return True
        else:
            print("❌ Invalid admin credentials.\n")
            return False

    def employee_login(self):
        print("\n👷 Employee Login")
        name = input("Enter your name: ")
        password = getpass("Enter password: ")

        self.cursor.execute(
            "SELECT password, employee_id FROM employees WHERE name=%s",
            (name,)
        )
        record = self.cursor.fetchone()
        if record and record[0] == password:
            print("✅ Employee login successful!\n")
            return record[1]
        else:
            print("❌ Invalid employee credentials.\n")
            return None

    def validate_admin(self, username, password):
        hashed_pwd = password
        self.cursor.execute(
            "SELECT * FROM admins WHERE username=%s AND password=%s",
            (username, hashed_pwd)
        )
        admin = self.cursor.fetchone()
        return bool(admin)

    def validate_employee(self, name, password):
        self.cursor.execute(
            "SELECT employee_id, password FROM employees WHERE name=%s",
            (name,)
        )
        record = self.cursor.fetchone()
        if record and record[1] == password:
            return record[0]  # return employee_id
        return None

    def register_employee(self, name, department, email, password):
        self.cursor.execute("""
            INSERT INTO employees (name, department, email, password)
            VALUES (%s, %s, %s, %s)
        """, (name, department, email, password))
        self.conn.commit()
        print("✅ Registered Successfully!\n")
