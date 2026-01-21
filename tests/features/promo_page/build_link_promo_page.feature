@build_link_promo_page @smoke @promo_page @regression
Feature: “Build A Link” forms on Special Promotions page
  As a user, I want to build a link on Promotions page follow the link to the destination page

  Background: User is on home page
    Given user logs in as a "user"
    Given user navigates to the "special-promotion" page

  @promo_page_successful @ui
  Scenario: User creates BC link on promo page successfully
    When user searches for "20% Off 100s of Wines" keyword on promo page
    When user filters by "Wine Access" brand on promo page
    When user sort by End Date and Oldest
    Then user should see the brand name on the first tile
    When user clicks on "Create Link" btn on the first tile
    Then user should be able to see a created deep link, copy link btn, FB and X share button
    When user clicks on Copy Link btn on promo page
    And opens the link
    Then the user should see the brand page that was used as Destination url.
    When user clicks on Export All button
    Then user sees downloaded file with name containing "special_promotions"

