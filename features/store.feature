Feature: Store management in user profile

  Scenario: A user logs in, creates a store, adds/removes another user, and deletes the store
    Given a user named "testuser" with password "testpass"
    And a user named "root" with password "root"
    When "testuser" logs in
    And they create a store named "TestBehave"
    Then the store "TestBehave" should exist
    And "testuser" should have own_store=True

    When "testuser" adds user "root" to the store "TestBehave"
    Then "root" should be a member of "TestBehave"
    And "root" should have own_store=True

    When "testuser" removes user "root" from the store "TestBehave"
    Then "root" should not be a member of "TestBehave"
    And "root" should have own_store=False

    When "testuser" deletes the store "TestBehave"
    Then the store "TestBehave" should no longer exist
    And "testuser" should have own_store=False

