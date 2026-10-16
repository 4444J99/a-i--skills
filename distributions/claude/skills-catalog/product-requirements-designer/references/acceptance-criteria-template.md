# Acceptance Criteria Templates

## Formats

### Gherkin (Given-When-Then)

Best for: Behavior-driven scenarios, automated testing

```gherkin
Feature: [Feature name]

  Scenario: [Scenario name]
    Given [precondition/context]
    And [additional precondition]
    When [action/trigger]
    And [additional action]
    Then [expected outcome]
    And [additional outcome]
    But [exception/negative outcome]
```

### Checklist Format

Best for: Simple criteria, quick verification

```markdown
**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
```

### Rule-Based Format

Best for: Business rules, validation logic

```markdown
**Rules:**
1. [Rule statement]
   - Condition: [When this is true]
   - Result: [This happens]
   
2. [Rule statement]
   - Condition: [When this is true]
   - Result: [This happens]
```

---

## Gherkin Examples

### Basic Scenario
```gherkin
Scenario: Successful login with valid credentials
  Given the user is on the login page
  And the user has a valid account
  When the user enters valid email and password
  And clicks the login button
  Then the user is redirected to the dashboard
  And sees a welcome message with their name
```

### Scenario Outline (Data-Driven)
```gherkin
Scenario Outline: Password validation
  Given the user is on the registration page
  When the user enters password "<password>"
  Then the system shows "<message>"
  And the submit button is "<button_state>"

  Examples:
    | password     | message                      | button_state |
    | abc          | Password too short           | disabled     |
    | password123  | Password needs special char  | disabled     |
    | Password1!   | Password accepted            | enabled      |
```

### Background (Shared Setup)
```gherkin
Background:
  Given the user is logged in
  And has admin permissions

Scenario: Admin can view user list
  When the admin navigates to user management
  Then the admin sees a list of all users

Scenario: Admin can edit user
  When the admin clicks edit on a user
  Then the admin sees the user edit form
```

---

## Criteria Categories

### Functional Criteria
What the feature must do.

```gherkin
Scenario: Filter products by category
  Given I am on the product listing page
  When I select "Electronics" from the category filter
  Then I see only products in the Electronics category
  And the product count updates to show filtered results
```

### Non-Functional Criteria

**Performance**
```gherkin
Scenario: Search response time
  Given I am on the search page
  When I search for "laptop"
  Then results display within 2 seconds
  And the page remains responsive during loading
```

**Accessibility**
```gherkin
Scenario: Screen reader compatibility
  Given I am using a screen reader
  When I navigate to the checkout page
  Then all form fields have proper labels
  And error messages are announced
  And I can complete checkout using only keyboard
```

**Security**
```gherkin
Scenario: Session timeout
  Given I am logged in
  When I am inactive for 30 minutes
  Then I am automatically logged out
  And redirected to login page with message
  And my session token is invalidated
```

### Edge Cases
```gherkin
Scenario: Empty search results
  Given I am on the search page
  When I search for "xyznonexistent123"
  Then I see a "No results found" message
  And I see suggested alternative searches
  And the search box retains my query

Scenario: Network failure during save
  Given I am editing a document
  And I have unsaved changes
  When the network connection is lost
  And I click save
  Then I see an offline indicator
  And my changes are saved locally
  And changes sync when connection restores
```

### Error Handling
```gherkin
Scenario: Invalid file upload
  Given I am on the file upload page
  When I select a file larger than 10MB
  Then the upload is rejected
  And I see error "File exceeds 10MB limit"
  And the file input is cleared
  And I can select a different file
```

---

## Acceptance Criteria Quality Checklist

### Each Criterion Should Be:

- [ ] **Testable**: Can definitively pass or fail
- [ ] **Clear**: Unambiguous language, no interpretation needed
- [ ] **Concise**: One behavior per criterion
- [ ] **Independent**: Doesn't depend on other criteria's order
- [ ] **User-focused**: Written from user's perspective (for functional)

### Common Mistakes to Avoid:

❌ **Too vague**
```
The page should load quickly.
```

✅ **Specific and measurable**
```
The page fully loads within 3 seconds on 3G connection.
```

❌ **Implementation details**
```
The system uses Redis to cache the results.
```

✅ **Behavior focused**
```
Repeated searches for the same term return instantly.
```

❌ **Multiple behaviors**
```
User can login, see their dashboard, and edit their profile.
```

✅ **Single behavior**
```
User can login with valid credentials.
User sees personalized dashboard after login.
User can edit their profile from dashboard.
```

---

## Acceptance Criteria Patterns

### CRUD Operations
```gherkin
# Create
Scenario: Create new item
  Given I am on the items page
  When I click "Add New"
  And fill in required fields
  And click "Save"
  Then the new item appears in the list
  And I see success confirmation

# Read
Scenario: View item details
  Given items exist in the system
  When I click on an item
  Then I see all item details
  And I see edit and delete options

# Update
Scenario: Edit existing item
  Given I am viewing an item
  When I click "Edit"
  And modify the name
  And click "Save"
  Then the item shows updated name
  And I see success confirmation

# Delete
Scenario: Delete item
  Given I am viewing an item
  When I click "Delete"
  Then I see confirmation dialog
  When I confirm deletion
  Then the item is removed from list
  And I see success confirmation
```

### Authentication
```gherkin
Scenario: Login required for protected pages
  Given I am not logged in
  When I try to access the dashboard
  Then I am redirected to login
  And see message "Please log in to continue"
  And after login I am sent to dashboard
```

### Form Validation
```gherkin
Scenario: Required field validation
  Given I am on the registration form
  When I leave the email field empty
  And click submit
  Then the form is not submitted
  And I see "Email is required" error
  And the email field is highlighted
  And focus moves to email field
```

### Pagination
```gherkin
Scenario: Paginated results
  Given there are 50 items
  And page size is 10
  When I view the first page
  Then I see items 1-10
  And pagination shows "Page 1 of 5"
  And "Previous" is disabled
  And "Next" is enabled
```

---

## Template: Full AC Document

```markdown
# Acceptance Criteria: [Story Title]

## Story
As a [user], I want to [action] so that [benefit].

## Functional Criteria

### Happy Path
```gherkin
Scenario: [Main success scenario]
  Given [context]
  When [action]
  Then [outcome]
```

### Alternative Paths
```gherkin
Scenario: [Alternative scenario]
  Given [context]
  When [different action]
  Then [different outcome]
```

## Edge Cases
```gherkin
Scenario: [Edge case]
  Given [unusual context]
  When [action]
  Then [handled gracefully]
```

## Error Handling
```gherkin
Scenario: [Error scenario]
  Given [error condition]
  When [action]
  Then [appropriate error handling]
```

## Non-Functional Criteria

### Performance
- [ ] [Performance criterion]

### Accessibility
- [ ] [Accessibility criterion]

### Security
- [ ] [Security criterion]

## Out of Scope
- [Explicitly not covered]

## Open Questions
- [Any unresolved questions]
```
