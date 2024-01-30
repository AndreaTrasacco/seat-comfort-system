import joblib


class UsersStorageController:
    def __init__(self):
        self._users_path = "../server/data/users/"

    def retrieve_user(self, name):  # It retrieves from a file the registered user and associated data
        return joblib.load(self._users_path + name)

    def save_user(self, user):  # It saves the user
        joblib.dump(user, self._users_path + user.get_name())

