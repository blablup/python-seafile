from seafileapi.utils import urljoin


class Account(object):
    def __init__(self, client):
        self.client = client

    def client_login_token(self):
        response = self.client.post('/api2/client-login/')
        response_json = response.json()
        return response_json.get('token')

    def client_login_url(self):
        token = self.client_login_token()
        if token:
            return urljoin(self.client.server, '/client-login/?token={}'.format(token))
        else:
            return None

