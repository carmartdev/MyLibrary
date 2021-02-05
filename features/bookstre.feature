Feature: Bookstore

    Background: fill test database
        Given a set of books is available for sale
            | title         | author          | price |
            | Ohlolap       | Esuuz Phohoo    | 32.99 |
            | Aererey       | Pooepex Uojmeik | 14.99 |
            | Ocaimuh       | Aigah Baefeix   | 23.49 |
            | Peele Zoos    | Teo Faquiey     | 88.99 |
            | Eupif Eengvoh | Ebohfee Acutoh  | 21.99 |

    Scenario: as buyer Betty would like to order some books online
        Given Betty opens bookstore homepage in her browser
        Then she notices the page title and header mention 'Bookstore'
            And she can see book catalog on main page

        Given shopping cart is empty
        When Betty adds to cart book 'Ohlolap'
        Then she notices counter near cart button showing '1'
            And shopping cart contains book 'Ohlolap'

        Given shopping cart contains book 'Ohlolap'
        When Betty tries to add book 'Ohlolap' again
        Then she notices counter near cart button showing '1'

        Given shopping cart contains book 'Ohlolap'
        When Betty adds to cart book 'Aererey'
        Then she notices counter near cart button showing '2'
            And shopping cart contains book 'Ohlolap'
            And shopping cart contains book 'Aererey'

        Given shopping cart contains book 'Ohlolap'
            And shopping cart contains book 'Aererey'
        When Betty clicks «cart» button
        Then she is redirected to cart page
            And she can see book 'Ohlolap' in her cart
            And she can see book 'Aererey' in her cart

        Given Betty is on cart page
        When Betty clicks «checkout» button
        Then she is redirected to checkout page
