Feature: Accumulate card

  Scenario: Specify invalid bearer token
      Given I try to accumulate card with invalid bearer token
       Then I will get "403" http error

  Scenario: Specify invalid card ID
      Given I try to accumulate card with invalid card ID
       Then I will get "404" http error

  Scenario: Specify invalid JSON body
      Given I try to accumulate card with invalid JSON body
       Then I will get "500" http error with "-32003" application error

  Scenario: Really trying to accumulate card
      Given I send correct data to accumulate card
       Then I will get Ok http status and modified card value

  Scenario: Trying to fulfill card
      Given I send data to fulfill card
       Then I will get Ok http status and disabled card

  Scenario: Trying to accumulate disabled card
      Given I try to accumulate disabled card
       Then I will get "500" http error with "-33003" application error

  Scenario: Trying to accumulate over limit
      Given I try to accumulate over limit
       Then I will get "500" http error with "-33002" application error