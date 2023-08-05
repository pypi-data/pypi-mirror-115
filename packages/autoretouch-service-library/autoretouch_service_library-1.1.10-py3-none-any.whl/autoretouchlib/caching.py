import hashlib
import json
import logging
import os
import pickle
import canonicaljson
import fakeredis
import redis
from fastapi.encoders import jsonable_encoder
from typing import Dict


class CachingService:
    """CachingService for processed content"""

    def __init__(self, component_name: str, component_version: str, commit_hash: str, storage=fakeredis.FakeStrictRedis()):
        self.enabled = True
        self.redis_host = os.environ.get('REDISHOST', 'localhost')
        self.redis_port = int(os.environ.get('REDISPORT', 6379))
        self.redis_password = os.environ.get('REDISPASSWORD', '')
        self.component_name = component_name
        self.component_version = component_version
        self.commit_hash = commit_hash

        if self.redis_host != 'localhost':
            if self.component_name == '':
                logging.fatal("setting an empty component_name can lead to \
                              unwanted cache hits with other components")
                self.enabled = False
            self.__db = self.__redis_connect__(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password)
            if self.__db is None:
                self.enabled = False
        else:
            self.__db = storage

    @ staticmethod
    def __redis_connect__(
            host: str,
            port: int,
            password: str,
            timeout=5) -> redis.client.Redis:
        try:
            client = redis.Redis(
                host=host,
                port=port,
                password=password,
                socket_timeout=timeout,
            )
            ping = client.ping()
            if ping is True:
                return client
        except redis.AuthenticationError:
            logging.error("AuthenticationError")
            return None

    @ staticmethod
    def __create_hash_key__(hashable_request: str) -> str:
        m = hashlib.sha256()
        m.update(hashable_request)
        return m.hexdigest().lower()

    @ staticmethod
    def extend_dict(request: Dict, **kwargs) -> Dict:
        for key, value in kwargs.items():
            request[key] = value
        return request

    def get(self, request: Dict) -> str:
        """Returns output contentHashes for a request if hashKey exists in cache"""
        if not self.enabled:
            raise CouldNotCacheContentException
        request['component_name'] = self.component_name
        request['component_version'] = self.component_version
        request['commit_hash'] = self.commit_hash
        hashableRequest = canonicaljson.encode_canonical_json(request)
        hashKey = self.__create_hash_key__(hashableRequest)
        binaryContentHashes = self.__db.get(hashKey)
        if binaryContentHashes is None:
            raise NoCacheHitException
        outPutContentHashes = json.loads(pickle.loads(binaryContentHashes))
        return outPutContentHashes

    def set(self, request: Dict, response: Dict) -> str:
        if not self.enabled:
            raise CouldNotCacheContentException
        """Loads contentHash for processed content to cache"""
        request['component_name'] = self.component_name
        request['component_version'] = self.component_version
        request['commit_hash'] = self.commit_hash
        hashableRequest = canonicaljson.encode_canonical_json(request)
        hashKey = self.__create_hash_key__(hashableRequest)
        try:
            binary_response = pickle.dumps(
                json.dumps(jsonable_encoder(response)))
            self.__db.set(hashKey, binary_response)
            return hashKey
        except Exception:
            raise CouldNotCacheContentException


class CouldNotCacheContentException(Exception):
    """Raised when content could not be cached"""
    pass


class NoCacheHitException(Exception):
    """Raised when no cache hit"""
    pass
