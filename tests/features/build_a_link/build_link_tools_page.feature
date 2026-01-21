@build_link_tools_page @ui @regression
Feature: “Build A Link” forms Tools pages and in the extension
  As a user, I want to build a link on Brands, Promotions, Tools pages and in extensions


  Background: User is on home page
    Given user logs in as a "user"
    Given user navigates to build a link tab

  @build_link_tab @smoke
  Scenario Outline: On Tools page, user uses build a link form on Tools page
    When user enters "<supported_brand>" into Destination URL input on build a link tab
    And user clicks on Create Short URL button on Tools Page
    And user clicks the Create Deep Link btn
    Then user should see "Your custom link has been created" msg, and custom link, and Build another link btn
    When user clicks on Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

    Examples:
      | supported_brand  |
      | michaelkors_url  |
      | michaelkors_cat  |
      | michaelkors_prod |


  @build_link_tab_inactive_brand
  Scenario: On Tools page, user fails to build a link using inactive brand url
    When user enters "inactive_brand_url" into Destination URL input on build a link tab
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg


  @build_link_tab_blacklisted
  Scenario: On Tools page, blacklisted user fails to build a link
    When user enters "blacklisted_brand_url" into Destination URL input for a brand they are blacklisted for
    And user clicks the Create Deep Link btn
    Then user should see "This brand is private and requires special approval." msg


  @build_link_tab_private_brand_whitelisted
  Scenario: On Tools page, whitelisted users successfully build a Private brand link
    When user enters "whitelisted_private_brand_url" into Destination URL input on build a link tab
    And user clicks the Create Deep Link btn
    And user clicks on Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

  @build_link_tab_private_brand_not_whitelisted
  Scenario: On Tools page, user, who is NOT whitelisted, fails to build a Private brand link
    When user enters "private_brand_url" into Destination URL input on build a link tab
    And user clicks the Create Deep Link btn
    Then user should see "This brand is private and requires special approval." msg


  @build_link_tab_deeplink_Disabled
  Scenario: On Tools page, user fails to build a brand link with a supported brand that's not Deeplink enabled.
    When user enters "inner_no_deeplink_brand_url" into Destination URL input on build a link tab
    And user clicks the Create Deep Link btn
    Then user should see "The brand has not authorized deep links for this domain." msg

  @build_link_tab_empty_link_build
  Scenario: On Tools page, user enters no url into Destination URL
    When user clicks the Create Deep Link btn
    Then user should see the "Destination URL can not be empty" error message

  @build_link_tab_incomplete_url_no_dot_com
  Scenario: On Tools page, user enters url without .com or .net
    When user enters "no_dot_com_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg

  @build_link_tab_not_supported_url
  Scenario: On Tools page, user tries to build a link for not supported brand
    When user enters "not_supported_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg
