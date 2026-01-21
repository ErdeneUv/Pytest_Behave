@login_api @backend @smoke @api @regression
Feature: Login API Functionality
  The purpose of this feature is to test the login functionality of the application, including token retrieval, login process, and logout functionality


  Background: User is on the Login Page
    Given I retrieve a valid CSRF token from "token_endpoint"

  @successful_api
  Scenario Outline: Successful login
    When User sends a POST request to "login_endpoint" with CSRF token, valid credentials of "<user>"
    Then User should receive a status code of 200
    And User should receive an access token and logout access
    And User successfully logs out using logout token
    Examples:
      | user |
      | USER |


  @unsuccessful_api_invalid_credentials
  Scenario Outline: Unsuccessful login, invalid credentials
    When User sends a POST request to "login_endpoint" with CSRF token, invalid credentials of "<username/email>" and "<password>"
    Then user gets status code "400" and "<error msg>"
    Examples:
      | username/email | password             | error msg                                 |
      | test_01        | test_password        | Sorry, unrecognized username or password. |
      | test_02        | test02_email_without | Sorry, unrecognized username or password. |

  @unsuccessful_api_with_missing_password_param
  Scenario Outline: Unsuccessful login, missing password
    When User sends a POST request to "login_endpoint" with CSRF token, with missing pwd of "<user>"
    Then user gets status code "400" and "<error msg>"
    Examples:
      | user | error msg                 |
      | USER | Missing credentials.pass. |

# the following scenarios asserts that status code would be 200 where it should be 403, it's because it's behavior for now. The tickit is issued
  @unsuccessful_api_invalid_token
  Scenario Outline: Unsuccessful login, invalid token
    When User sends a POST request to "login_endpoint" with INVALID CSRF token, VALID credentials of "<user>"
    Then User gets status code 200
    Examples:
      | user |
      | USER |


  @unsuccessful_api_logout_without_token
      #This will get 200 for now will be updated
  Scenario Outline: Logout attempt without providing a logout token
    Given "<User>" successfully logins with valid creds
    When "<User>" sends a GET request to "logout_endpoint" without the logout token
    Then User should receive a status code of 200
    Examples:
      | User |
      | USER |


  @unsuccessful_api_after_logout
    #This will get 200 for now
  Scenario Outline: Verify access token is invalid after logout
    Given "<User>" successfully logins with valid creds
    And User successfully logs out using logout token
    When User try to access another protected API using the previous access token
    Then User should receive status code 401 Unauthorized
    Examples:
      | User |
      | USER |