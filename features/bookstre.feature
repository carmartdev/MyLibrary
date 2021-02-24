Feature: Bookstore

    Scenario: as buyer Betty would like to order some books online
        Given Betty opens bookstore homepage in her browser
        Then she notices the page title and header mention 'Bookstore'
            And she can see book catalog on main page
            And she can see link to her cart in the top right corner

        Given shopping cart is empty
        When Betty adds to cart book '100 malicious little mysteries' by 'Isaac Asimov'
        Then she notices counter near cart button showing '1'
            And shopping cart contains book '100 malicious little mysteries'
            And button near book '100 malicious little mysteries' by 'Isaac Asimov' now says 'In Cart'

        Given shopping cart contains book '100 malicious little mysteries'
        When Betty tries to add book '100 malicious little mysteries' by 'Isaac Asimov' again
        Then she is redirected to cart page

        Given Betty is on cart page
        When Betty clicks 'continue shopping' button
        Then she is redirected to home page

        Given shopping cart contains book '100 malicious little mysteries'
        When Betty adds to cart book '101 family vacation games' by 'Shando Varda'
        Then she notices counter near cart button showing '2'
            And shopping cart contains book '100 malicious little mysteries'
            And shopping cart contains book '101 family vacation games'

        Given shopping cart contains book '100 malicious little mysteries'
            And shopping cart contains book '101 family vacation games'
        When Betty clicks «cart» button
        Then she is redirected to cart page
            And she can see book '100 malicious little mysteries' in her cart
            And she can see book '101 family vacation games' in her cart

        Given Betty is on cart page
            And shopping cart contains book '100 malicious little mysteries'
            And shopping cart contains book '101 family vacation games'
        Then she can see that subtotal for her order is '$55.90'

        Given Betty is on cart page
            And shopping cart contains book '100 malicious little mysteries'
            And shopping cart contains book '101 family vacation games'
        When she changes quantity for '101 family vacation games' to '2'
        Then she can see that subtotal for her order is '$96.20'

        Given Betty is on cart page
            And shopping cart contains book '101 family vacation games'
        When Betty deletes from cart book '101 family vacation games'
        Then shopping cart does not contain book '101 family vacation games'

        Given Betty is on cart page
        When Betty clicks «checkout» button
        Then she is redirected to checkout page

        Given new browser session is started
            And Tang opens bookstore homepage in his browser
        Then his shopping cart is empty

    Scenario: when buyer adds book to cart she is redirected to the same page
        Given Betty opens bookstore homepage in her browser
        When Betty navigates to page '17'
            And Betty adds to cart book 'Caring for your dog' by 'June Preszler'
        Then she is redirected to page '17'
