@build_link_brand_page @ui @smoke @regression
Feature: “Build A Link” forms on Brands page
  As a user, I want to build a link on Brands, Promotions, and Tools pages

  Background: User is on home page
    Given user logs in as a "user"
    Given user navigates to the "brands" page

  @brand_page_successful
  Scenario Outline: Build a link on Brand page
    When user clicks on Select a Brand and search for "<supported brand>"
    And user clicks on that brand from the search result to open it
    When user enters supported brand "<url>" into Destination URL input on brand page
    And user clicks on Create Short URL button to get long url on brands page
    And user clicks the Create Deep Link btn on brands_page
    Then user should see an affiliate link
    When user clicks on brand_pages Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

    Examples:
      | supported brand | url            |
      | lululemon       | lululemon_url  |
      | lululemon       | lululemon_cat  |
      | lululemon       | lululemon_prod |



  #@brand_page_other_brand_link
  #This scenario is commented out since now portal supports creating link in brand detail page using any brands link
  #Scenario Outline: User shouldn't build a link with any other brands url
    #When user searches for "<supported brand>"
    #And user clicks on that brand from the search result to open it
    #When user enters supported brand "mismatch_brand" into Destination URL input on brand page
    #And user clicks the Create Deep Link btn
    #Then user should see "Destination URL does not match Brand URL." msg on brands_page

    #Examples:
     # | supported brand |
      #| hsn             |
      #| qvc             |

  @brand_page_deeplink_not_enabled
  Scenario: User should see short and long links instead of create a link form
    When user searches for "Age of Learning"
    And user clicks on that brand from the search result to open it
    Then user should see short and long link


  @brand_page_private_brand
  Scenario Outline: User, who is whitelisted, should be able to create a link of private brand
    When user searches for "<whitelisted_private_brand>"
    And user clicks on that brand from the search result to open it
    When user enters supported brand "<url>" into Destination URL input on brand page
    And user clicks on Create Short URL button to get long url on brands page
    And user clicks the Create Deep Link btn on brands_page
    Then user should see an affiliate link
    And user should see copy link button and x's share button
    When user clicks on X share button
    Then user navigate to X page
    When user clicks on brand_pages Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

    Examples:
      | whitelisted_private_brand | url        |
      | zappos                    | zappos_url |

  @brand_page_incomplete_url
  Scenario: User should see the error msg upon entering incomplete url
    When user searches for "Michael Kors"
    And user clicks on that brand from the search result to open it
    When user enters supported brand "no_dot_com_url" into Destination URL input on brand page
    And user clicks the Create Deep Link btn on brands_page
    Then user should see "THIS BRAND IS NOT CURRENTLY AVAILABLE ON BRANDCYCLE" msg on brands_page

  @brand_page_empty_url
  Scenario: User should see the error msg upon entering emtpy url
    When user searches for "crocs"
    And user clicks on that brand from the search result to open it
    And user clicks the Create Deep Link btn on brands_page
    Then user should see "Destination URL can not be empty." msg on brands_page

  @brand_page_link_share
  Scenario Outline: User should be able to use FB and X's share btn to share the created link
    When user searches for "<supported brand>"
    And user clicks on that brand from the search result to open it
    When user enters supported brand "<url>" into Destination URL input on brand page
    #And user clicks on Create Short URL button to get long url on brands page - took out because we don't support FB share on long links due to FB cutting off the long links.
    And user clicks the Create Deep Link btn on brands_page
    Then user should see an affiliate link
    When user clicks on FB share button
    Then user navigate to FB page
    When user comes back to the brand page
    And user clicks on X share button
    Then user navigate to X page

    Examples:
      | supported brand | url       |
      | crocs           | crocs_url |