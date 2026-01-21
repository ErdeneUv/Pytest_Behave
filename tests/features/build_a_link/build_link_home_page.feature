@build_link_homepage @build_a_link @ui @smoke @regression
Feature: Build A Link feature on HomePage
  As a user, I want to build a link on the HomePage

  Background: User is on home page
    Given user logs in as a "user"

  @page_loads_completely
  Scenario: User should see Homepage loads completely
    Then user should see snapshot report title
    Then user should see build a link form title
    Then user should see Featured Announcements
    Then user should see Socials
    Then user should see Blogs
    Then user should see bottom elements


  @build_link_homepage_successful
  Scenario Outline: Build a link on HomePage
    When user enters supported brand "<url>" into Destination URL input
    And user clicks on Create Short URL button to get long url
    When user clicks the Create Deep Link btn
    Then the user should get a short or long brandcycle link
    When user clicks on Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

    Examples:
      | url           |
      | underarm_url  |
      | underarm_cat  |
      | underarm_prod |


  @inactive_brand_homepage
  Scenario: User fails to build a link with inactive brand url
    When user enters "inactive_brand_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg
    Then user should not see the brand in BrandPage

  @blacklisted_homepage
  Scenario: Blacklisted user fails to build a link
    When user enters "blacklisted_brand_url" into Destination URL input for a brand they are blacklisted for
    And user clicks the Create Deep Link btn
    Then user should see "This brand is private and requires special approval." msg
    Then user should not see the brand in BrandPage

  @private_brand_whitelisted_homepage
  Scenario: Whitelisted users successfully build a Private brand link
    When user enters supported brand "whitelisted_private_brand_url" into Destination URL input
    And user clicks on Create Short URL button to get long url
    And user clicks the Create Deep Link btn
    Then the user should get a short or long brandcycle link
    When user clicks on Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

  @private_brand_not_whitelisted_homepage
  Scenario: User, who is NOT whitelisted, fails to build a Private brand link
    When user enters "private_brand_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is private and requires special approval." msg
    Then user should not see the brand in BrandPage

  @Deeplink_Disabled_homepage
  Scenario: User fails to build a brand link with a supported brand that's not Deeplink enabled.
    When user enters "inner_no_deeplink_brand_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "The brand has not authorized deep links for this domain." msg

  @empty_link_build_homepage
  Scenario: User enters no url into Destination URL
    When user clicks the Create Deep Link btn
    Then user should see the "Destination URL can not be empty" error message

  @incomplete_url_no_dot_com_homepage
  Scenario: User enters url without .com or .net
    When user enters "no_dot_com_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg

  @not_supported_url_homepage
  Scenario: User tries to build a link for not supported brand
    When user enters "not_supported_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg

