#!/usr/bin/env python3
# -*- coding: utf-8 -*-
@when("Betty opens bookstore homepage in her browser")
def load_home_page(context):
    context.browser.get(context.homepage)

@then("she will see '{title}' in browser title")
def titles_matches(context, title):
    context.test.assertIn(title, context.browser.title)
