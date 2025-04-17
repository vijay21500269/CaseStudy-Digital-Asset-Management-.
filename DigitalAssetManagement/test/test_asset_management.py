import unittest
import mysql.connector
from dao.asset_management_service_impl import AssetManagementServiceImpl
from myexceptions.asset_not_found_exception import AssetNotFoundException
from dao.asset_management_service_impl import AssetManagementServiceImpl
class TestAssetManagement(unittest.TestCase):

    def setUp(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='#vijaysql**',
            database='digital_asset'  # or whatever test DB name you use
        )
        self.cursor = self.conn.cursor()
        self.service = AssetManagementServiceImpl(self.conn)

        # Clean database tables
        self.cursor.execute("DELETE FROM maintenance_records")
        self.cursor.execute("DELETE FROM asset_allocations")
        self.cursor.execute("DELETE FROM reservations")
        self.cursor.execute("DELETE FROM assets")
        self.cursor.execute("DELETE FROM employees")

        # Insert test employee
        self.cursor.execute("""
            INSERT INTO employees (employee_id, name, department, email, password)
            VALUES (1, 'Test User', 'IT', 'test@example.com', 'testpass')
        """)

        # Insert test asset with ID 100
        self.cursor.execute("""
            INSERT INTO assets (asset_id, name, type, serial_number, purchase_date, location, status, owner_id)
            VALUES (100, 'Projector', 'Electronics', 'SN99999', '2023-01-01', 'Room 303', 'available', 1)
        """)

        self.conn.commit()

    def tearDown(self):
        self.cursor.execute("DELETE FROM asset_allocations")
        self.cursor.execute("DELETE FROM reservations")
        self.cursor.execute("DELETE FROM maintenance_records")
        self.cursor.execute("DELETE FROM assets")
        self.cursor.execute("DELETE FROM employees")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_add_maintenance(self):
        self.service.perform_maintenance(100, '2025-03-31', "Routine check", 1500.00)
        self.cursor.execute("SELECT * FROM maintenance_records WHERE asset_id = 100")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[3], "Routine check")

    def test_asset_not_found_exception(self):
        with self.assertRaises(AssetNotFoundException):
            self.service.perform_maintenance(999, '2025-03-31', "Invalid", 500.00)

    def test_asset_allocation(self):
        result = self.service.allocate_asset(100, 1, '2025-03-31')
        self.assertTrue(result)
        self.cursor.execute("SELECT * FROM asset_allocations WHERE asset_id = 100")
        self.assertIsNotNone(self.cursor.fetchone())

    def test_asset_reservation(self):
        self.service.reserve_asset(100, 1, '2025-03-31', '2025-04-01', '2025-04-05', 'reserved')
        self.cursor.execute("SELECT * FROM reservations WHERE asset_id = 100")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[6], 'reserved')

if __name__ == '__main__':
    unittest.main()
