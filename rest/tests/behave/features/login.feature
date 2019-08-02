Feature: Login

  Scenario: Send invalid JSON when trying to login
      Given I try to login with invalid JSON
       Then I will get "500" http error with "-32003" application error

  Scenario: Specify incorrect user ID when login
      Given I try to login with incorrect user ID
       Then I will get "404" http error or "500" http error with "-32005" app error

  Scenario: Specify incorrect password when login
      Given I try to login with incorrect password
       Then I will get "500" http error with "-32005" application error

  Scenario: Really trying to login
      Given I send correct login data
       Then I will get Ok http status and tokens
