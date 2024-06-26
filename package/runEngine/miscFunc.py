# -*- coding: utf-8 -*-
INF = 1.0e6
BIG_M = 1.0e2

def _judger(key1, key2) -> bool:
    return (key1 or (key2 is not None) or (key2 is True)) and (key2 is not False)
