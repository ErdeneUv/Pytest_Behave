@brands_index_page @ui @regression
Feature: Brands Index page and it's Category Filter, Select a Brand and Letter filter, as well as Featured brands
  As a user, I want to find a brand using Filters and search function on Brand Index page and visit Featured Brands on this page

  Background: User is on home page
    Given user logs in as a "user"
    Given user navigates to the "Brands" page

  @brands_page_featured_brands
  Scenario: User should see Featured brands title, featured brands logos and click to see brand's homepage
    When user clicks on featured brands logo
    Then user should land on brand's detail page
    Then user should see featured brands logos

  @brands_index_page_Cat_and_Letter_filters
  Scenario: User should be able to filter by category and first letter of the brand
    When user clicks on Category Filter and clicks on Food and Drink
    When user clicks on letter B filter
    Then user should see only these Brand with these ID
      | Brand                      | ID   |
      | Bean Box                   | 1022 |
      | BJ's Wholesale Club        | 1093 |
      | Black Rifle Coffee Company | 1212 |
      | Blue Apron                 | 381  |
      | Bobbie                     | 1114 |
      | ButcherBox                 | 847  |
    Then user should see Clear button on Cat and Letter Filters
    Then user should not see other letters
    When user clicks on Clear button on Cat Filter
    Then user should see total number of brands greater than previous results


  @brands_index_page_brand_search
  Scenario: User should be able to find a brand using Select a Brand function
    When user clicks on Select a Brand and search for "Melissa & Doug"
    Then user should see Category and Letter filters got reset and their Clear button are not displayed
    Then user should see only "Melissa & Doug" under letter "M"


  @brands_page_details_and_forms
  Scenario: User should see brand's details and all four forms
    When user clicks on Select a Brand and search for "Allbirds"
    And user clicks on that brand from the search result to open it
    Then user should see brands detail
    Then user should see Create Homepage Link form
    Then user should see Create A Custom Tracking Link form
    Then user should see Share Special Promotions form
    Then user should see Share Banners form

