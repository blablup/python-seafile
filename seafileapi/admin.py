from seafileapi.account import Account
from seafileapi.exceptions import UserExisted, DoesNotExist


class AdminUserReference(object):
    """An account reference obtained by SeafileAdmin.list_users"""
    def __init__(self, email, source=None):
        self.email = email
        self.source = source

    def __repr__(self):
        return '<{} "{}" ({})>'.format(self.__class__.__name__,
                                       self.email,
                                       self.source or 'Unknown source')

    def resolve(self, client):
        """Resolve this reference into a seafileapi.account.Account object, using `client`"""
        return client.admin.get_user(self.email)


class SeafileAdmin(object):
    def __init__(self, client):
        self.client = client

    def list_users(self, start=0, limit=0, scope=None):
        """Return a list of AdminUserReference objects from the /accounts/ API"""
        VALID_SCOPES = ['LDAP', 'DB']
        if scope is not None and scope not in VALID_SCOPES:
            raise ValueError('Scope can be one of {}'.format(VALID_SCOPES))
        params = {
            'start': start,
            'limit': limit
        }
        if scope is not None:
            params['scope'] = scope
        response = self.client.get('/api2/accounts/', params=params)
        response_json = response.json()
        users = []
        for user_json in response_json:
            users.append(AdminUserReference(email=user_json['email'], source=user_json.get('source')))
        return users

    def search_user(self, filter):
        """Search for user accounts, to be used by autocompleters"""
        params = {'q': filter}
        response = self.client.get('/api2/search-user', params=params)
        response_json = response.json()
        return response_json['users']

    def get_user(self, email):
        account_json = self.client.get('/api2/accounts/{}/'.format(email)).json()
        return Account.from_json(self.client, account_json)

    def create_user(self, email, password, is_active=True, is_staff=False):
        url = '/api2/accounts/{}/'.format(email)
        params = {'password': password,
                  'is_active': is_active and 'true' or 'false',
                  'is_staff': is_staff and 'true' or 'false'}
        result = self.client.put(url, data=params, expected=[200, 201])
        if result.status_code == 201:
            return result.json()  # User created
        elif result.status_code == 200:
            raise UserExisted()

    def update_user(self, email, **kwargs):
        """Update a user account. Any of the following keys must be provided:
            - password, is_staff, is_active, name, note, storage."""
        url = '/api2/accounts/{}/'.format(email)
        params = {}
        attrs = ['password', 'is_active', 'is_staff', 'name', 'note', 'storage']
        for attr in attrs:
            if attr in kwargs:
                val = kwargs.pop(attr)
                if val is not None:
                    params[attr] = val
        result = self.client.put(url, data=params, expected=[200, 201, 400])
        if result.status_code == 400:
            raise DoesNotExist('User {}'.format(email))
        return True

    def delete(self, email):
        url = '/api2/accounts/{}/'.format(email)
        result = self.client.delete(url, expected=[200, 202])
        if result.status_code == 200:
            return True
        elif result.status_code == 202:
            raise DoesNotExist('User {}'.format(email))

    def list_user_repos(self, username):
        pass

    def is_exist_group(self,group_name):
        pass
