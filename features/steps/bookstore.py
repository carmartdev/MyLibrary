#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep, time
from selenium.common.exceptions import NoSuchElementException
from store.models import CartItem, Book

def wait_for(fn, timeout=5):
    stime = time()
    while True:
        try:
            return fn()
        except (AssertionError, NoSuchElementException) as e:
            if time() - stime > timeout:
                raise e
            sleep(0.5)

@given("a set of books is available for sale")
def fill_test_database(context):
    for b in context.table:
        Book(title=b["title"], author=b["author"], price=b["price"]).save()

@given("Betty opens bookstore homepage in her browser")
def load_home_page(context):
    context.browser.get(context.base_url)

@then("she notices the page title and header mention '{title}'")
def page_title_and_header_mention_bookstore(context, title):
    context.test.assertIn(title, context.browser.title)
    context.test.assertIn(title,
                          context.browser.find_element_by_tag_name('h1').text)

@then("she can see book catalog on main page")
def book_catalog_on_main_page(context):
    try:
        wait_for(lambda: context.browser.find_element_by_id("id_book_catalog"))
    except NoSuchElementException:
        context.test.fail("Book catalog not found on main page")

@given("shopping cart is empty")
def cart_is_empty(context):
    context.test.assertEqual(CartItem.objects.count(), 0)

@when("Betty adds to cart book '{title}'")
def add_book_to_cart(context, title):
    path = f"//td[contains(text(), '{title}')]/following::button"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@then("she notices counter near cart button showing '{number:n}'")
def counter_shows(context, number):
    cart = wait_for(lambda: context.browser.find_element_by_id("id_cart"))
    context.test.assertIn(str(number), cart.text)

@step("shopping cart contains book '{title}'")
def cart_contains_book(context, title):
    try:
        CartItem.objects.get(book=Book.objects.get(title=title))
    except CartItem.DoesNotExist:
        context.test.fail(f"Book {title} not found in shopping cart")
    except Book.DoesNotExist:
        context.test.fail(f"Book {title} does not exist in catalog")

@when("Betty tries to add book '{title}' again")
def add_book_again(context, title):
    context.execute_steps(f"When Betty adds to cart book '{title}'")

@when("Betty clicks «cart» button")
def click_cart_button(context):
    wait_for(lambda: context.browser.find_element_by_id("id_cart")).click()

@given("Betty is on cart page")
@then("she is redirected to cart page")
def buyer_can_see_her_cart(context):
    context.test.assertIn("cart".upper(), context.browser.title.upper())

@then("she can see book '{title}' in her cart")
def buyer_can_see_book_in_her_cart(context, title):
    try:
        path = f"//td[contains(text(), '{title}')]"
        wait_for(lambda: context.browser.find_element_by_xpath(path))
    except NoSuchElementException:
        context.test.fail(f"Buyer can't see book {title} in her cart")

@when("Betty clicks «checkout» button")
def click_checkout(context):
    wait_for(lambda: context.browser.find_element_by_id("id_checkout_button")
             ).click()

@then("she is redirected to checkout page")
def list_of_payment_methods_is_shown(context):
    context.test.assertIn("Checkout", context.browser.title)
