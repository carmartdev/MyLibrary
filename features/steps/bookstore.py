#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep, time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def wait_for(fn, timeout=5):
    stime = time()
    while True:
        try:
            return fn()
        except (AssertionError, NoSuchElementException) as e:
            if time() - stime > timeout:
                raise e
            sleep(0.5)

@given("new browser session is started")
def clear_cookies(context):
    context.browser.delete_all_cookies()

@given("Betty opens bookstore homepage in her browser")
@when("Tang opens bookstore homepage in his browser")
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
        wait_for(lambda: context.browser.find_element_by_id("id-book-catalog"))
    except NoSuchElementException:
        context.test.fail("Book catalog not found on main page")

@then("she can see link to her cart in the top right corner")
def cart_link_is_in_top_right_corner(context):
    context.browser.set_window_size(1024, 768)
    cart = wait_for(lambda: context.browser.find_element_by_id("id-cart"))
    context.test.assertAlmostEqual(cart.location["x"] + cart.size["width"],
                                   964, delta=20)
    context.test.assertAlmostEqual(cart.location["y"], 0, delta=20)

@when("Betty adds book to cart")
@step("Betty adds to cart book '{number:n}'")
def add_book_to_cart(context, number=1):
    path = f"(//form[starts-with(@action, '/cart/')])[{number}]/button"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@given("Betty adds to cart book '{title}' by '{authors}'")
def add_book_to_cart(context, title, authors):
    path = f"//img[@alt='{title} by {authors}']/following::button"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@step("there is no counter near cart link")
def there_is_no_counter_near_cart_button(context):
    cart = wait_for(lambda: context.browser.find_element_by_id("id-cart"))
    context.test.assertEqual("🛒 Cart".upper(), cart.text)

@then("counter near cart link shows '{number:n}'")
def counter_shows(context, number):
    cart = wait_for(lambda: context.browser.find_element_by_id("id-cart"))
    context.test.assertIn(str(number), cart.text)

@then("button near book '{number}' now says '{button_caption}'")
def button_near_book_says(context, number, button_caption):
    path = f"(//form[starts-with(@action, '/cart/')])[{number}]/button"
    button = wait_for(lambda: context.browser.find_element_by_xpath(path))
    context.test.assertEqual(button.text.upper(), "in cart".upper())

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

@step("Betty clicks «cart» button")
def click_cart_button(context):
    wait_for(lambda: context.browser.find_element_by_id("id-cart")).click()

@given("Betty is on cart page")
@step("she is redirected to cart page")
def buyer_can_see_her_cart(context):
    context.test.assertIn("cart".upper(), context.browser.title.upper())

@step("she can see book '{title}' in her cart")
def buyer_can_see_book_in_her_cart(context, title):
    if not is_book_on_cart_page(context, title):
        context.test.fail(f"Buyer can't see book {title} in her cart")

@then("she can't see book '{title}' in her cart")
def buyer_can_see_book_in_her_cart(context, title):
    if is_book_on_cart_page(context, title):
        context.test.fail(f"Buyer can see book {title} in her cart. But shouldn't")

def is_book_on_cart_page(context, title):
    try:
        path = f"//td/a[contains(text(), '{title}')]"
        wait_for(lambda: context.browser.find_element_by_xpath(path))
        return True
    except NoSuchElementException:
        return False

@when("she changes quantity for '{title}' to '{qty:n}'")
def change_book_qty(context, title, qty):
    path = f"//td/a[contains(text(), '{title}')]/following::input"
    qty_input = wait_for(lambda: context.browser.find_element_by_xpath(path))
    qty_input.send_keys(Keys.CONTROL, 'a')
    qty_input.send_keys(Keys.DELETE)
    qty_input.send_keys(qty)
    wait_for(lambda: context.browser.find_element_by_name("update")).click()

@when("Betty deletes from cart book '{title}'")
def delete_book_from_cart(context, title):
    path = f"//td/a[contains(text(), '{title}')]/following::button"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@step("she can see that subtotal for her order is '{value}'")
def subtotal_is(context, value):
    t = wait_for(lambda: context.browser.find_element_by_id("id-total-price"))
    context.test.assertEqual(value, t.text)

@when("Betty clicks «checkout» button")
def click_checkout(context):
    wait_for(lambda: context.browser.find_element_by_id("id-checkout-button")
             ).click()

@then("she is redirected to checkout page")
def checkout_page_loaded(context):
    context.test.assertIn("Checkout", context.browser.title)

@step("Betty navigates to page '{page_num}'")
def navigate_to_page(context, page_num):
    context.browser.get(f"{context.base_url}/?page={page_num}")

@step("Betty clicks on cover of book '{number}'")
def click_on_book_cover(context, number):
    path = f"(//img[contains(@class, 'card-img-top')])[{number}]"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@step("Betty clicks on author name '{number}'")
def click_on_author_name(context, number):
    path = ("(//a[starts-with(@href, '/author/') and "
            f"starts-with(@title, 'Show more books by')])[{number}]")
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@step("she can see author's page")
def buyer_can_see_books_for_author(context):
    path = f"//h5[starts-with(text(), 'Books by ')]"
    wait_for(lambda: context.browser.find_element_by_xpath(path))

@when("Betty clicks back link")
def click_on_back_link(context):
    wait_for(lambda: context.browser.find_element_by_id("id-backlink")).click()

@step("she is redirected to page with book details")
def check_buyer_is_redirected_to_book_details(context):
    try:
        wait_for(lambda: context.browser.find_element_by_id("id-book-details"))
    except NoSuchElementException:
        context.test.fail("Book details not found on page")

@step("Betty types '{keyword}' in search bar")
def search(context, keyword):
    search = wait_for(lambda: context.browser.find_element_by_name("query"))
    search.send_keys(keyword)
    search.send_keys(Keys.ENTER)

@step("she can see search results for '{keyword}'")
def buyer_can_see_search_results_for(context, keyword):
    path = f"//h5[contains(text(), 'Search results for \"{keyword}\"')]"
    wait_for(lambda: context.browser.find_element_by_xpath(path))

@when("Betty clicks on next page")
def click_on_next_page(context):
    path = "//a[@aria-label='Next']"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@when("Betty clicks on previous page")
def click_on_previous_page(context):
    path = "//a[@aria-label='Previous']"
    wait_for(lambda: context.browser.find_element_by_xpath(path)).click()

@step("active page shows '{number:n}'")
def active_page_is(context, number):
    path = f"//li[contains(@class, 'active')]/a"
    active_page = wait_for(lambda: context.browser.find_element_by_xpath(path))
    context.test.assertIn(f"?page={number}", active_page.get_attribute("href"))
