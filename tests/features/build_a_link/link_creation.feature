@link_creation
Feature: This feature files is for creating and storing BC links to external file



  Background: User is on home page
    Given User logs in as a "user"

  @link_creation
  Scenario Outline: Build a link on HomePage
    When user enters supported brand "<url>" into Destination URL input
    And user clicks on Create Short URL button to get long url
    And user clicks the Create Deep Link btn
    Then the user should get a short or long brandcycle link
    When user clicks on Copy Link btn
    #When user opens a new file and paste the created link and take a newline

    Examples:
      | url                       |
      | michaelkors_url           |
      | michaelkors_cat           |
      | michaelkors_prod          |
