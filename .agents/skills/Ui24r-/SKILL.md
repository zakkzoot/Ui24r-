```markdown
# Ui24r- Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches best practices and conventions for developing in the Ui24r- Python codebase. It covers file organization, import/export styles, commit message patterns, and testing conventions. The repository does not use a specific framework, emphasizing lightweight, modular Python development.

## Coding Conventions

### File Naming
- Use **snake_case** for all file and module names.
  - **Example:**  
    ```python
    # Good
    user_profile.py

    # Bad
    UserProfile.py
    userProfile.py
    ```

### Import Style
- Prefer **relative imports** within the package.
  - **Example:**  
    ```python
    from .utils import helper_function
    ```

### Export Style
- Use **named exports** by explicitly listing public objects in `__all__`.
  - **Example:**  
    ```python
    __all__ = ['MyClass', 'my_function']
    ```

### Commit Messages
- No strict prefixing; freeform style.
- Average length: ~61 characters.
  - **Example:**  
    ```
    Fix bug in data processing for edge cases
    Add support for new user roles
    ```

## Workflows

### Adding a New Module
**Trigger:** When you need to add a new feature or utility.
**Command:** `/add-module`

1. Create a new Python file using snake_case naming.
2. Implement your feature or utility.
3. Use relative imports for any internal dependencies.
4. Add public classes/functions to `__all__` if needed.
5. Write corresponding test files (see Testing Patterns).

### Updating an Existing Module
**Trigger:** When modifying or refactoring existing code.
**Command:** `/update-module`

1. Locate the target module (ensure snake_case naming).
2. Make your changes, maintaining relative imports.
3. Update `__all__` if public API changes.
4. Update or add tests as appropriate.

### Writing Tests
**Trigger:** When adding or updating features.
**Command:** `/write-test`

1. Create a test file matching the pattern `*.test.*` (e.g., `user_profile.test.py`).
2. Write test functions for each public function/class.
3. Use the preferred (unspecified) testing framework.
4. Run tests to ensure correctness.

## Testing Patterns

- **File Pattern:** Test files are named with `*.test.*` (e.g., `module.test.py`).
- **Framework:** Not explicitly specified; use your preferred Python testing framework (e.g., `pytest` or `unittest`).
- **Example:**
  ```python
  # user_profile.test.py

  def test_user_creation():
      user = create_user('Alice')
      assert user.name == 'Alice'
  ```

## Commands
| Command         | Purpose                                      |
|-----------------|----------------------------------------------|
| /add-module     | Scaffold and implement a new module          |
| /update-module  | Update or refactor an existing module        |
| /write-test     | Create or update tests for a module/feature  |
```
