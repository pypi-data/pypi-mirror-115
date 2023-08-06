import requests

class UserCredentials:

    def __init__(self, username, token=None, permissions=None):
        self.username = username
        self.token = token
        self.permissions = permissions

    def to_json(self):
        return {"username": self.username, "token": self.token}

    @staticmethod
    def from_json(json):
        username = json['username']
        token = None
        permissions = None
        if 'token' in json:
            token = json['token']
        if 'permissions' in json:
            permissions = json['permissions']
        return UserCredentials(username, token, permissions)


class AuthClient:
    def __init__(self, host):
        self.host = host
        self.auth_endpoint = "http://%s/api/v2.0/auth" % self.host

    def auth_user(self, username, password):
        credentials = UserCredentials(username, password)
        response = requests.post(self.auth_endpoint, json=credentials.to_json())
        if response.status_code != 200:
            return False
        else:
            return UserCredentials.from_json(response.json())
