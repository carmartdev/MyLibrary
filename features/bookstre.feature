Feature: Bookstore
    Betty (user) would like to order some books online.

    Scenario: Betty has heard about a cool new online bookstore.
        When Betty opens bookstore homepage in her browser
        Then she notices the page title and header mention 'Bookstore'
            And she see book catalog on main page

        When Betty clicks «add to cart» button near 1st book
        Then popup appears saying that book was added to her cart

        When Betty clicks «add to cart» button near 2nd book
        Then popup appears saying that book was added to her cart

        When Betty clicks «cart» button
        Then she see 2 recently added books in her cart

        When Betty clicks «checkout» button
        Then she is redirected to the page with list of payment methods
