import joblib


class UsersStorageController:
    def __init__(self):
        self._users_path = "../data/users/users.obj"

    def retrieve_users(self):  # It retrieves from a file all the registered users and associated data

        return joblib.load(self._users_path)

    def save_users(self, users):
        joblib.dump(users, self._users_path)


class User:  # Model class
    def __init__(self, name, awake_position, sleeping_position):
        self._name = name
        self._awake_position = awake_position
        self._sleeping_position = sleeping_position

    def set_awake_position(self, awake_position):
        self._awake_position = awake_position

    def get_awake_position(self):
        return self._awake_position

    def set_sleeping_position(self, sleeping_position):
        self._sleeping_position = sleeping_position

    def get_sleeping_position(self):
        return self._sleeping_position
