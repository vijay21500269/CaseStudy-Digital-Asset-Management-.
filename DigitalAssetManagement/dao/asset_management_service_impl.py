from dao.asset_management_service import AssetManagementService
import mysql.connector
from myexceptions.asset_not_found_exception import AssetNotFoundException

class AssetManagementServiceImpl(AssetManagementService):

    def __init__(self, conn=None):
        if conn:
            self.conn = conn
        else:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='#vijaysql**',
                database='dig_asset'
            )
        self.cursor = self.conn.cursor()

    def add_asset(self, name, asset_type, serial_number, purchase_date, location, status, owner_id):
        self.cursor.execute("""
            INSERT INTO assets (name, type, serial_number, purchase_date, location, status, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, asset_type, serial_number, purchase_date, location, status, owner_id))
        self.conn.commit()

    def update_asset(self, asset_id, location=None, status=None):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        if not self.cursor.fetchone():
            raise AssetNotFoundException(f"Asset with ID {asset_id} not found.")
        updates = []
        values = []
        if location:
            updates.append("location=%s")
            values.append(location)
        if status:
            updates.append("status=%s")
            values.append(status)
        if updates:
            query = f"UPDATE assets SET {', '.join(updates)} WHERE asset_id=%s"
            values.append(asset_id)
            self.cursor.execute(query, tuple(values))
            self.conn.commit()

    def delete_asset(self, asset_id):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        if not self.cursor.fetchone():
            raise AssetNotFoundException(f"Asset with ID {asset_id} not found.")
        self.cursor.execute("DELETE FROM assets WHERE asset_id=%s", (asset_id,))
        self.conn.commit()

    def allocate_asset(self, asset_id, employee_id, allocation_date):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        asset = self.cursor.fetchone()
        if not asset:
            raise AssetNotFoundException("Asset not found.")
        if asset[6].lower() != "available":
            raise Exception("Asset is not available for allocation.")

        self.cursor.execute("""
            SELECT * FROM reservations 
            WHERE asset_id = %s 
            AND status = 'approved' 
            AND %s BETWEEN start_date AND end_date
        """, (asset_id, allocation_date))
        if self.cursor.fetchone():
            raise Exception("Asset is reserved during this date and cannot be allocated.")

        self.cursor.execute("""
            INSERT INTO asset_allocations (asset_id, employee_id, allocation_date)
            VALUES (%s, %s, %s)
        """, (asset_id, employee_id, allocation_date))

        self.cursor.execute("UPDATE assets SET status='allocated' WHERE asset_id=%s", (asset_id,))
        self.conn.commit()
        return True

    def deallocate_asset(self, asset_id):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        if not self.cursor.fetchone():
            raise AssetNotFoundException(f"Asset with ID {asset_id} not found.")
        self.cursor.execute("DELETE FROM asset_allocations WHERE asset_id=%s", (asset_id,))
        self.cursor.execute("UPDATE assets SET status='available' WHERE asset_id=%s", (asset_id,))
        self.conn.commit()

    def perform_maintenance(self, asset_id, maintenance_date, description, cost):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        if not self.cursor.fetchone():
            raise AssetNotFoundException(f"Asset with ID {asset_id} not found.")
        self.cursor.execute("""
            INSERT INTO maintenance_records (asset_id, maintenance_date, description, cost)
            VALUES (%s, %s, %s, %s)
        """, (asset_id, maintenance_date, description, cost))
        self.conn.commit()

    def reserve_asset(self, asset_id, employee_id, reservation_date, start_date, end_date, status):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        if not self.cursor.fetchone():
            raise AssetNotFoundException(f"Asset with ID {asset_id} not found.")

        self.cursor.execute("""
            SELECT * FROM reservations
            WHERE asset_id = %s AND status IN ('approved', 'pending')
            AND (
                (start_date <= %s AND end_date >= %s) OR
                (start_date <= %s AND end_date >= %s)
            )
        """, (asset_id, start_date, start_date, end_date, end_date))

        if self.cursor.fetchone():
            print("This asset is already reserved during the selected period.")
            return False

        self.cursor.execute("""
            INSERT INTO reservations (asset_id, employee_id, reservation_date, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (asset_id, employee_id, reservation_date, start_date, end_date, status))
        self.conn.commit()
        print("Asset reserved successfully.")
        return True

    def withdraw_reservation(self, reservation_id):
        self.cursor.execute("SELECT * FROM reservations WHERE reservation_id = %s", (reservation_id,))
        reservation = self.cursor.fetchone()
        if not reservation:
            raise Exception("Reservation not found.")
        if reservation[6].lower() == "canceled":
            raise Exception("Reservation is already canceled.")

        asset_id = reservation[1]

        self.cursor.execute("""
            UPDATE reservations SET status = 'canceled' 
            WHERE reservation_id = %s
        """, (reservation_id,))

        self.cursor.execute("""
            SELECT COUNT(*) FROM reservations 
            WHERE asset_id = %s AND status IN ('pending', 'approved')
        """, (asset_id,))
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("UPDATE assets SET status = 'available' WHERE asset_id = %s", (asset_id,))
        self.conn.commit()
        return True

    # --- NEW METHODS ADDED BELOW ---

    def get_pending_reservations(self):
        self.cursor.execute("SELECT * FROM reservations WHERE status = 'pending'")
        return self.cursor.fetchall()

    def approve_reservation(self, reservation_id):
        self.cursor.execute("SELECT * FROM reservations WHERE reservation_id = %s", (reservation_id,))
        if not self.cursor.fetchone():
            raise Exception("Reservation not found.")
        self.cursor.execute("""
            UPDATE reservations SET status = 'approved' 
            WHERE reservation_id = %s
        """, (reservation_id,))
        self.conn.commit()
        return True

    def get_asset_allocations(self):
        self.cursor.execute("""
            SELECT a.asset_id, a.name, aa.employee_id, aa.allocation_date 
            FROM asset_allocations aa 
            JOIN assets a ON a.asset_id = aa.asset_id
        """)
        return self.cursor.fetchall()

    def get_available_assets(self):
        self.cursor.execute("SELECT * FROM assets WHERE status = 'available'")
        return self.cursor.fetchall()

    def get_all_reservations(self):
        self.cursor.execute("""
            SELECT reservation_id, asset_id, employee_id, start_date, end_date, status
            FROM reservations
        """)
        return self.cursor.fetchall()
