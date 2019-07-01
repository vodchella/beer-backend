Feature: Login

  Scenario: Send invalid JSON when login
      Given I try to login with invalid JSON
       Then I will get "500" http error and "-32003" application error

  Scenario: Specify incorrect user ID when login
      Given I try to login with incorrect user ID
       Then I will get "404" http error or "500" http error with "-32005" app error
