# Contributing to AutoML

Thank you for your interest in contributing to AutoML! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback

## Getting Started

### Development Setup

1. **Fork and clone the repository**

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions focused (single responsibility)

### Code Formatting

Use Black for formatting:
```bash
black app/
```

### Linting

Run flake8 before committing:
```bash
flake8 app/
```

### Type Checking

Use mypy for type checking:
```bash
mypy app/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_cleaning.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Test edge cases and error conditions

Example:
```python
def test_fill_null_with_mean():
    """Test filling null values with mean."""
    df = pd.DataFrame({'col': [1, 2, None, 4]})
    # Test implementation
    assert df['col'].isnull().sum() == 0
```

## Project Structure

```
app/
├── config.py          # Configuration settings
├── main.py            # Application entry point
├── cleaning/          # Data cleaning modules
├── training/          # Model training modules
└── utils/             # Utility functions
```

### Adding New Features

1. **Cleaning Feature**: Add to `app/cleaning/`
2. **Training Feature**: Add to `app/training/`
3. **Utility Function**: Add to `app/utils/`

### Module Template

```python
"""
Module Description
"""
import streamlit as st


def render_page():
    """Render the page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
    st.header("Page Title")
    
    # Your implementation
```

## Pull Request Process

1. **Update your branch**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run tests and linting**:
   ```bash
   pytest
   black app/
   flake8 app/
   mypy app/
   ```

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   ```

   Use conventional commits:
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation
   - `style`: Formatting
   - `refactor`: Code restructuring
   - `test`: Adding tests
   - `chore`: Maintenance

4. **Push and create PR**:
   ```bash
   git push origin your-branch
   ```
   Then create a Pull Request on GitHub

5. **PR Requirements**:
   - Clear description of changes
   - All tests passing
   - Code formatted with Black
   - No linting errors
   - Documentation updated (if needed)

## Documentation

- Update README.md for feature changes
- Update docs/user_guide.md for user-facing changes
- Add docstrings to new functions
- Comment complex logic

## Questions?

- Open an issue for bugs
- Start a discussion for feature ideas
- Ask questions in PR comments

---

**Thank you for contributing! 🎉**
