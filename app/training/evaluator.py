"""
Model Evaluation and Testing Module
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                            mean_squared_error, r2_score, mean_absolute_error,
                            confusion_matrix, classification_report)
import plotly.graph_objects as go


def render_testing_section():
    """Render the model testing section."""
    st.subheader("🧪 Test Model on Test Data")
    
    test_col1, test_col2, test_col3 = st.columns([2, 2, 1])
    
    with test_col1:
        test_model_name = st.selectbox("Select model to test", 
                                      list(st.session_state.trained_models.keys()), 
                                      key="test_model_select")
    
    with test_col3:
        test_button_clicked = st.button("🚀 Test Model", use_container_width=True, key="test_model_btn")
    
    if test_button_clicked:
        test_model(test_model_name)


def test_model(model_name):
    """Test a trained model on test data."""
    try:
        # Get test data from session state
        X_test_scaled = st.session_state.X_test_scaled
        y_test = st.session_state.y_test
        problem_type = st.session_state.get('problem_type')
        
        selected_test_model = st.session_state.trained_models[model_name]
        y_test_pred = selected_test_model.predict(X_test_scaled)
        
        st.subheader(f"📊 Test Results for {model_name}")
        
        if problem_type == "Classification":
            render_classification_results(y_test, y_test_pred)
        else:  # Regression
            render_regression_results(y_test, y_test_pred)
        
        st.success("✅ Model testing completed!")
    
    except Exception as e:
        st.error(f"❌ Error testing model: {str(e)}")


def render_classification_results(y_test, y_test_pred):
    """Render classification model test results."""
    # Classification metrics
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
    test_recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
    test_f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
    
    # Display metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Accuracy", f"{test_accuracy:.4f}")
    with metric_col2:
        st.metric("Precision", f"{test_precision:.4f}")
    with metric_col3:
        st.metric("Recall", f"{test_recall:.4f}")
    with metric_col4:
        st.metric("F1-Score", f"{test_f1:.4f}")
    
    # Confusion Matrix
    st.write("**Confusion Matrix**")
    cm = confusion_matrix(y_test, y_test_pred)
    cm_df = pd.DataFrame(cm, columns=[f"Predicted {i}" for i in range(len(cm))],
                        index=[f"Actual {i}" for i in range(len(cm))]).astype(str)
    st.dataframe(cm_df, width='stretch')
    
    # Classification Report
    st.write("**Classification Report**")
    report = classification_report(y_test, y_test_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose().astype(str)
    st.dataframe(report_df, width='stretch')


def render_regression_results(y_test, y_test_pred):
    """Render regression model test results."""
    # Regression metrics
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    # Display metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("MSE", f"{test_mse:.4f}")
    with metric_col2:
        st.metric("RMSE", f"{test_rmse:.4f}")
    with metric_col3:
        st.metric("MAE", f"{test_mae:.4f}")
    with metric_col4:
        st.metric("R² Score", f"{test_r2:.4f}")
    
    # Prediction vs Actual
    st.write("**Prediction vs Actual Values**")
    comparison_df = pd.DataFrame({
        'Actual': y_test.values[:20],
        'Predicted': y_test_pred[:20],
        'Difference': (y_test.values[:20] - y_test_pred[:20])
    }).astype(str)
    st.dataframe(comparison_df, width='stretch')
    
    # Residual plot
    st.write("**Residuals Distribution**")
    residuals = y_test.values - y_test_pred
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=residuals,
        nbinsx=30,
        marker_color='#1f77b4'
    ))
    fig.update_layout(
        title="Residuals Distribution",
        xaxis_title="Residuals",
        yaxis_title="Frequency",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
