"""
Download Module for Cleaned Data
"""
import streamlit as st
import pandas as pd
from utils.download import download_csv, download_excel


def render_download_page():
    """Render the Download page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
    st.header("📥 Download Cleaned Dataset")
    
    st.subheader("Dataset Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", st.session_state.df.shape[0])
    with col2:
        st.metric("Total Columns", st.session_state.df.shape[1])
    with col3:
        st.metric("Remaining Null Values", st.session_state.df.isnull().sum().sum())
    
    st.subheader("Preview of Cleaned Data")
    df = st.session_state.df.head(20).astype(str)
    st.dataframe(df, width='stretch')
    
    st.subheader("📥 Download Options")
    
    # Download CSV
    download_csv(st.session_state.df, "cleaned_dataset.csv")
    
    # Download Excel
    download_excel(st.session_state.df, "cleaned_dataset.xlsx")
    
    st.divider()
    
    st.subheader("🚀 Next Steps")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Model Training", use_container_width=True, key="move_to_training"):
            st.session_state.workflow = "training"
            st.rerun()
    
    with col2:
        if st.button("Continue Cleaning", use_container_width=True, key="continue_cleaning"):
            st.rerun()
    
    st.subheader("📊 Comparison with Original")
    comparison_df = pd.DataFrame({
        'Metric': ['Rows', 'Columns', 'Null Values', 'Duplicates'],
        'Original': [
            st.session_state.original_df.shape[0],
            st.session_state.original_df.shape[1],
            st.session_state.original_df.isnull().sum().sum(),
            st.session_state.original_df.duplicated().sum()
        ],
        'Cleaned': [
            st.session_state.df.shape[0],
            st.session_state.df.shape[1],
            st.session_state.df.isnull().sum().sum(),
            st.session_state.df.duplicated().sum()
        ]
    }).astype(str)
    st.dataframe(comparison_df, width='stretch')
