Feature: List cards

  Scenario: Specify invalid bearer token
      Given I try to list cards with invalid bearer token
       Then I will get "403" http error

  Scenario: Specify invalid or not my user ID
      Given I try to list cards with invalid or not my user ID
       Then I will get "404" http error

  Scenario: Really trying to list cards
      Given I send correct data to list cards
       Then I will get Ok http status and array of cards