Feature: Accumulate card

  Scenario: Specify invalid bearer token
      Given I try to accumulate card with invalid bearer token
       Then I will get "403" http error

  Scenario: Specify invalid card ID
      Given I try to accumulate card with invalid card ID
       Then I will get "404" http error

  Scenario: Really trying to accumulate card
      Given I send correct data to accumulate card
       Then I will get Ok http status and modified card value

  Scenario: Trying to fulfill card
      Given I send data to fulfill card
       Then I will get Ok http status and disabled card with info message