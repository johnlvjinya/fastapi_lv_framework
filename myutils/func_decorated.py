#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import time
from functools import wraps


def log_func_time(func):
    """
    装饰器：用来记录没有加 async 定义的被装饰函数/方法运行时间
    Args:
        func:

    Returns:

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_t = time.time()
        resp = func(*args, **kwargs)
        cost = (time.time() - start_t)
        # msg = 'func time spend info: [func: {func}] [cost: {cost:.3f} ms] [args: {args}]  [kwargs: {kwargs}]'\
        #     .format(func=func.__name__,
        #             cost=cost,
        #             args=args,
        #             kwargs=kwargs)
        msg = 'func time spend info: [func: {func}] [cost: {cost:.3f} sec] [args: {args}]'.format(func=func.__name__,cost=cost,args=args,)
        print(msg)
        return resp

    return wrapper
