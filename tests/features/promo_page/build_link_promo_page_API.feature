@build_link_promo_page @smoke @promo_page @promo_page_api @regression
Feature: “Build A Link” forms API on Special Promotions page
  As a user, I want to build a link on Promotions page using API and follow the link to the destination page


  @promo_page_success_api @api
  Scenario: User sends request to /special_promotions/list with Keywords and Brand and gets list of promos
    When user sends a request to portal with payloads of keywords : "20% Off 100s of Wines", brandTitle : "Wine Access"
    Then user will receive a status code "200" and response with dealID of "Wine Access"
    When user sends a request to get promo link
    Then user will receive status code "200" and promo link
    When user send get request to BC link
    Then the user should see Brand url in final response

  @promo_page_success_api @api
  Scenario: User sends request to /special_promotions/list with Brand and sorted by End Date and Oldest. Then User gets list of promos
    When user sends a request to portal with payloads of brandTitle : "Bowflex", sortBy : "end", orderBy : "old"
    Then user will receive a status code "200", response with dealID of "Bowflex", description of "Shop Bowflex and save 15% plus Free Shipping on orders $400+ when you use code SAVE15 at checkout."
    When user sends a request to get promo link
    Then user will receive status code "200" and promo link
    When user send get request to BC link
    Then the user should see Brand url in final response