Feature: Create card

  Scenario: Specify invalid bearer token
      Given I try to create card with invalid bearer token
       Then I will get "403" http error

  Scenario: Specify invalid JSON body
      Given I try to create card with invalid JSON body
       Then I will get "500" http error with "-32003" application error

  Scenario: Specify invalid owner ID
      Given I try to create card with invalid owner ID
       Then I will get "400" http error

  Scenario: Specify empty name
      Given I try to create card with empty name
       Then I will get "400" http error

  Scenario: Really trying to create card
      Given I send correct card data
       Then I will get Ok http status and new card in result