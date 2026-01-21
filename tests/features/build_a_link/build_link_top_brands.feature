@top5
Feature: Build A Link feature smoke test against top 5 performing brands, plus a brand from remaining networks
  As a user, I want to build a link using top 5 brands plus a brand from remaining networks


  @build_link_homepage_successful_top5
  Scenario Outline: Build a link on HomePage
    Given user logs in as a "user"
    When user enters supported brand "<url>" into Destination URL input
    And user clicks on Create Short URL button to get long url
    And user clicks the Create Deep Link btn
    Then the user should get a short or long brandcycle link
    When user clicks on Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

    Examples:
      | url                |
      | nordstromrack_url  |
      | nordstromrack_cat  |
      | nordstromrack_prod |
      | qvc_url            |
      | qvc_cat            |
      | qvc_prod           |
      | wayfair_url        |
      | wayfair_cat        |
      | wayfair_prod       |


  @inactive_brand_top5
  Scenario: User fails to build a link with inactive brand url
    Given user logs in as a "user"
    When user enters "inactive_brand_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg
    Then user should not see the brand in BrandPage

  @blacklisted_top5
  Scenario: Blacklisted user fails to build a link
    Given user logs in as a "user"
    When user enters "blacklisted_brand_url" into Destination URL input for a brand they are blacklisted for
    And user clicks the Create Deep Link btn
    Then user should see "This brand is private and requires special approval." msg
    Then user should not see the brand in BrandPage

  @private_brand_whitelisted_top5
  Scenario: Whitelisted users successfully build a Private brand link
    Given user logs in as a "user"
    When user enters supported brand "whitelisted_private_brand_url" into Destination URL input
    And user clicks on Create Short URL button to get long url
    And user clicks the Create Deep Link btn
    Then the user should get a short or long brandcycle link
    When user clicks on Copy Link btn
    And opens the link
    Then the user should see the brand page that was used as Destination url.

  @private_brand_not_whitelisted_top5
  Scenario: User, who is NOT whitelisted, fails to build a Private brand link
    Given user logs in as a "user"
    When user enters "private_brand_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is private and requires special approval." msg
    Then user should not see the brand in BrandPage

  @Deeplink_Disabled_top5
  Scenario: User fails to build a brand link with a supported brand that's not Deeplink enabled.
    Given user logs in as a "user"
    When user enters "inner_no_deeplink_brand_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "The brand has not authorized deep links for this domain." msg

  @empty_link_build_top5
  Scenario: User enters no url into Destination URL
    Given user logs in as a "user"
    When user clicks the Create Deep Link btn
    Then user should see the "Destination URL can not be empty" error message

  @incomplete_url_no_dot_com_top5
  Scenario: User enters url without .com or .net
    Given user logs in as a "user"
    When user enters "no_dot_com_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg

  @not_supported_url_top5
  Scenario: User tries to build a link for not supported brand
    Given user logs in as a "user"
    When user enters "not_supported_url" into Destination URL input
    And user clicks the Create Deep Link btn
    Then user should see "This brand is not currently available on BrandCycle" msg


  @build_link_homepage_successful_api_top5
  Scenario Outline: Build a link on HomePage
    When user sends supported brand "<url>" to build link api with valid credentials and access token
    Then user gets status code "200", "url" and "url_long" url brandcycle links
    When user send get request to BC link
    Then the user should see Brand url in final response

    Examples:
      | url              |
      | qvc_url          |
      | qvc_cat          |
      | qvc_prod         |
      | michaelkors_url  |
      | michaelkors_cat  |
      | michaelkors_prod |
      | hsn_url          |
      | hsn_cat          |
      | hsn_prod         |

  @inactive_brand_api_top5
  Scenario: User fails to build a link with inactive brand url
    When user sends "inactive_brand_url" to build link api with valid credentials and access token
    Then user should get status code "410" and "THIS BRAND IS NOT CURRENTLY AVAILABLE ON BRANDCYCLE" msg

  @blacklisted_api_top5
  Scenario: Blacklisted user fails to build a link
    When user sends blacklisted "blacklisted_brand_url" to build link api with valid credentials and access token
    Then user should get status code "403" and "PRIVATE BRAND" msg

  @private_brand_whitelisted_api_top5
  Scenario: Whitelisted users successfully build a Private brand link
    When user sends supported brand "whitelisted_private_brand_url" to build link api with valid credentials and access token
    Then user gets status code "200", "url" and "url_long" url brandcycle links
    When user send get request to BC link
    Then the user should see Brand url in final response

  @private_brand_not_whitelisted_api_top5
  Scenario: User, who is NOT whitelisted, fails to build a Private brand link
    When user sends "private_brand_url" to build link api with valid credentials and access token
    Then user should get status code "403" and "This Brand is private and requires special approval" msg

  @Deeplink_Disabled_api_top5
  Scenario: User fails to build a brand link with a supported brand that's not Deeplink enabled.
    When user sends "inner_no_deeplink_brand_url" to build link api with valid credentials and access token
    Then user should get status code "406" and "UNFORTUNATELY, THIS BRAND CURRENTLY DOES NOT SUPPORT DEEP LINKING" msg

  @empty_link_build_api_top5
  Scenario: User enters no url into Destination URL
    When user sends "no url" to build link api with valid credentials and access token
    Then user should get status code "400" and "Destination url invalid." msg

  @incomplete_url_no_dot_com_api_top5
  Scenario: User enters url without .com or .net
    When user sends "no_dot_com_url" to build link api with valid credentials and access token
    Then user should get status code "410" and "THIS BRAND IS NOT CURRENTLY AVAILABLE ON BRANDCYCLE" msg

  @not_supported_url_api_top5
  Scenario: User tries to build a link for not supported brand
    When user sends "not_supported_url" to build link api with valid credentials and access token
    Then user should get status code "410" and "THIS BRAND IS NOT CURRENTLY AVAILABLE ON BRANDCYCLE" msg

