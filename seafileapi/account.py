from seafileapi.utils import utf8lize, urljoin


class Account(object):
    """
    A seafile account
    """
    def __init__(self, client, id, email, create_time, is_active, is_staff, usage, total, login_time = 0):
        self.client = client
        self.id = id
        self.email = email
        self.create_time = create_time
        self.last_login = login_time
        self.is_active = is_active
        self.is_staff = is_staff
        self.usage = usage
        self.total = total

    def __repr__(self):
        return '<{} "{}" active={} staff={}>'.format(self.__class__.__name__,
                                                     self.email,
                                                     self.is_active,
                                                     self.is_staff)

    @classmethod
    def from_json(cls, client, account_json):
        account_json = utf8lize(account_json)
        account_id = account_json['id']
        email = account_json['email']
        create_time = account_json['create_time']
        last_login = account_json['last_login']
        is_active = account_json['is_active']
        is_staff = account_json['is_staff']
        usage = account_json['usage']
        total = account_json['total']

        return cls(client, account_id, email, create_time, is_active, is_staff, usage, total)


class AccountApi(object):
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
