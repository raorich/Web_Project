Feature: Store error handling
  Scenario: Attempting to create a store with invalid data
    Given a user named "alice" with password "test1234"
    When "alice" logs in
    When they try to create a store with no name
    Then the response should contain "Missing store name."

  Scenario: Attempting to create a store that already exists
    Given a user named "bob" with password "test1234"
    When "bob" logs in
    When they create a store named "MyStore"
    When they try to create a store named "MyStore"
    Then the response should contain "Store already exists."

  Scenario: Trying to add a user that doesn't exist
    Given a user named "charlie" with password "test1234"
    When "charlie" logs in
    When they create a store named "TeamStore"
    When "charlie" tries to add non-existent user "ghostuser" to "TeamStore"
    Then the response should contain "User doesn't exist."

  Scenario: Trying to rename a store with an invalid name
    Given a user named "david" with password "test1234"
    When "david" logs in
    When they create a store named "RenameMe"
    When "david" tries to rename store "RenameMe" to "123"
    Then the response should contain "The new name is too short."
	
  Scenario: User tries to add themselves to a store they don't belong to
    Given a user named "owner" with password "123456"
    And a user named "intruder" with password "123456"
    When "owner" logs in
    And they create a store named "PrivateStore"
    When "intruder" logs in
    And "intruder" tries to add user "intruder" to the store "PrivateStore"
    Then the response should contain "This user don't own this store."

  Scenario: User tries to add themselves to a store
    Given a user named "selfadder" with password "123456"
    When "selfadder" logs in
    And they create a store named "SoloStore"
    When "selfadder" tries to add user "selfadder" to the store "SoloStore"
    Then the response should contain "This user already is in this store."
