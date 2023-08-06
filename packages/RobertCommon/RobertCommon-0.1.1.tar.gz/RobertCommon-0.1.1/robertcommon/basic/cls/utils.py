from functools import wraps
from threading import Thread
from typing import Callable

# 单例模式
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

'''
#元类
class SingClass(metaclass=Singleton):
    def __init__(self):
        pass
'''


def daemon_thread(fn: Callable) -> Callable[..., Thread]:

    @wraps(fn)
    def _wrap(*args, **kwargs) -> Thread:
        return Thread(target=fn, args=args, kwargs=kwargs, daemon=True)

    return _wrap

'''
 @daemon_thread
    def thread_func():
        pass
'''