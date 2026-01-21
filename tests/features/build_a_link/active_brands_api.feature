@active_brands_api
Feature: We want to see if any of BrandCycle active brands links are working.
  If not it might be due to brands is not active in the network
  We also wants to add newly created brands to the list of active brands

  @active_brands
  Scenario: Verify Active brands' links are working
    When user gets list of current and new active brands
    Then user will check if there would be any new brands to add to it and delete from it
    When user gets BC links for all active brands homepage
    And user will check BC links are working, if not user will report it