#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from store.models import Book

BROWSER_PATH = "/usr/bin/firefox"

def rmdir(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fname in filenames:
            os.remove(os.path.join(dirpath, fname))
        for dname in dirnames:
            rmdir(os.path.join(dirpath, dname))
    os.rmdir(path)

def fill_test_database():
    for i in range(10):
        Book(title=f"Book title {i}", author=f"Author {i}", price=0.0).save()

def before_all(context):
    fill_test_database()
    options = Options()
    # options.headless = True
    context.browser = webdriver.Firefox(
        firefox_binary=FirefoxBinary(BROWSER_PATH),
        service_log_path=os.devnull,
        options=options
    )
    context.tmpdir = context.browser.capabilities.get("moz:profile")

def after_all(context):
    context.browser.quit()
    if os.path.exists(context.tmpdir):
        rmdir(context.tmpdir)

def before_scenario(context, scenario):
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
        return
