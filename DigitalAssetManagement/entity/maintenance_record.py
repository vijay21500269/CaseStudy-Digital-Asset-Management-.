class MaintenanceRecord:
    def __init__(self, maintenance_id=None, asset_id=None, maintenance_date=None, description=None, cost=None):
        self.__maintenance_id = maintenance_id
        self.__asset_id = asset_id
        self.__maintenance_date = maintenance_date
        self.__description = description
        self.__cost = cost

    # Getters and Setters
