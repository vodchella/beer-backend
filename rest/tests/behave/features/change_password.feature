Feature: Change password

  Scenario: Send invalid JSON when trying to change password
      Given I try to change password with invalid JSON
       Then I will get "500" http error with "-32003" application error

  Scenario: Specify incorrect user ID when trying to change password
      Given I try to change password with incorrect user ID
       Then I will get "404" http error

  Scenario: Trying to change password with invalid request data
      Given I send incorrect data to change password
       Then I will get "400" http error

  Scenario: Trying to change password with incorrect old one
      Given I send incorrect old password
       Then I will get "500" http error with "-32004" application error

  Scenario: Really trying to change password
      Given I send correct password data
       Then I will get Ok http status and "ok" result
