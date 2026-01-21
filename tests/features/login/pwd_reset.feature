@pwd_reset @ui @smoke @regression
Feature: Password Reset
  As a user, I want to reset my password

  Background: User is on password reset page
    Given user clicks on Reset password here button
    And user lands on password reset page

  @reset_pwd
  Scenario Outline: Reset password
    When user enters "<username>" and clicks on send button
    Then user sees message

    Examples:
    |username|
    |test23@gmail.com|
    |test23          |

  @reset_pwd_back
  Scenario: Reset password to go back to login page
    When user clicks on Back to login button
    Then user sees login page