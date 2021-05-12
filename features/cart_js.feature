@javascript
Feature: Shopping Cart
    As a buyer
    In order to select items for eventual purchase
    I want to accumulate a list of items for purchase while investigating catalog

    Scenario: when buyer adds book to cart she is redirected to the same page
        Given Betty opens bookstore homepage in her browser
            And Betty navigates to page '2'
        When Betty adds to cart book '1'
        Then active page shows '2'

    Scenario: buyer can see cart contents by clicking on cart link
        Given Betty opens bookstore homepage in her browser
            And there is no counter near cart link
            And Betty adds to cart book '100 Malicious Little Mysteries' by 'Isaac Asimov'
        When Betty clicks «cart» button
        Then she is redirected to cart page
            And she can see book '100 Malicious Little Mysteries' in her cart

    Scenario: buyer can add book to cart from catalog
        Given Betty opens bookstore homepage in her browser
            And there is no counter near cart link
        When Betty adds to cart book '1'
        Then counter near cart link shows '1'
            And button near book '1' now says 'In Cart'

    Scenario: buyer can add book to cart from book description
        Given Betty opens bookstore homepage in her browser
            And there is no counter near cart link
            And Betty clicks on cover of book '100 Malicious Little Mysteries' by 'Isaac Asimov'
        When Betty adds book to cart
        Then counter near cart link shows '1'

    Scenario: buyer can't add same book to cart more than once
        Given Betty opens bookstore homepage in her browser
            And there is no counter near cart link
        When Betty adds to cart book '1'
        Then counter near cart link shows '1'
        When Betty adds to cart book '1'
        Then she is redirected to cart page
        When Betty clicks close button
        Then counter near cart link shows '1'

    Scenario: buyer can add to cart as many different books as she wants
        Given Betty opens bookstore homepage in her browser
            And there is no counter near cart link
        When Betty adds to cart book '1'
        Then counter near cart link shows '1'
        When Betty adds to cart book '2'
        Then counter near cart link shows '2'

    Scenario: buyer can change books quantity in cart
        Given Betty opens bookstore homepage in her browser
            And Betty adds to cart book '100 Malicious Little Mysteries' by 'Isaac Asimov'
            And Betty clicks «cart» button
            And she can see that subtotal for her order is '$15.60'
        When she changes quantity for '100 Malicious Little Mysteries' to '2'
        Then she can see that subtotal for her order is '$31.20'

    Scenario: buyer can delete books from cart
        Given Betty opens bookstore homepage in her browser
            And Betty adds to cart book '100 Malicious Little Mysteries' by 'Isaac Asimov'
            And Betty clicks «cart» button
            And she can see book '100 Malicious Little Mysteries' in her cart
        When Betty deletes from cart book '100 Malicious Little Mysteries'
        Then she can't see book '100 Malicious Little Mysteries' in her cart

    Scenario: buyer can go to checkout page from shopping cart
        Given Betty opens bookstore homepage in her browser
            And Betty adds to cart book '1'
            And Betty clicks «cart» button
        When Betty clicks «checkout» button
        Then she is redirected to checkout page

    Scenario: different buyers have separate carts
        Given Betty opens bookstore homepage in her browser
        When Betty adds to cart book '1'
        Then counter near cart link shows '1'

        Given new browser session is started
        When Tang opens bookstore homepage in his browser
        Then there is no counter near cart link
