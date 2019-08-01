Feature: View card

  Scenario: Specify invalid bearer token
      Given I try to view card with invalid bearer token
       Then I will get "403" http error

  Scenario: Specify invalid card ID
      Given I try to view card with invalid card ID
       Then I will get "404" http error

  Scenario: Really trying to view card
      Given I send correct data to view card
       Then I will get Ok http status and valid card in result