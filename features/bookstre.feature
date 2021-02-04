Feature: Bookstore
    Betty (user) would like to order some books online.

    Background: fill test database
        Given a set of books
            | title         | author          | price |
            | Ohlolap       | Esuuz Phohoo    | 32.99 |
            | Aererey       | Pooepex Uojmeik | 14.99 |
            | Ocaimuh       | Aigah Baefeix   | 23.49 |
            | Peele Zoos    | Teo Faquiey     | 88.99 |
            | Eupif Eengvoh | Ebohfee Acutoh  | 21.99 |

    Scenario: Betty has heard about a cool new online bookstore.
        When Betty opens bookstore homepage in her browser
        Then she notices the page title and header mention 'Bookstore'
            And she see book catalog on main page

        When Betty clicks «add to cart» button near 1st book
        Then she notices counter near cart button shows 1

        When Betty tries to add 1st book to cart again
        Then she notices counter near cart button shows 1

        When Betty clicks «add to cart» button near 2nd book
        Then she notices that counter value is now 2

        When Betty clicks «cart» button
        Then she see 2 recently added books in her cart

        When Betty clicks «checkout» button
        Then she is redirected to the page with list of payment methods
