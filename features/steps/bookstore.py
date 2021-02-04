#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep, time
from selenium.common.exceptions import NoSuchElementException
from store.models import Book

def wait_for(fn, timeout=5):
    stime = time()
    while True:
        try:
            return fn()
        except (AssertionError, NoSuchElementException) as e:
            if time() - stime > timeout:
                raise e
            sleep(0.5)

@given("a set of books")
def fill_test_database(context):
    userdata = context.config.userdata
    for row in context.table:
        Book(title=row["title"], author=row["author"], price=userdata.getint(row["price"])).save()

@when("Betty opens bookstore homepage in her browser")
def load_home_page(context):
    context.browser.get(context.base_url)

@then("she notices the page title and header mention '{title}'")
def page_title_and_header_mention_bookstore(context, title):
    context.test.assertIn(title, context.browser.title)

@then("she see book catalog on main page")
def she_see_book_catalog_on_main_page(context):
    try:
        wait_for(lambda: context.browser.find_element_by_id("id_book_catalog"))
    except NoSuchElementException:
        context.test.fail("Book catalog not found on main page")

@when("Betty clicks «add to cart» button near 1st book")
def add_to_cart_1st_book(context):
    table = wait_for(lambda: context.browser.find_element_by_id("id_book_catalog"))
    rows = table.find_elements_by_tag_name("tr")
    path = ".//button"
    rows[0].find_element_by_xpath(".//button").click()

@then("she notices counter near cart button shows 1")
def counter_shows_one(context):
    cart = wait_for(lambda: context.browser.find_element_by_id("id_cart"))
    context.test.assertIn("1", cart.text)

@when("Betty tries to add 1st book to cart again")
def add_book_to_cart_repeatedly(context):
    add_to_cart_1st_book(context)

@when("Betty clicks «add to cart» button near 2nd book")
def add_to_cart_2nd_book(context):
    table = wait_for(lambda: context.browser.find_element_by_id("id_book_catalog"))
    rows = table.find_elements_by_tag_name("tr")
    path = ".//button"
    rows[1].find_element_by_xpath(".//button").click()

@then("she notices that counter value is now 2")
def counter_shows_two(context):
    cart = wait_for(lambda: context.browser.find_element_by_id("id_cart"))
    context.test.assertIn("2", cart.text)

@when("Betty clicks «cart» button")
def click_cart_button(context):
    raise NotImplementedError("STEP: When Betty clicks «cart» button")

@then("she see 2 recently added books in her cart")
def two_books_in_the_cart(context):
    raise NotImplementedError("STEP: Then she see 2 recently added books in her cart")

@when("Betty clicks «checkout» button")
def click_checkout(context):
    raise NotImplementedError("STEP: When Betty clicks «checkout» button")

@then("she is redirected to the page with list of payment methods")
def list_of_payment_methods_is_shown(context):
    raise NotImplementedError("STEP: Then she is redirected to the page with list of payment methods")
