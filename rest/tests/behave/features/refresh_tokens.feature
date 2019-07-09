Feature: Refresh tokens

  Scenario: Execute some request with "refresh" token
      Given I try to execute some request with "refresh" token
       Then I will get "403" http error

  Scenario: Execute "/refresh-tokens" with "auth" token
      Given I try to execute "/refresh-tokens" with "auth" token
       Then I will get "403" http error

  Scenario: Execute "/refresh-tokens" with "refresh" token
      Given I try to execute "/refresh-tokens" with "refresh" token
       Then I will get Ok http status
