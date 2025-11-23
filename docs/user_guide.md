# AutoML User Guide

## Getting Started

### Installation

1. **Clone or download the repository**:
   ```bash
   cd AutoML
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the application with:
```bash
streamlit run app/main.py
```

The application will open at `http://localhost:8501`

---

## Data Cleaning Workflow

### Step 1: Upload Your Dataset

1. Click **"Start Cleaning"** on the home page
2. Navigate to **"Upload & Explore"**
3. Upload a CSV file
4. Review the dataset statistics and data types

### Step 2: Handle Null Values

1. Navigate to **"Handle Null Values"**
2. Review null value summary
3. Choose an operation:
   - **Remove rows**: Delete rows containing nulls
   - **Fill values**: Replace nulls with mean/median/mode/forward fill/backward fill/custom value

### Step 3: Remove Duplicates

1. Navigate to **"Handle Duplicates"**
2. Review duplicate summary
3. Remove duplicates:
   - All duplicates
   - Based on specific columns

### Step 4: Convert Data Types

1. Navigate to **"Data Type Conversion"**
2. Select a column
3. Choose target data type
4. Apply conversion

**Tip**: The converter intelligently handles currency symbols and number formatting!

### Step 5: Encode Categorical Data

1. Navigate to **"Column Encoding"**
2. Select categorical columns
3. Choose encoding method:
   - **Label Encoding**: For tree-based models
   - **One-Hot Encoding**: For linear models
   - **Ordinal Encoding**: For ordered categories

### Step 6: Download Cleaned Data

1. Navigate to **"Download"**
2. Review summary and comparison
3. Download as CSV or Excel

---

## Model Training Workflow

### Step 1: Load Data

1. Click **"Start Training"** on the home page
2. Either:
   - Upload a new CSV file, or
   - Import cleaned data from the cleaning module

### Step 2: Configure Training

Use the sidebar to configure:
- **Target Column**: Select your target variable
- **Problem Type**: Classification or Regression
- **Test Set Size**: 10-50%

### Step 3: Train Models

1. Click **"🚀 Train Models"**
2. Wait for training to complete
3. Review results table

**Classification Models**:
- Logistic Regression
- Random Forest
- Decision Tree
- SVM

**Regression Models**:
- Linear Regression
- Random Forest
- Decision Tree
- SVM
- XGBoost

### Step 4: Review Performance

- View **performance comparison** charts
- Check **model rankings**
- Review **detailed metrics**

### Step 5: Test Models

1. Select a model to test
2. Click **"🚀 Test Model"**
3. Review:
   - Classification: Accuracy, Precision, Recall, F1, Confusion Matrix
   - Regression: MSE, RMSE, MAE, R², Residual Distribution

### Step 6: Download Models

1. Select a trained model
2. Click **"📥 Download"**
3. Save the `.pkl` file for deployment

---

## Tips & Best Practices

### Data Preparation

✅ **Do**:
- Remove or fill null values before training
- Encode all categorical columns
- Check for and remove duplicates
- Ensure target variable is appropriate for problem type

❌ **Don't**:
- Train models with null values
- Use categorical data without encoding
- Mix problem types (classification target with regression model)

### Model Selection

**Classification**:
- Use **Logistic Regression** for interpretability
- Use **Random Forest** for best accuracy (usually)
- Use **SVM** for complex decision boundaries

**Regression**:
- Use **Linear Regression** for interpretability
- Use **Random Forest** or **XGBoost** for best performance
- Check **R² score** for model fit quality

### Performance Metrics

**Classification**:
- **Accuracy**: Overall correctness
- **Precision**: When it predicts positive, how often is it correct?
- **Recall**: Of all actual positives, how many did it find?
- **F1-Score**: Harmonic mean of precision and recall

**Regression**:
- **MSE**: Mean squared error (lower is better)
- **RMSE**: Root mean squared error (same units as target)
- **MAE**: Mean absolute error (average prediction error)
- **R² Score**: How well the model explains variance (1.0 is perfect)

---

## Troubleshooting

### "Non-numeric columns found" error

**Solution**: Use Column Encoding to encode all categorical columns before training.

### Training is slow

**Solution**: 
- Reduce dataset size
- Use fewer features
- Reduce n_estimators for tree-based models

### Poor model performance

**Solutions**:
- Clean data more thoroughly
- Remove outliers
- Try different encoding methods
- Adjust test set size
- Collect more data

---

## Keyboard Shortcuts

- `Ctrl+R` or `F5`: Refresh the app (will reset session)
- `Ctrl+Shift+R`: Hard refresh (clears cache)

---

**Need more help?** Check the [README.md](../README.md) or create an issue on GitHub.
