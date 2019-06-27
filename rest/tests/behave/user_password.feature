Feature: User password management

  Scenario: Trying to specify incorrect user ID
      Given I send incorrect user ID
       Then I will get "404" http-error code

  Scenario: Trying to change password with invalid request data
      Given I send incorrect data to change password
       Then I will get "400" http-error code
