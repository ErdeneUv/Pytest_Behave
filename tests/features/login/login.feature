@login @ui @smoke @regression
Feature: Login
  As a user,
  I want to apply, login into Portal.


  Background: User is on the Login Page
    Given user is on Login Page

  @successful
  Scenario Outline: Successful login
    When "<user>" enter correct credentials
    Then user logged in successfully and redirected to Main Page

    Examples:
      | user    |
      | user    |


  @unsuccessful
  Scenario Outline: Unsuccessful login
    When user enter incorrect "<username/email>" and "<password>"
    Then user gets error message
    Examples:
      | username/email | password             |
      | test_username  | test_password        |
      | test_email     | test02_email_without |



