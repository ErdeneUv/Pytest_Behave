@link_performance @link_performance_ui @report @ui @smoke @regression
Feature: Link Performance report
  As a user, I want to see performances of link I created in given time frame

  @lpr_brand_filter_sort_sales
  Scenario: LPR Brand filter, calendar, sorting by Sales
    Given user logs in as a "user"
    Given user navigates to the "link-performance report" page
    When user enters "07/01/2025" for star date and "09/01/2025" for end date
    When user filters for "Instacart"
    When user sort by Sales
    Then user will see "$60.50", "5", "1" matching
    When user clicks on "Clicks" header to sort by it
    Then user will see "5" on first row's clicks
    When user clicks on "Payout" header to sort by it
    Then user will see "$1.81" on first row's payout


  @lpr_date_preset_sort_click
  Scenario: LPR Date Preset, sorting by Clicks, Payout, Orders
    Given user logs in as a "user"
    Given user navigates to the "link-performance report" page
    When user clicks on "3M" date preset
    Then user should see date for today in end date and 3 months back in start date
    When user clicks on "1M" date preset
    Then user should see date for today in end date and 1 month back in start date
    Then user should see less number of links and pages


    @lpr_user_filter
    Scenario: LPR User filter
      Given user logs in as a "fash"
      Given user navigates to the "link-performance report" page
      When user enters "07/1/2025" for star date and "09/01/2025" for end date
      When user clicks on User Filter and choose "FashionorLove_AddUser", "BC_API", and "FashionorLove_BC_API002
      Then user would see "13" links and total of "2" pages
      When user clicks on clear filters
      Then user would see more than "13" links