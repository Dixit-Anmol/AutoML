"""
Column Management Module
"""
import streamlit as st
from utils.session import save_state


def render_columns_page():
    """Render the Column Management page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
    st.header("📋 Column Management")
    
    operation = st.radio("Select Operation", ["Drop Columns", "Rename Columns"])
    
    if operation == "Drop Columns":
        st.subheader("🛠️ Drop Columns")
        columns_to_drop = st.multiselect("Select columns to drop", st.session_state.df.columns.tolist())
        
        if st.button("Drop Selected Columns"):
            save_state(f"Drop columns: {', '.join(columns_to_drop)}")
            st.session_state.df = st.session_state.df.drop(columns=columns_to_drop)
            st.success(f"✅ Dropped columns: {', '.join(columns_to_drop)}. New shape: {st.session_state.df.shape}")
            df = st.session_state.df.head().astype(str)
            st.dataframe(df, width='stretch')
    
    else:  # Rename Columns
        st.subheader("🛠️ Rename Columns")
        
        col1, col2 = st.columns(2)
        rename_dict = {}
        
        for col in st.session_state.df.columns:
            with col1:
                st.write(f"**{col}**")
            with col2:
                new_name = st.text_input(f"New name for {col}", value=col, key=f"rename_{col}")
                if new_name != col:
                    rename_dict[col] = new_name
        
        if st.button("Apply Rename"):
            if rename_dict:
                save_state(f"Rename columns: {list(rename_dict.keys())}")
                st.session_state.df = st.session_state.df.rename(columns=rename_dict)
                st.success(f"✅ Renamed columns: {rename_dict}")
                df = st.session_state.df.head().astype(str)
                st.dataframe(df, width='stretch')
            else:
                st.info("ℹ️ No columns to rename")
