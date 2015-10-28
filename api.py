import logging
import requests

try:
    # python2
    from urlparse import urljoin
except ImportError:
    # python3
    from urllib.parse import urljoin


class KisiApi:
    """ Class to interface with KISI API
    """

    def __init__(self, email, password):
        self.session = requests.Session()
        self.base_url = 'https://api.getkisi.com'
        self.auth_token = ''
        self.login(email, password)

    def login(self, email, password):
        """
        Login to API

        :return: Authentication token from KISI API
        """
        auth_json = {'user': {'email': email, 'password': password}}
        resp = self.send_api('POST', 'users/sign_in', json=auth_json)
        self.auth_token = resp.json()['authentication_token']
        logging.debug('Got authentication token {}'.format(self.auth_token))
        return self.auth_token

    def get_lock_id(self, lock_name):
        """ Get ID of the first lock that contains lock_name text """
        resp = self.send_api('GET', '/locks')
        locks = resp.json()
        lock = next((lock for lock in locks if lock_name in lock['name']))
        real_lock_name = lock['name']
        lock_id = lock['id']
        logging.info('Found lock: "{}" (ID: {})'.format(real_lock_name,
                                                        lock_id))
        return lock_id

    def unlock(self, lock_name):
        """
        Unlock first lock that contains lock_name text

        :return: JSON response from KISI API
        """
        lock_id = self.get_lock_id(lock_name)
        logging.debug('Unlocking lock ID {}'.format(lock_id))
        resp = self.send_api('POST', '/locks/{}/access'.format(lock_id))
        result = resp.json()
        logging.info(result)
        return result

    def send_api(self, method, endpoint, **kwargs):
        """ Send call to API

        :param method: HTTP method ('GET', 'POST', etc.)
        :param endpoint: API endpoint to join to the base url
        :kwargs: keyword arguments that will be added to API request, e.g.
        json={'key', 'value}
        """
        url = urljoin(self.base_url, endpoint)
        req = requests.Request(method, url, headers=self.get_headers(),
                               **kwargs)
        logging.debug('Sending {} request to {}'.format(req.method, req.url))
        prepped = req.prepare()
        resp = self.session.send(prepped)
        resp.raise_for_status()
        return resp

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'X-Authentication-Token': self.auth_token
        }
