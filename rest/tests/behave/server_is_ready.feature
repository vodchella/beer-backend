Feature: REST-server is ready?

  Scenario: Get software version string
      Given I send GET-request to http://localhost:8517/
       Then I will see full software version
