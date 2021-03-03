#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from string import ascii_letters
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from store.models import Author, Book
from aux import wait_for

@given("new browser session is started")
def clear_cookies(context):
    context.browser.delete_all_cookies()

@given("Betty opens bookstore homepage in her browser")
@given("Tang opens bookstore homepage in his browser")
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

@then("she can see link to her cart in the top right corner")
def cart_link_is_in_top_right_corner(context):
    context.browser.set_window_size(1024, 768)
    cart = wait_for(lambda: context.browser.find_element_by_id("id_cart"))
    context.test.assertAlmostEqual(cart.location["x"] + cart.size["width"],
                                   964, delta=20)
    context.test.assertAlmostEqual(cart.location["y"], 0, delta=20)

@given("shopping cart is empty")
@then("his shopping cart is empty")
def cart_is_empty(context):
    cart = wait_for(lambda: context.browser.find_element_by_id("id_cart"))
    context.test.assertEqual("cart".upper(), cart.text.upper())

@when("Betty adds to cart book '{title}' by '{authors}'")
def add_book_to_cart(context, title, authors):
    path = f"//img[@alt='{title} by {authors}']/following::button"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@then("she notices counter near cart button showing '{number:n}'")
def counter_shows(context, number):
    cart = wait_for(lambda: context.browser.find_element_by_id("id_cart"))
    context.test.assertIn(str(number), cart.text)

@then("button near book '{title}' by '{authors}' now says '{button_caption}'")
def button_near_book_says(context, title, authors, button_caption):
    path = f"//img[@alt='{title} by {authors}']/following::button"
    button = wait_for(lambda: context.browser.find_element_by_xpath(path))
    context.test.assertEqual(button.text.upper(), "in cart".upper())

@step("shopping cart contains book '{title}'")
def book_in_cart(context, title):
    context.test.assertTrue(is_book_in_cart(context, title))

@when("Betty tries to add book '{title}' again")
def add_book_again(context, title):
    context.execute_steps(f"When Betty adds to cart book '{title}'")

@when("Betty clicks '{caption}' button")
def click_button(context, caption):
    path = f"//a[contains(text(), '{caption}')]"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@then("she is redirected to home page")
def buyer_can_see_home_page(context):
    context.test.assertIn("bookstore".upper(), context.browser.title.upper())

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

@when("she changes quantity for '{title}' to '{qty:n}'")
def change_book_qty(context, title, qty):
    path = f"//td[contains(text(), '{title}')]/following::input"
    qty_input = wait_for(lambda: context.browser.find_element_by_xpath(path))
    qty_input.send_keys(Keys.CONTROL, 'a')
    qty_input.send_keys(Keys.DELETE)
    qty_input.send_keys(qty)
    wait_for(lambda: context.browser.find_element_by_name("update")).click()

@when("Betty deletes from cart book '{title}'")
def delete_book_from_cart(context, title):
    path = f"//td[contains(text(), '{title}')]/following::button"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@step("shopping cart does not contain book '{title}'")
def book_not_in_cart(context, title):
    context.test.assertFalse(is_book_in_cart(context, title))

def is_book_in_cart(context, title):
    session_key = context.browser.get_cookie("sessionid").get("value")
    cart = context.session_store(session_key=session_key).get("cart")
    book_id = Book.objects.get(title=title).pk
    return str(book_id) in cart

@then("she can see that subtotal for her order is '{value}'")
def subtotal_is(context, value):
    t = wait_for(lambda: context.browser.find_element_by_id("id_total_price"))
    context.test.assertEqual(value, t.text)

@when("Betty clicks «checkout» button")
def click_checkout(context):
    wait_for(lambda: context.browser.find_element_by_id("id_checkout_button")
             ).click()

@then("she is redirected to checkout page")
def checkout_page_loaded(context):
    context.test.assertIn("Checkout", context.browser.title)

@when("Betty navigates to page '{page_num}'")
def navigate_to_page(context, page_num):
    context.browser.get(f"{context.base_url}/?page={page_num}")

@then("she is redirected to page '{page_num}'")
def check_buyer_is_redirected_to_page(context, page_num):
    context.test.assertEqual(f"{context.base_url}/?page={page_num}",
                             context.browser.current_url)

@when("Betty clicks on cover of book '{title}' by '{authors}'")
def click_on_book_cover(context, title, authors):
    path = f"//img[@alt='{title} by {authors}']"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@then("Betty is redirected to page with details for book '{title}' by '{authors}'")
def check_buyer_is_redirected_to_book_details(context, title, authors):
    context.test.assertIn(f"{title} by {authors}", context.browser.title)
