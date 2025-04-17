from dao.asset_management_service_impl import AssetManagementServiceImpl
from myexceptions.asset_not_found_exception import AssetNotFoundException
from myexceptions.asset_not_maintain_exception import AssetNotMaintainException
from dao.login_service import LoginService
import getpass
import mysql.connector
service = AssetManagementServiceImpl()
class AssetManagementApp:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#vijaysql**",
            database="dig_asset"
        )
        self.login_service = LoginService(self.conn)  # ✅ pass conn here
        self.service = AssetManagementServiceImpl(self.conn)

    def display_admin_menu(self):
        print("\n=== 🔐 Admin Panel ===")
        print("1. Add Asset")
        print("2. Update Asset")
        print("3. Delete Asset")
        print("4. Allocate Asset")
        print("5. Deallocate Asset")
        print("6. Perform Maintenance")
        print("7. Approve Reservations")
        print("8. Withdraw Reservation")
        print("9. Exit")

    def display_employee_menu(self):
        print("\n=== 👷 Employee Panel ===")
        print("1. View Allocated Assets")
        print("2. View Available Assets")
        print("3. View All Reservations")
        print("4. Reserve Asset")
        print("5. Exit")

    def run_admin_tasks(self):
        while True:
            self.display_admin_menu()
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    name = input("Enter asset name: ")
                    asset_type = input("Enter asset type: ")
                    serial_number = input("Enter serial number: ")
                    purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
                    location = input("Enter location: ")
                    status = input("Enter status (in use / decommissioned / under maintenance): ")
                    owner_id = input("Enter owner ID: ")
                    self.service.add_asset(name, asset_type, serial_number, purchase_date, location, status, owner_id)
                    print("✔️ Asset added successfully.")

                elif choice == "2":
                    asset_id = int(input("Enter asset ID to update: "))
                    new_location = input("Enter new location: ")
                    new_status = input("Enter new status: ")
                    self.service.update_asset(asset_id, new_location, new_status)
                    print("✔️ Asset updated successfully.")

                elif choice == "3":
                    asset_id = int(input("Enter asset ID to delete: "))
                    self.service.delete_asset(asset_id)
                    print("✔️ Asset deleted successfully.")

                elif choice == "4":
                    asset_id = int(input("Enter asset ID to allocate: "))
                    employee_id = int(input("Enter employee ID: "))
                    allocation_date = input("Enter allocation date (YYYY-MM-DD): ")
                    self.service.allocate_asset(asset_id, employee_id, allocation_date)
                    print("✔️ Asset allocated successfully.")

                elif choice == "5":
                    asset_id = int(input("Enter asset ID to deallocate: "))
                    self.service.deallocate_asset(asset_id)
                    print("✔️ Asset deallocated successfully.")

                elif choice == "6":
                    asset_id = int(input("Enter asset ID for maintenance: "))
                    maintenance_date = input("Enter maintenance date (YYYY-MM-DD): ")
                    description = input("Enter maintenance description: ")
                    cost = float(input("Enter maintenance cost: "))
                    self.service.perform_maintenance(asset_id, maintenance_date, description, cost)
                    print("✔️ Maintenance performed successfully.")

                elif choice == "7":
                    pending_reservations = self.service.get_pending_reservations()
                    if not pending_reservations:
                        print("📭 No pending reservations.")
                    else:
                        print("\nPending Reservations:")
                        for res in pending_reservations:
                            print(res)
                        res_id = int(input("Enter reservation ID to approve: "))
                        self.service.approve_reservation(res_id)
                        print("✅ Reservation approved.")

                elif choice == "8":
                    reservation_id = int(input("Enter reservation ID to withdraw: "))
                    success = self.service.withdraw_reservation(reservation_id)
                    if success:
                        print("✔️ Reservation withdrawn successfully.")

                elif choice == "9":
                    print("🚪 Exiting admin panel...")
                    break

                else:
                    print("❌ Invalid choice. Try again.")

            except AssetNotFoundException as e:
                print(f"❌ {e}")
            except AssetNotMaintainException as e:
                print(f"❌ {e}")
            except Exception as e:
                print(f"❌ Error: {e}")

    def run_employee_tasks(self, emp_id):
        while True:
            self.display_employee_menu()
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    allocations = self.service.get_asset_allocations()
                    print("\n📋 Asset Allocations:")
                    print("Asset ID | Name            | Employee ID | Allocation Date")
                    print("-" * 55)
                    for asset_id, name, emp_id, alloc_date in allocations:
                        print(f"{asset_id:<9} | {name:<15} | {emp_id:<11} | {alloc_date.strftime('%Y-%m-%d')}")




                elif choice == "2":

                    assets = self.service.get_available_assets()

                    print("\n📦 Available Assets:")

                    print("Asset ID | Name            | Type           | Serial Number")

                    print("-" * 65)

                    for asset in assets:
                        asset_id, name, type_, serial_number = asset[:4]

                        print(f"{asset_id:<8} | {name:<15} | {type_:<14} | {serial_number}")



                elif choice == "3":

                    reservations = self.service.get_all_reservations()

                    print("\n📅 All Reservations:")

                    print("Reservation ID | Asset ID | Employee ID | Start Date  | End Date    | Status")

                    print("-------------------------------------------------------------------------------")

                    for r in reservations:
                        reservation_id, asset_id, employee_id, start_date, end_date, status = r

                        print(
                            f"{reservation_id:<15} | {asset_id:<8} | {employee_id:<12} | {start_date} | {end_date} | {status}")


                elif choice == "4":
                    asset_id = int(input("Enter asset ID to reserve: "))
                    reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    self.service.reserve_asset(asset_id, emp_id, reservation_date, start_date, end_date, "pending")
                    print("🕒 Reservation created with status 'pending'.")

                elif choice == "5":
                    print("🚪 Exiting employee panel...")
                    break

                else:
                    print("❌ Invalid choice. Try again.")

            except Exception as e:
                print(f"❌ Error: {e}")

    def login_or_register(self):
        print("\n🔐 Welcome to Asset Management System")
        print("1. Admin Login")
        print("2. Employee Login")
        print("3. Employee Registration")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            if self.login_service.validate_admin(username, password):
                print(f"\n👑 Welcome Admin {username}!")
                self.run_admin_tasks()
            else:
                print("❌ Invalid admin credentials.")

        elif choice == "2":
            name = input("Enter employee name: ")
            password = input("Enter password: ")
            emp_id = self.login_service.validate_employee(name, password)
            if emp_id:
                print(f"\n👋 Welcome Employee {name}!")
                self.run_employee_tasks(emp_id)
            else:
                print("❌ Invalid employee credentials.")

        elif choice == "3":
            print("\n📝 Employee Registration:")
            name = input("Name: ")
            password = input("Password: ")
            department = input("Department: ")
            email = input("Enter email: ")
            self.login_service.register_employee(name, department, email, password)
            print("✅ Registration successful! You can now login.")

        elif choice == "4":
            print("👋 Exiting... Goodbye!")
            exit()
        else:
            print("❌ Invalid option.")

    def run(self):
        while True:
            self.login_or_register()


if __name__ == "__main__":
    app = AssetManagementApp()
    app.run()