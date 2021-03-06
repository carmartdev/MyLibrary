#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from aux import wait_for

@when("Betty types '{keyword}' in search bar")
def search(context, keyword):
    search = wait_for(lambda: context.browser.find_element_by_name("query"))
    search.send_keys(keyword)
    search.send_keys(Keys.ENTER)
    path = f"//h5[contains(text(), 'Search results for \"{keyword}\"')]"
    wait_for(lambda: context.browser.find_element_by_xpath(path))

@then("she can see book '{title}' by '{authors}' in search results")
def book_is_on_page(context, title, authors):
    try:
        path = f"//img[@alt='{title} by {authors}']"
        wait_for(lambda: context.browser.find_element_by_xpath(path))
    except NoSuchElementException:
        msg = f"Book {title} by {authors} not found in search results"
        context.test.fail(msg)

@when("clicks on next page")
def click_on_next_page(context):
    path = f"//a[@aria-label='Next']"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()
