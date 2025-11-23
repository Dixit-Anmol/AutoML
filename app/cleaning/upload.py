"""
Upload and Explore Dataset Module
"""
import streamlit as st
import pandas as pd
from config import PREVIEW_ROWS


def render_upload_page():
    """Render the Upload & Explore page."""
    st.header("📁 Upload & Explore Dataset")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.original_df = st.session_state.df.copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Dataset Head")
            df = st.session_state.df.head(PREVIEW_ROWS).astype(str)
            st.dataframe(df, width='stretch')
        
        with col2:
            st.subheader("📊 Dataset Description")
            df = st.session_state.df.describe().astype(str)
            st.dataframe(df, width='stretch')
        
        st.subheader("📈 Dataset Info")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", st.session_state.df.shape[0])
        with col2:
            st.metric("Total Columns", st.session_state.df.shape[1])
        with col3:
            st.metric("Total Null Values", st.session_state.df.isnull().sum().sum())
        with col4:
            st.metric("Total Duplicates", st.session_state.df.duplicated().sum())
        
        st.subheader("🔍 Data Types")
        df = pd.DataFrame({
            'Column': st.session_state.df.columns,
            'Data Type': st.session_state.df.dtypes.values,
            'Non-Null Count': st.session_state.df.count().values,
            'Null Count': st.session_state.df.isnull().sum().values
        }).astype(str)
        st.dataframe(df, width='stretch')
