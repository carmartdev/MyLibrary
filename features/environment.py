#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import os
from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

BROWSER_PATH = "/usr/bin/firefox"

def rmdir(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fname in filenames:
            os.remove(os.path.join(dirpath, fname))
        for dname in dirnames:
            rmdir(os.path.join(dirpath, dname))
    os.rmdir(path)

@fixture
def selenium_browser_firefox(context):
    options = Options()
    # options.headless = True
    context.browser = webdriver.Firefox(
        firefox_binary=FirefoxBinary(BROWSER_PATH),
        service_log_path=os.devnull,
        options=options
    )
    tmpdir = context.browser.capabilities.get("moz:profile")
    yield context.browser

    # cleanup-fixture part:
    context.browser.quit()
    if os.path.exists(tmpdir):
        rmdir(tmpdir)

def before_all(context):
    use_fixture(selenium_browser_firefox, context)
