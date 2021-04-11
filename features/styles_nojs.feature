Feature: Styles
    As a webmaster
    In order to ensure store is displayed properly
    I want to check CSS is loaded correctly

    Scenario: buyer can see expected elements in their appropriate locations
        Given Betty opens bookstore homepage in her browser
        Then she notices the page title and header mention 'Bookstore'
            And she can see book catalog on main page
            And she can see link to her cart in the top right corner
