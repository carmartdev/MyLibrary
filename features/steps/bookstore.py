#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException

@when("Betty opens bookstore homepage in her browser")
def load_home_page(context):
    context.browser.get(context.homepage)

@then("she notices the page title and header mention '{title}'")
def page_title_and_header_mention_bookstore(context, title):
    context.test.assertIn(title, context.browser.title)

@then("she see book catalog on main page")
def she_see_book_catalog_on_main_page(context):
    try:
        context.browser.find_element_by_id("id_book_catalog")
    except NoSuchElementException:
        context.test.fail("Book catalog not found on main page")

@when("Betty clicks «add to cart» button near 1st book")
def add_to_cart_1st_book(context):
    table = context.browser.find_element_by_id("id_book_catalog")
    rows = table.find_elements_by_tag_name("tr")
    path = ".//button"
    rows[0].find_element_by_xpath(".//button").click()

@then("popup appears saying that book was added to her cart")
def popup_book_added_to_the_cart_is_shown(context):
    raise NotImplementedError("STEP: Then popup appears saying that book was added to her cart")

@when("Betty clicks «add to cart» button near 2nd book")
def add_to_cart_2nd_book(context):
    raise NotImplementedError("STEP: When Betty clicks «add to cart» button near 2nd book")

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
