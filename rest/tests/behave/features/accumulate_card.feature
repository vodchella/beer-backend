Feature: Accumulate card

  Scenario: Specify invalid bearer token
      Given I try to accumulate card with invalid bearer token
       Then I will get "403" http error

  Scenario: Specify invalid card ID
      Given I try to accumulate card with invalid card ID
       Then I will get "404" http error