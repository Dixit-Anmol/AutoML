"""
Data Type Conversion Module
"""
import streamlit as st
import pandas as pd
import numpy as np
import re
from utils.session import save_state


def render_conversion_page():
    """Render the Data Type Conversion page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
    st.header("🔄 Data Type Conversion")
    
    st.subheader("Current Data Types")
    df = pd.DataFrame({
        'Column': st.session_state.df.columns,
        'Current Type': st.session_state.df.dtypes.values
    }).astype(str)
    st.dataframe(df, width='stretch')
    
    st.subheader("🛠️ Convert Data Type")
    selected_col = st.selectbox("Select column to convert", st.session_state.df.columns.tolist())
    current_type = str(st.session_state.df[selected_col].dtype)
    
    st.write(f"Current type: **{current_type}**")
    
    new_type = st.selectbox("Convert to", ["int64", "float64", "object", "bool", "datetime64[ns]"])
    
    if st.button("Convert Data Type"):
        try:
            save_state(f"Convert {selected_col} to {new_type}")
            if new_type == "datetime64[ns]":
                st.session_state.df[selected_col] = pd.to_datetime(
                    st.session_state.df[selected_col], errors='coerce')
            elif new_type in ["int64", "float64"]:
                # Clean the data for numeric conversion
                def clean_numeric(val):
                    if pd.isna(val):
                        return np.nan
                    val_str = str(val).strip()
                    
                    # Remove common currency symbols and separators
                    val_str = val_str.replace('₹', '').replace('$', '').replace('€', '').replace('£', '')
                    val_str = val_str.replace(',', '').strip()
                    
                    # Try direct conversion first
                    try:
                        return float(val_str)
                    except ValueError:
                        pass
                    
                    # Extract all numeric parts (including decimals and negative signs)
                    numeric_match = re.search(r'-?\d+\.?\d*', val_str)
                    if numeric_match:
                        try:
                            return float(numeric_match.group())
                        except ValueError:
                            return np.nan
                    
                    # If no numeric part found, return NaN
                    return np.nan
                
                st.session_state.df[selected_col] = st.session_state.df[selected_col].apply(clean_numeric)
                
                # Count null values created
                null_count = st.session_state.df[selected_col].isnull().sum()
                
                if null_count > 0:
                    st.info(f"ℹ️ {null_count} values had no numeric part and were converted to NaN")
                
                st.session_state.df[selected_col] = st.session_state.df[selected_col].astype(new_type)
            else:
                st.session_state.df[selected_col] = st.session_state.df[selected_col].astype(new_type)
            
            st.success(f"✅ Converted '{selected_col}' from {current_type} to {new_type}")
            df = st.session_state.df[[selected_col]].head(10).astype(str)
            st.dataframe(df, width='stretch')
        except Exception as e:
            st.error(f"❌ Error converting data type: {str(e)}")
