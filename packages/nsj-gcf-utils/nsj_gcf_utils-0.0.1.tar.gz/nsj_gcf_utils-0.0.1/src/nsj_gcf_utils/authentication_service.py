import json

from app_logger import logger
from google.cloud import secretmanager_v1 as secretmanager
from hashlib import sha256


class AuthenticationService:
    """
    This is by no mean a safe authentication system, its a simple authentication system
    """
    # {"keys": [
    #   {"id": "ANA-DP", "hash":key1},
    #   {"id": "USER2", "hash":key2},
    #   {"id": "USER3", "hash":key3}
    # ]}

    _api_keys = list()
    secret_client = None

    @classmethod
    def _get_client(cls):
        if cls.secret_client is None:
            cls.secret_client = secretmanager.SecretManagerServiceClient()
        return cls.secret_client

    def load_keys_from_secret(self, secret_uri, update=True):
        secret_client = AuthenticationService._get_client()
        keys = json.loads(secret_client.access_secret_version(
            name=secret_uri).payload.data.decode('UTF-8'))["keys"]
        self.load_keys_from_list(keys, update)
        return self

    def load_keys_from_list(self, keys, update=True):
        if update:
            self._api_keys += keys
        else:
            self._api_keys = keys
        return self

    def verify_api_key(self, api_key) -> str:
        """
        Returns the app_client id, if api_key is valid, or None otherwise.
        """
        for key in self._api_keys:
            hashed = sha256((key['id'] + api_key).encode('utf-8')).hexdigest()
            if hashed == key['hash']:
                logger.info(
                    "[%(class_name)s] - Authentication id = %(message)s",
                    {'class_name': self.__class__.__name__,
                     'message': key['id']})
                return key['id']
        return None


if __name__ == "__main__":
    import uuid
    client = "postman"
    api_key = str(uuid.uuid4())
    hashed = sha256((client + api_key).encode('utf-8')).hexdigest()
    print('api_key: ' + api_key)
    print('hashed: ' + hashed)
