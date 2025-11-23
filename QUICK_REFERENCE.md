# 🚀 AutoML Quick Reference

## Running the Application

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run the application
streamlit run app/main.py
```

## Project Structure

```
AutoML/
├── app/                    # Main application code
│   ├── main.py             # Entry point
│   ├── config.py           # Configuration
│   ├── cleaning/           # Data cleaning modules (8 files)
│   ├── training/           # Model training modules (3 files)
│   └── utils/              # Utilities (2 files)
├── data/                   # Data directory (gitignored)
├── models/                 # Saved models (gitignored)
├── tests/                  # Test files
├── docs/                   # Documentation
└── app_backup.py           # Original single-file version
```

## Module Organization

### Cleaning Modules (`app/cleaning/`)
- `upload.py` - Upload & explore datasets
- `nulls.py` - Handle null values
- `duplicates.py` - Remove duplicates
- `conversion.py` - Data type conversion
- `encoding.py` - Categorical encoding
- `filters.py` - Data filtering
- `columns.py` - Column management
- `download_page.py` - Download cleaned data

### Training Modules (`app/training/`)
- `trainer.py` - Model training logic
- `evaluator.py` - Model evaluation & testing
- `visualizations.py` - Performance charts

### Utilities (`app/utils/`)
- `session.py` - Session state management
- `download.py` - Download helpers

## Key Configuration (`app/config.py`)

```python
PAGE_TITLE = "ML Trainer"
DEFAULT_TEST_SIZE = 0.2
RANDOM_STATE = 42
PREVIEW_ROWS = 10
```

## Development Commands

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Format code
black app/

# Lint code
flake8 app/

# Type check
mypy app/

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## Common Tasks

### Adding a New Cleaning Operation

1. Create new file in `app/cleaning/`
2. Implement `render_*_page()` function
3. Import in `app/main.py`
4. Add to routing logic

### Adding a New Model

1. Edit `app/training/trainer.py`
2. Add model to appropriate models dictionary
3. Update results processing

### Modifying Configuration

- Edit `app/config.py`
- No need to change code in modules

## File Locations

- **Code**: `app/`
- **Data**: `data/` (create manually if saving datasets)
- **Models**: `models/` (create manually if saving models)
- **Docs**: `docs/`
- **Tests**: `tests/`

## What Was Changed

### Quick Fixes ✅
- Fixed deprecated pandas `fillna(method='ffill')` → `ffill()`
- Fixed deprecated pandas `fillna(method='bfill')` → `bfill()`
- Added `.gitignore`

### Restructuring ✅
- Created modular folder structure
- Split 1073-line `app.py` into 15+ focused modules
- Added configuration management
- Added utility functions
- Created comprehensive documentation
- Original code backed up as `app_backup.py`

## Troubleshooting

### "Module not found" errors
- Make sure you're in the AutoML directory
- Activate virtual environment
- Run `pip install -r requirements.txt`

### "Cannot find app/main.py"
- You're in the wrong directory
- Run from AutoML root directory

### Old app.py doesn't work anymore
- Use `streamlit run app_backup.py` for old version
- Or use new version: `streamlit run app/main.py`

## Next Steps

1. Test the new structure: `streamlit run app/main.py`
2. Try all features to ensure they work
3. (Optional) Add unit tests
4. (Optional) Set up CI/CD
5. (Optional) Docker containerization

---

**Questions?** See `docs/user_guide.md` or `docs/contributing.md`
