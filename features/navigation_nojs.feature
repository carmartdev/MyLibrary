Feature: Navigation
    As a buyer
    In order to discover new interesting books
    I want simple and joyful way to investigate catalog

    Scenario: buyer can navigate through catalog via pagination bar
        Given Betty opens bookstore homepage in her browser
            And active page shows '1'
        When Betty clicks on next page
        Then active page shows '2'

        Given active page shows '2'
        When Betty clicks on previous page
        Then active page shows '1'

    Scenario: buyer can see description by clicking on book cover
        Given Betty opens bookstore homepage in her browser
        When Betty clicks on cover of book '1'
        Then she is redirected to page with book details

    Scenario: buyer can see books writen by author clicking on his name
        Given Betty opens bookstore homepage in her browser
            And Betty clicks on cover of book '1'
        When Betty clicks on author name '1'
        Then she can see author's page

    Scenario: buyer can return back to the same page in catalog after seeing description
        Given Betty opens bookstore homepage in her browser
            And Betty navigates to page '2'
            And Betty clicks on cover of book '1'
            And she is redirected to page with book details
        When Betty clicks back link
        Then she can see book catalog on main page
            And active page shows '2'

    Scenario: buyer can return back to authors page after seeing description
        Given Betty opens bookstore homepage in her browser
            And Betty clicks on cover of book '1'
            And Betty clicks on author name '1'
            And she can see author's page
            And Betty clicks on cover of book '1'
            And she is redirected to page with book details
        When Betty clicks back link
        Then she can see author's page

    Scenario: buyer can search books in catalog from catalog
        Given Betty opens bookstore homepage in her browser
        When Betty types 'dog' in search bar
        Then she can see search results for 'dog'

    Scenario: buyer can search books in catalog from book details
        Given Betty opens bookstore homepage in her browser
            And Betty clicks on cover of book '1'
            And she is redirected to page with book details
        When Betty types 'dog' in search bar
        Then she can see search results for 'dog'

    Scenario: buyer can navigate search results
        Given Betty opens bookstore homepage in her browser
            And Betty types 'cat' in search bar
            And she can see search results for 'cat'
            And active page shows '1'
        When Betty clicks on next page
        Then active page shows '2'
        When Betty clicks on previous page
        Then active page shows '1'

    Scenario: buyer can return back to search results after seeing description
        Given Betty opens bookstore homepage in her browser
            And Betty types 'bear' in search bar
            And she can see search results for 'bear'
            And Betty clicks on cover of book '1'
            And she is redirected to page with book details
        When Betty clicks back link
        Then she can see search results for 'bear'
