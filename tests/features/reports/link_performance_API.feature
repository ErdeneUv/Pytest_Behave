@link_performance @link_performance_api @report @api @smoke @regression
Feature: Link Performance report API
  As a user, I want to get performances data of link I created in given time frame

  @lpr_brand_filter_sort_sales_api
  Scenario: LPR Brand filter, calendar, sorting by Sales API
    When user sends a request to "brands-engaged" for userID "12256"
    Then user receives a status code "200" and engaged brand's ids
    When user sends a request to "link-performance" as a "USER" for userID "12256", brandID "761", createdAfter "2025-06-08", createdBefore "2025-09-08", sort "dateCreated", direction "desc"
    Then user will get status code of "200"
    Then user will get sales: "60.5", payout: "1.815" clicks: "5", orders: "1", conversionRate: "20"

  @lpr_user_filter_api
  Scenario: LPR User filter API
    When user sends a request to "subusers" as a "FASH"
    Then user will receive status code "200" and subusers' uid
    When user sends a request to "brands-engaged" for userId "12255", "12782", "12781"
    When user sends a request to "link-performance" as a "FASH" for userID "12255,12782,12781", sort "dateCreated", direction "desc", periodStart "2025-07-01", periodEnd "2025-09-01"
    Then user will get status code of "200"
    Then user will get totalItems: "13", totalPages: "2" in meta of payload

