Feature: User password management

  Scenario: Trying to send invalid JSON
      Given I send invalid JSON
       Then I will get "500" http error and "-32003" application error

  Scenario: Trying to specify incorrect user ID
      Given I send incorrect user ID
       Then I will get "404" http error

  Scenario: Trying to change password with invalid request data
      Given I send incorrect data to change password
       Then I will get "400" http error

  Scenario: Trying to change password with incorrect old one
      Given I send incorrect old password
       Then I will get "500" http error and "-32004" application error

  Scenario: Really trying to change password
      Given I send correct password data
       Then I will get Ok http status and "ok" result
