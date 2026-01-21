@snapshot_report @report @smoke @regression
Feature: Snapshot Report feature on HomePage
  As a user, I want to check reports such as Clicks, Orders, Sales and Commissions for Nov/1/2024 to Nov/30/2024 on Home Page

  @snapshot_report_api
  Scenario: User successfully get response of reports for month of November on HomePage
    When User sends a Post request to "REPORTS_ENDPOINT" to get snapshots of November as a "USER"
    Then User should get status code "200"
    Then User should be able to see some data in totals


  @snapshot_report_ui
  Scenario Outline: User successfully checks reports for month of November on HomePage
    Given User logs in as a "user"
    When User clicks on TimeFrame dropdown menu and selects 'Between Dates'
    When User selects 07/01/2025 on Start Date input
    When User selects 08/01/2025 on End Date input
    When User clicks Run btn
    Then User should be able to see following results of: "<Clicks>", "<Orders>", "<Sales>", and "<Commissions>"

    Examples:
      | Clicks | Orders | Sales | Commissions |
      | 4,816  | 1      | $61   | $1.82       |
