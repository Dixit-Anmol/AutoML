"""
Model Training Module
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                            mean_squared_error, r2_score, mean_absolute_error)
from config import DEFAULT_TEST_SIZE, RANDOM_STATE
from training.visualizations import render_visualizations
from training.evaluator import render_testing_section


def render_trainer_page():
    """Render the Model Trainer page."""
    st.header("🤖 Machine Learning Model Trainer")
    st.write("Upload your cleaned dataset and train classification or regression models:")
    
    # Initialize session state for models
    if 'trained_models' not in st.session_state:
        st.session_state.trained_models = {}
    if 'model_results' not in st.session_state:
        st.session_state.model_results = None
    
    # Data loading options
    if st.session_state.df is None:
        st.subheader("📁 Load Dataset")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Option 1: Upload CSV File**")
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'], key="training_upload")
            if uploaded_file is not None:
                st.session_state.df = pd.read_csv(uploaded_file)
                st.success("✅ Dataset loaded successfully!")
                st.rerun()
        
        with col2:
            st.write("**Option 2: Import from Cleaning Module**")
            if st.button("Import Cleaned Data", use_container_width=True, key="import_from_cleaning"):
                if st.session_state.df is not None:
                    st.success("✅ Cleaned data imported from cleaning module!")
                    st.rerun()
                else:
                    st.error("❌ No cleaned data available. Please clean a dataset first in the Data Cleaning module.")
    
    if st.session_state.df is not None:
        render_configuration_sidebar()
        render_dataset_preview()
        
        if st.session_state.get('train_button_clicked'):
            train_models()
        
        if st.session_state.model_results is not None:
            render_results()


def render_configuration_sidebar():
    """Render the sidebar configuration."""
    with st.sidebar:
        st.subheader("📊 Data Configuration")
        
        # Dataset info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", st.session_state.df.shape[0])
        with col2:
            st.metric("Columns", st.session_state.df.shape[1])
        with col3:
            st.metric("Memory", f"{st.session_state.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        st.divider()
        
        # Target variable selection
        st.write("**Select Target Variable**")
        target_col = st.selectbox("Target Column", st.session_state.df.columns.tolist())
        st.session_state['target_col'] = target_col
        
        st.divider()
        
        # Problem type selection
        st.write("**Select Problem Type**")
        problem_type = st.radio("Problem Type", ["Classification", "Regression"])
        st.session_state['problem_type'] = problem_type
        
        st.divider()
        
        # Test set size
        st.write("**Test Set Size**")
        test_size = st.slider("Test Set Size (%)", 10, 50, 20, step=5) / 100
        st.session_state['test_size'] = test_size
        
        st.divider()
        
        if st.button("🚀 Train Models", use_container_width=True, key="train_models_btn"):
            st.session_state['train_button_clicked'] = True
            st.rerun()


def render_dataset_preview():
    """Render dataset preview section."""
    st.subheader("📈 Dataset Preview")
    with st.expander("Dataset Preview", expanded=True):
        df = st.session_state.df.head(10).astype(str)
        st.dataframe(df, width='stretch')
    
    with st.expander("Dataset Info"):
        st.write(f"**Shape:** {st.session_state.df.shape}")
        st.write(f"**Data Types:**")
        df = pd.DataFrame({
            'Column': st.session_state.df.columns,
            'Type': st.session_state.df.dtypes.values
        }).astype(str)
        st.dataframe(df, width='stretch')


def train_models():
    """Train machine learning models."""
    try:
        target_col = st.session_state.get('target_col')
        problem_type = st.session_state.get('problem_type')
        test_size = st.session_state.get('test_size', DEFAULT_TEST_SIZE)
        
        # Prepare data
        X = st.session_state.df.drop(columns=[target_col])
        y = st.session_state.df[target_col]
        
        # Check for non-numeric columns
        non_numeric_cols = X.select_dtypes(include=['object']).columns.tolist()
        if non_numeric_cols:
            st.error(f"❌ Non-numeric columns found: {non_numeric_cols}. Please encode them first.")
            st.session_state['train_button_clicked'] = False
        else:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=RANDOM_STATE)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Store test data in session state for testing section
            st.session_state.X_test_scaled = X_test_scaled
            st.session_state.y_test = y_test
            st.session_state.scaler = scaler
            
            results = []
            
            if problem_type == "Classification":
                results = train_classification_models(X_train_scaled, X_test_scaled, y_train, y_test)
            else:  # Regression
                results = train_regression_models(X_train_scaled, X_test_scaled, y_train, y_test)
            
            st.session_state.model_results = pd.DataFrame(results)
            st.session_state['train_button_clicked'] = False
            st.success("✅ Models trained successfully!")
    
    except Exception as e:
        st.error(f"❌ Error during training: {str(e)}")
        st.session_state['train_button_clicked'] = False


def train_classification_models(X_train, X_test, y_train, y_test):
    """Train classification models."""
    st.info("🔄 Training Classification Models...")
    progress_bar = st.progress(0)
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
        "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "SVM": SVC(kernel='rbf', random_state=RANDOM_STATE)
    }
    
    results = []
    
    for idx, (name, model) in enumerate(models.items()):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        results.append({
            "Model": name,
            "Accuracy": round(accuracy, 4),
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "F1-Score": round(f1, 4),
            "Type": "Classification"
        })
        
        st.session_state.trained_models[name] = model
        progress_bar.progress((idx + 1) / len(models))
    
    return results


def train_regression_models(X_train, X_test, y_train, y_test):
    """Train regression models."""
    st.info("🔄 Training Regression Models...")
    progress_bar = st.progress(0)
    
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE),
        "Decision Tree": DecisionTreeRegressor(random_state=RANDOM_STATE),
        "SVM": SVR(kernel='rbf'),
        "XGBoost": XGBRegressor(n_estimators=100, random_state=RANDOM_STATE, verbosity=0)
    }
    
    results = []
    
    for idx, (name, model) in enumerate(models.items()):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            "Model": name,
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "MAE": round(mae, 4),
            "R² Score": round(r2, 4),
            "Type": "Regression"
        })
        
        st.session_state.trained_models[name] = model
        progress_bar.progress((idx + 1) / len(models))
    
    return results


def render_results():
    """Render training results and visualizations."""
    st.subheader("📊 Model Results")
    df = st.session_state.model_results.astype(str)
    st.dataframe(df, width='stretch')
    
    # Visualizations
    render_visualizations()
    
    # Testing section
    render_testing_section()
    
    # Download models section
    render_download_models()


def render_download_models():
    """Render model download section."""
    from utils.download import download_model
    
    st.subheader("📥 Download Models")
    selected_model = st.selectbox("Select model to download", list(st.session_state.trained_models.keys()))
    
    if selected_model:
        download_model(st.session_state.trained_models[selected_model], selected_model)
        
        # Show model metrics
        model_row = st.session_state.model_results[
            st.session_state.model_results['Model'] == selected_model
        ].iloc[0]
        
        st.subheader(f"📈 {selected_model} Metrics")
        metric_items = [(col_name, value) for col_name, value in model_row.items() 
                       if col_name not in ["Model", "Type"]]
        metric_cols = st.columns(len(metric_items))
        
        for idx, (col_name, value) in enumerate(metric_items):
            with metric_cols[idx]:
                st.metric(col_name, value)
