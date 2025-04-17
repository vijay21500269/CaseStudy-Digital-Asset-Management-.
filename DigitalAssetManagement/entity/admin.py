class Admin:
    def __init__(self, admin_id, username, password):
        self.__admin_id = admin_id
        self.__username = username
        self.__password = password

    def get_admin_id(self):
        return self.__admin_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password
