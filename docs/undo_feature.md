# 🔄 Undo Feature Documentation

## Overview

The AutoML application now includes a powerful **Undo** feature that allows users to revert their latest dataset changes during the data cleaning workflow.

## How It Works

### History Management

- **Automatic State Saving**: Before each data modification, the current state of the dataset is automatically saved
- **History Limit**: Up to **10 previous states** are stored (configurable via `MAX_HISTORY_SIZE` in `app/utils/session.py`)
- **Memory Efficient**: Old states are automatically removed when the limit is reached

### Available in Cleaning Workflow

The undo feature is available in the **Data Cleaning** workflow sidebar and tracks changes from:

- ✅ **Handle Null Values**: Remove rows, fill with mean/median/mode/forward fill/backward fill/custom
- ✅ **Handle Duplicates**: Remove all duplicates or based on specific columns  
- ✅ **Data Type Conversion**: Convert column types
- ✅ **Column Encoding**: Label encoding, one-hot encoding, ordinal encoding
- ✅ **Column Management**: Drop columns, rename columns

## User Interface

### Undo Button Location

The undo button appears in the **left sidebar** when you're in the Data Cleaning workflow:

```
🔧 Data Cleaning
← Back to Home
─────────────────
⏮️ Undo
Last: Fill Age with mean
[↶ Undo Last Change] [10]
─────────────────
Select Operation
```

### Features

1. **Last Action Display**: Shows description of the most recent change
2. **Undo Button**: Click to revert the last change
3. **History Count**: Shows how many states you can undo (max 10)
4. **Success Message**: Confirms what was undone after clicking

### Example Usage

1. Upload a dataset
2. Fill null values in "Age" column with mean → *State saved*
3. Remove duplicates → *State saved*
4. Encode "Gender" column → *State saved*
5. Click **"↶ Undo Last Change"** → Encoding is reverted
6. Click again → Duplicate removal is reverted
7. Click again → Null filling is reverted

## Technical Implementation

### Files Modified

1. **`app/utils/session.py`**
   - Added `save_state(description)` - Saves current dataframe state
   - Added `undo()` - Restores previous state
   - Added `can_undo()` - Checks if undo is available
   - Added `get_history_count()` - Returns number of undo states
   - Added `get_last_action()` - Returns description of last action

2. **`app/main.py`**
   - Added undo button to cleaning workflow sidebar
   - Displays last action and history count

3. **Cleaning Modules** (all updated):
   - `app/cleaning/nulls.py` - 9 save points
   - `app/cleaning/duplicates.py` - 2 save points
   - `app/cleaning/conversion.py` - 1 save point
   - `app/cleaning/encoding.py` - 1 save point
   - `app/cleaning/columns.py` - 2 save points

### Code Example

```python
from utils.session import save_state

# Before making a change
if st.button("Remove Duplicates"):
    save_state("Remove all duplicates")  # Save current state
    st.session_state.df = st.session_state.df.drop_duplicates()
    st.rerun()
```

## Configuration

### History Size

Modify in `app/utils/session.py`:

```python
# Maximum number of history states to keep
MAX_HISTORY_SIZE = 10  # Change to desired value
```

**Note**: Higher values use more memory, especially with large datasets.

## Limitations

1. **Workflow-Specific**: Undo only works in the **Data Cleaning** workflow, not in Model Training
2. **Session-Based**: History is lost when you refresh the page or close the browser
3. **Memory Limit**: Stores up to 10 states by default (can be configured)
4. **Filter Data Not Tracked**: The "Filter Data" operation is for analysis only and doesn't modify the main dataset, so it's not tracked

## Future Enhancements

Potential improvements:
- **Redo functionality** - Restore undone changes
- **Persistent history** - Save history to disk
- **History browser** - View and jump to any previous state
- **State comparison** - Show diff between states
- **Export history** - Save change log

## Benefits

✅ **Mistake Recovery**: Quickly revert unwanted changes  
✅ **Experimentation**: Try different approaches without fear  
✅ **Learning Tool**: See the impact of each operation  
✅ **Workflow Confidence**: Work faster knowing you can undo  

---

**Enjoy safer, more confident data cleaning! 🎉**
