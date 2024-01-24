#!/usr/bin/env python3
"""
Redis module, Writing strings to Redis
Reading from Redis and recovering original type
Incrementing values, storing lists, Retrieving lists
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Returns wrapper
        """
        key_m = method.__qualname__
        self._redis.incr(key_m)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Prototype: def call_history(method: Callable) -> Callable:
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Returns wrapper
        """
        key = method.__qualname__
        inp = key + ':inputs'
        outp = key + ":outputs"
        data = str(args)
        self._redis.rpush(inp, data)
        fin = method(self, *args, **kwds)
        self._redis.rpush(outp, str(fin))
        return fin
    return wrapper


def replay(func: Callable):
    """
    Displays history of calls of a particular function
    """
    r = redis.Redis()
    key = func.__qualname__
    inp = r.lrange("{}:inputs".format(key), 0, -1)
    outp = r.lrange("{}:outputs".format(key), 0, -1)
    calls_number = len(inp)
    times_str = 'times'
    if calls_number == 1:
        times_str = 'time'
    fin = '{} was called {} {}:'.format(key, calls_number, times_str)
    print(fin)
    for k, v in zip(inp, outp):
        fin = '{}(*{}) -> {}'.format(
            key_m, k.decode('utf-8'), v.decode('utf-8'))
        print(fin)


class Cache():
    """
    Store instance of Redis client as private variable _redis and
    Flush the instance using flushdb and
    """
    def __init__(self):
        """
        Prototype: def __init__(self):
        Store instance of Redis client as private variable _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store history of inputs and outputs for particular function
        """
        gen = str(uuid.uuid4())
        self._redis.set(gen, data)
        return gen

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Convert data back to desired format
        """
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_int(self, key):
        return self.get(key, int)

    def get_str(self, key):
        value = self._redis.get(key)
        return value.decode("utf-8")
