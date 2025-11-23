# 🚀 ML Yantra - Machine Learning Instrument

A comprehensive web-based machine learning application built with **Streamlit** that enables users to prepare data and train machine learning models without writing code.

## ✨ Features

### 📊 Data Cleaning Workflow
- **Upload & Explore**: Load CSV files and analyze dataset structure
- **Handle Null Values**: Remove or fill missing values using multiple strategies (Mean, Median, Mode, Forward/Backward Fill, Custom Values)
- **Handle Duplicates**: Detect and remove duplicate rows
- **Data Type Conversion**: Convert columns between different data types with intelligent parsing
- **Column Encoding**: Apply Label Encoding, One-Hot Encoding, or Ordinal Encoding to categorical data
- **Filter Data**: Analyze data with various filtering options (Range, Greater Than, Less Than, Equal To)
- **Column Management**: Drop or rename columns as needed
- **Download**: Export cleaned datasets as CSV or Excel

### 🤖 Model Training Workflow
- **Classification Models**: Train Logistic Regression, Random Forest, Decision Tree, and SVM
- **Regression Models**: Train Linear Regression, Random Forest, Decision Tree, SVM, and XGBoost
- **Automatic Scaling**: Features are automatically scaled using StandardScaler
- **Model Comparison**: View performance metrics side-by-side
- **Model Testing**: Test trained models on test data with detailed metrics
- **Visualizations**: Interactive charts comparing model performance
- **Model Export**: Download trained models as pickle files

## 📋 Requirements

- Python 3.8+
- All dependencies listed in `requirements.txt`

## 🔧 Installation

1. **Clone or download the repository**
   ```bash
   cd AutoML
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

Start the Streamlit application:
```bash
streamlit run app/main.py
```

> **Note**: The project has been restructured for better maintainability. The entry point is now `app/main.py` instead of `app.py`.

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Data Cleaning Workflow

1. **Start Cleaning**: Click "Start Cleaning" on the home page
2. **Upload Dataset**: Upload a CSV file in the "Upload & Explore" section
3. **Explore Data**: View dataset statistics, data types, and quality metrics
4. **Clean Data**: Use the sidebar to navigate through cleaning operations:
   - Remove or fill null values
   - Handle duplicate rows
   - Convert data types
   - Encode categorical columns
   - Filter data for analysis
   - Manage columns
5. **Download**: Export your cleaned dataset as CSV or Excel

### Model Training Workflow

1. **Start Training**: Click "Start Training" on the home page
2. **Load Data**: Either upload a CSV or import cleaned data from the Data Cleaning module
3. **Configure Model**:
   - Select target variable
   - Choose problem type (Classification or Regression)
   - Set test set size
4. **Train Models**: Click "Train Models" to train all available models
5. **Review Results**: 
   - View model performance metrics
   - Compare models with visualizations
   - Check model rankings
6. **Test Models**: Select a trained model and test it on test data
7. **Download Models**: Export trained models as pickle files

## 📊 Supported Models

### Classification
- Logistic Regression
- Random Forest Classifier
- Decision Tree Classifier
- Support Vector Machine (SVM)

### Regression
- Linear Regression
- Random Forest Regressor
- Decision Tree Regressor
- Support Vector Machine (SVR)
- XGBoost Regressor

## 📈 Metrics

### Classification Metrics
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Classification Report

### Regression Metrics
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- R² Score
- Residuals Distribution

## 🛠️ Data Preparation Features

### Null Value Handling
- Remove rows with null values (all or specific columns)
- Fill with Mean, Median, Mode
- Forward Fill / Backward Fill
- Custom value filling

### Data Type Conversion
- Automatic numeric parsing (handles currency symbols, separators)
- Conversion to: int64, float64, object, bool, datetime64[ns]
- Intelligent error handling

### Encoding Methods
- **Label Encoding**: Converts categories to numeric labels (0, 1, 2, ...)
- **One-Hot Encoding**: Creates binary columns for each category
- **Ordinal Encoding**: Assigns numeric values based on order

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.35.0 | Web framework |
| pandas | ≥2.1.0 | Data manipulation |
| numpy | ≥1.26.0 | Numerical computing |
| scikit-learn | ≥1.3.0 | ML algorithms & preprocessing |
| xgboost | ≥2.0.0 | Gradient boosting |
| plotly | ≥5.17.0 | Interactive visualizations |
| matplotlib | ≥3.7.0 | Static visualizations |
| openpyxl | ≥3.1.2 | Excel file support |

## 💡 Tips & Best Practices

1. **Data Quality**: Ensure your data is clean before training models
2. **Encoding**: Encode all categorical columns before model training
3. **Test Size**: Use 20-30% for test set size for better generalization
4. **Model Selection**: Compare metrics to choose the best model for your use case
5. **Export Models**: Download trained models for use in production

## ⚠️ Limitations

- Models require all numeric features (encode categorical data first)
- Large datasets may take longer to process
- Session state is lost when the app is refreshed
- Models are trained on the entire dataset (no cross-validation)

## 🐛 Troubleshooting

### "Non-numeric columns found" error
- Use the Column Encoding section to encode all categorical columns

### Model training fails
- Check that your target variable is appropriate for the problem type
- Ensure all features are numeric
- Verify sufficient data (at least 10+ samples)

### Download buttons not working
- Check browser pop-up settings
- Ensure sufficient disk space
- Try a different browser

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Happy Machine Learning! 🎉**
