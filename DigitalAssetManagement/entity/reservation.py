class Reservation:
    def __init__(self, reservation_id=None, asset_id=None, employee_id=None, reservation_date=None,
                 start_date=None, end_date=None, status=None):
        self.__reservation_id = reservation_id
        self.__asset_id = asset_id
        self.__employee_id = employee_id
        self.__reservation_date = reservation_date
        self.__start_date = start_date
        self.__end_date = end_date
        self.__status = status

    # Getters and Setters
