# This feature exercises the full life‑cycle of a collection and its items
# It includes a smoke scenario for basic create/delete functionality and a regression
# scenario that covers creation, update, retrieval and deletion of both
# collections and collection items.
@collection_api @api
Feature: Collection API (Collections + Collection Items)
  As an API client
  I want to create, update, retrieve and delete collections and their items
  So that I can verify the functionality of the BrandCycle collections API

  @smoke @api
  Scenario: Smoke test – create and delete a collection
    Given a valid user with id "12855"
    When the user creates a collection with name "API Smoke Test Collection", description "Smoke test for collection creation" and default image url "https://media.kohlsimg.com/is/image/kohls/7787448?wid=805&hei=805"
    Then the response status code should be "201"
    And save the collection id
    And the collection name should be "API Smoke Test Collection" and description should be "Smoke test for collection creation"
    When the user deletes the collection
    Then the response status code should be "204"
    When the user attempts to retrieve the collection
    Then the response status code should be "404"

  # Regression scenario exercises the complete life‑cycle: create a
  # collection, add an item, update both the item and the collection,
  # retrieve them at multiple levels, and finally delete them.  This
  # provides thorough coverage of the back‑end endpoints.
  @regression @api
  Scenario: Regression test – full collection lifecycle
    Given a valid user with id "12855"
    When the user creates a collection with name "API Test Collection", description "Testing for status_01" and default image url "https://media.kohlsimg.com/is/image/kohls/7787448?wid=805&hei=805&op_sharpen=1"
    Then the response status code should be "201"
    And save the collection id
    And the collection name should be "API Test Collection" and description should be "Testing for status_01"
    When the user creates a collection item with name "Loomaknoti Home Sweet Home Throw Rug", original url "https://www.kohls.com/product/prd-7787448/loomaknoti-home-sweet-home-throw-rug.jsp?pfm=bdrecs-WebStore-PDP-Horizontal1-b1156-400%7C406&bdrecsId=132814e6-0dfc-4c12-a348-fff2c7528ec5", shopping url "https://link.brandcycle.com/8od45r", store "Kohl's", image url "https://media.kohlsimg.com/is/image/kohls/54611128_CC_ALT2?wid=390&hei=390&op_sharpen=1"
    Then the response status code should be "201"
    And save the collection item id
    And the collection item name should be "Loomaknoti Home Sweet Home Throw Rug" and original url should be "https://www.kohls.com/product/prd-7787448/loomaknoti-home-sweet-home-throw-rug.jsp?pfm=bdrecs-WebStore-PDP-Horizontal1-b1156-400%7C406&bdrecsId=132814e6-0dfc-4c12-a348-fff2c7528ec5"
    When the user updates the collection item with name "Apple Watch Series 10 (!!UPDATED One More Testing)", original url "https://www.bestbuy.com/site/apple-watch-series-10-gps-46mm-aluminum-case-with-black-sport-band-m-l-jet-black-2024/6572689.p?skuId=6572689", shopping url "https://link.brandcycle.com/8od45r", store "Kohl's", image url "https://media.kohlsimg.com/is/image/kohls/54611128_CC_ALT2?wid=390&hei=390&op_sharpen=1"
    Then the response status code should be "200"
    And the collection item name should be "Apple Watch Series 10 (!!UPDATED One More Testing)" and original url should be "https://www.bestbuy.com/site/apple-watch-series-10-gps-46mm-aluminum-case-with-black-sport-band-m-l-jet-black-2024/6572689.p?skuId=6572689"
    When the user updates the collection to description "MORE DESCRIPTIONS GOT UPDATED!!! This is for testing purpose only, please discard" and status "published"
    Then the response status code should be "200"
    And the collection description should be "MORE DESCRIPTIONS GOT UPDATED!!! This is for testing purpose only, please discard" and status should be "published"
    When the user retrieves collections for the user
    Then the response status code should be "200"
    And the collection id should be present in the response
    And the collection name should be "API Test Collection" and description should be "MORE DESCRIPTIONS GOT UPDATED!!! This is for testing purpose only, please discard"
    When the user retrieves items for the collection
    Then the response status code should be "200"
    And the collection item id should be present in the response
    And the collection item name should be "Apple Watch Series 10 (!!UPDATED One More Testing)" and original url should be "https://www.bestbuy.com/site/apple-watch-series-10-gps-46mm-aluminum-case-with-black-sport-band-m-l-jet-black-2024/6572689.p?skuId=6572689"
    When the user retrieves the collection item
    Then the response status code should be "200"
    And the collection item id should match saved id and name should be "Apple Watch Series 10 (!!UPDATED One More Testing)" and original url should be "https://www.bestbuy.com/site/apple-watch-series-10-gps-46mm-aluminum-case-with-black-sport-band-m-l-jet-black-2024/6572689.p?skuId=6572689"
    When the user deletes the collection item
    Then the response status code should be "204"
    When the user attempts to retrieve the collection item
    Then the response status code should be "404"
    When the user deletes the collection
    Then the response status code should be "204"
    When the user attempts to retrieve the collection
    Then the response status code should be "404"