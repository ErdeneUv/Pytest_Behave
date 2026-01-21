@build_link_homepage_api @build_a_link @api @smoke @regression
Feature: Build A Link API. This API is in Homepage, Bookmarklet, iOS app, /build-a-link, /merchant/merchant/[id]
  As a user, I want to build a link by sending request to deep linking API

  @build_link_homepage_successful_api
  Scenario Outline: Build a link on HomePage API
    When user sends supported brand "<url>" to build link api with valid credentials and access token
    Then user gets status code "200", "url" and "url_long" url brandcycle links
    When user send get request to BC link
    Then the user should see Brand url in final response

    Examples:
      | url                       |
      | amazon_url                |
      | walmart_url               |
      | walmart_cat               |
      | walmart_prod              |
      | lululemon_url             |
      | lululemon_cat             |
      | lululemon_prod            |
      | target_url                |
      | target_cat                |
      | target_prod               |
      | underarm_url              |
      | underarm_cat              |
      | underarm_prod             |
      | samsclub_url              |
      | samsclub_cat              |
      | samsclub_prod             |
      | michaelkors_url           |
      | michaelkors_cat           |
      | michaelkors_prod          |
      | qvc_url                   |
      | qvc_cat                   |
      | qvc_prod                  |
      | macys_url                 |
      | macys_cat                 |
      | macys_prod                |
      | ruelala_url               |
      | ruelala_cat               |
      | ruelala_prod              |
      | nordstrom_url             |
      | nordstrom_cat             |
      | nordstrom_prod            |
      | kohls_url                 |
      | kohls_cat                 |
      | kohls_prod                |
      | woot_url                  |
      | woot_cat                  |
      | woot_prod                 |
      | giltcity_url              |
      | giltcity_cat              |
      | giltcity_prod             |
      | coachoutlet_url           |
      | coachoutlet_cat           |
      | coachoutlet_prod          |
      | jcpenney_url              |
      | jcpenney_cat              |
      | jcpenney_prod             |
      | jcpenney_prod             |
      | hsn_url                   |
      | hsn_cat                   |
      | hsn_prod                  |
      | oldnavy_url                |
      | oldnavy_cat                |
      | oldnavy_prod               |
      | bestbuy_url               |
      | bestbuy_cat               |
      | bestbuy_prod              |

  @inactive_brand_api
  Scenario: User fails to build a link with inactive brand url
    When user sends "inactive_brand_url" to build link api with valid credentials and access token
    Then user should get status code "410" and "THIS BRAND IS NOT CURRENTLY AVAILABLE ON BRANDCYCLE" msg

  @blacklisted_api
  Scenario: Blacklisted user fails to build a link
    When user sends blacklisted "blacklisted_brand_url" to build link api with valid credentials and access token
    Then user should get status code "403" and "PRIVATE BRAND" msg

  @private_brand_whitelisted_api
  Scenario: Whitelisted users successfully build a Private brand link
    When user sends supported brand "whitelisted_private_brand_url" to build link api with valid credentials and access token
    Then user gets status code "200", "url" and "url_long" url brandcycle links
    When user send get request to BC link
    Then the user should see Brand url in final response

  @private_brand_not_whitelisted_api
  Scenario: User, who is NOT whitelisted, fails to build a Private brand link
    When user sends "private_brand_url" to build link api with valid credentials and access token
    Then user should get status code "403" and "This Brand is private and requires special approval" msg

  @Deeplink_Disabled_api
  Scenario: User fails to build a link out of a brand that's not Deeplink enabled.
    When user sends "inner_no_deeplink_brand_url" to build link api with valid credentials and access token
    Then user should get status code "406" and "UNFORTUNATELY, THIS BRAND CURRENTLY DOES NOT SUPPORT DEEP LINKING" msg

  @empty_link_build_api
  Scenario: User enters no url into Destination URL
    When user sends request without urls to build link api with valid credentials and access token
    Then user should get status code "400" and "Destination url invalid." msg

  @incomplete_url_no_dot_com_api
  Scenario: User enters url without .com or .net
    When user sends "no_dot_com_url" to build link api with valid credentials and access token
    Then user should get status code "410" and "THIS BRAND IS NOT CURRENTLY AVAILABLE ON BRANDCYCLE" msg

  @not_supported_url_api
  Scenario: User tries to build a link for not supported brand
    When user sends "not_supported_url" to build link api with valid credentials and access token
    Then user should get status code "410" and "THIS BRAND IS NOT CURRENTLY AVAILABLE ON BRANDCYCLE" msg

