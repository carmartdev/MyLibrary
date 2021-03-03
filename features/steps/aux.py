#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep, time
from selenium.common.exceptions import NoSuchElementException


def wait_for(fn, timeout=5):
    stime = time()
    while True:
        try:
            return fn()
        except (AssertionError, NoSuchElementException) as e:
            if time() - stime > timeout:
                raise e
            sleep(0.5)
