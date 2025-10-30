from src.http_client import Client

USERS_ENPOINT = "/users"

class UserService:
    def __init__(self):
        self.client = Client()

    def get_user(self, user_id):
        url = f"{self.client.base_url}{USERS_ENPOINT}/{user_id}"
        return self.client.get_json(url)

    def get_users(self):
        url = f"{self.client.base_url}{USERS_ENPOINT}"
        return self.client.get_json(url)