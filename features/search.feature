Feature: Search
    As a buyer
    I want to find books in store quickly.

    Scenario: buyer should be able to search books in catalog
        Given Betty opens bookstore homepage in her browser
        When Betty types 'dog' in search bar
        Then she can see book 'Caring For Your Dog' by 'June Preszler' in search results

    Scenario: buyer should be able to navigate search results
        Given Betty opens bookstore homepage in her browser
        When Betty types 'cat' in search bar
            And clicks on next page
        Then she can see book 'Underworld' by 'Catherine MacPhail' in search results
