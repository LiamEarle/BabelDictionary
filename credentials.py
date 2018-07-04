import json
import os


class TwitterCredentials(object):
    def __init__(self, path):
        if not os.path.exists(path):
            raise ValueError('The specified path to credentials does not exist!')

        with open(path, encoding='utf-8') as file:
            self.credentials = dict(json.load(file))

    def get_consumer_key(self):
        """
        Returns the Twitter Consumer Key
        :return: String consumer_key
        """
        return self.credentials.get('consumer_key', '')

    def get_consumer_secret(self):
        """
        Returns the Twitter Consumer Secret
        :return: String consumer_secret
        """
        return self.credentials.get('consumer_secret', '')

    def get_access_token_key(self):
        """
        Returns the Twitter Access Token Key
        :return: String access_token_key
        """
        return self.credentials.get('access_token_key', '')

    def get_access_token_secret(self):
        """
        Returns the Twitter Access Token Secret
        :return: String access_token_secret
        """
        return self.credentials.get('access_token_secret', '')
