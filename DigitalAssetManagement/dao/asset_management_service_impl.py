from dao.asset_management_service import AssetManagementService
import mysql.connector
from myexceptions.asset_not_found_exception import AssetNotFoundException

class AssetManagementServiceImpl(AssetManagementService):

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='#vijaysql**',
            database='digital_asset'
        )
        self.cursor = self.conn.cursor()

    def add_asset(self, name, asset_type, serial_number, purchase_date, location, status, owner_id):
        self.cursor.execute("""
            INSERT INTO assets (name, type, serial_number, purchase_date, location, status, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, asset_type, serial_number, purchase_date, location, status, owner_id))
        self.conn.commit()

    def update_asset(self, asset_id, name=None, location=None, status=None):
        updates = []
        values = []
        if name:
            updates.append("name=%s")
            values.append(name)
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
        self.cursor.execute("DELETE FROM assets WHERE asset_id=%s", (asset_id,))
        self.conn.commit()

    def allocate_asset(self, asset_id, employee_id, allocation_date):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        asset = self.cursor.fetchone()
        if not asset:
            raise AssetNotFoundException("Asset not found.")
        if asset[6] != "available":
            print("Asset is not available for allocation.")
            return None
        self.cursor.execute("""
            INSERT INTO asset_allocations (asset_id, employee_id, allocation_date)
            VALUES (%s, %s, %s)
        """, (asset_id, employee_id, allocation_date))
        self.cursor.execute("UPDATE assets SET status='allocated' WHERE asset_id=%s", (asset_id,))
        self.conn.commit()
        return True

    def deallocate_asset(self, asset_id):
        self.cursor.execute("DELETE FROM asset_allocations WHERE asset_id=%s", (asset_id,))
        self.cursor.execute("UPDATE assets SET status='available' WHERE asset_id=%s", (asset_id,))
        self.conn.commit()

    def perform_maintenance(self, asset_id, maintenance_date, description, cost):
        self.cursor.execute("SELECT * FROM assets WHERE asset_id=%s", (asset_id,))
        asset = self.cursor.fetchone()
        if not asset:
            raise AssetNotFoundException("Asset not found.")
        self.cursor.execute("""
            INSERT INTO maintenance_records (asset_id, maintenance_date, description, cost)
            VALUES (%s, %s, %s, %s)
        """, (asset_id, maintenance_date, description, cost))
        self.conn.commit()

    def reserve_asset(self, asset_id, employee_id, reservation_date, start_date, end_date, status):
        self.cursor.execute("""
            INSERT INTO reservations (asset_id, employee_id, reservation_date, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (asset_id, employee_id, reservation_date, start_date, end_date, status))
        self.conn.commit()

    def withdraw_reservation(self, reservation_id):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            get_query = """select r.asset_id, a.status 
                          from reservations r
                          join assets a on r.asset_id = a.asset_id
                          where r.reservation_id = %s"""
            cursor.execute(get_query, (reservation_id,))
            reservation = cursor.fetchone()
            if not reservation:
                raise AssetNotFoundException("reservation id not found.")
            asset_id, current_status = reservation
            if current_status.lower() != 'reserved':
                print(f"cannot withdraw reservation - asset is not reserved (current status: {current_status})")
                return False
            update_asset_query = "update assets set status = 'available' where asset_id = %s"
            cursor.execute(update_asset_query, (asset_id,))
            update_reservation_query = "update reservations set status = 'withdrawn' where reservation_id = %s"
            cursor.execute(update_reservation_query, (reservation_id,))
            conn.commit()
            print("reservation withdrawn successfully! asset is now available.")
            return True
        except mysql.connector.Error as e:
            print(f"database error: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()