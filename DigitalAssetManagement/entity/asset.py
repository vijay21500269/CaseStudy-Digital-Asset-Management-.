class Asset:
    def __init__(self, asset_id=None, name=None, asset_type=None, serial_number=None, purchase_date=None,
                 location=None, status=None, owner_id=None):
        self.__asset_id = asset_id
        self.__name = name
        self.__asset_type = asset_type
        self.__serial_number = serial_number
        self.__purchase_date = purchase_date
        self.__location = location
        self.__status = status
        self.__owner_id = owner_id

    # Getters and Setters
