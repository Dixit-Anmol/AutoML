"""
Null Value Handling Module
"""
import streamlit as st
import pandas as pd
from utils.session import save_state


def render_nulls_page():
    """Render the Handle Null Values page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
    st.header("🔴 Handle Null Values")
    
    # Recalculate null counts every time the page loads
    null_counts = st.session_state.df.isnull().sum()
    
    if null_counts.sum() == 0:
        st.success("✅ No null values found in the dataset!")
    else:
        st.subheader("Null Value Summary")
        null_df = pd.DataFrame({
            'Column': null_counts[null_counts > 0].index,
            'Null Count': null_counts[null_counts > 0].values,
            'Percentage': (null_counts[null_counts > 0].values / len(st.session_state.df) * 100).round(2)
        }).astype(str)
        st.dataframe(null_df, width='stretch')
        
        st.subheader("🛠️ Handle Null Values")
        operation = st.radio("Select Operation", ["Remove Rows with Nulls", "Fill Null Values"])
        
        if operation == "Remove Rows with Nulls":
            scope = st.radio("Scope", ["Remove rows with ANY null", "Remove rows with nulls in specific column(s)"])
            
            if scope == "Remove rows with ANY null":
                if st.button("Remove All Rows with Null Values"):
                    save_state("Remove rows with null values")
                    st.session_state.df = st.session_state.df.dropna()
                    st.rerun()
            else:
                columns_with_nulls = null_counts[null_counts > 0].index.tolist()
                selected_cols = st.multiselect("Select columns", columns_with_nulls)
                
                if st.button("Remove Rows with Nulls in Selected Columns"):
                    save_state(f"Remove nulls in {', '.join(selected_cols)}")
                    st.session_state.df = st.session_state.df.dropna(subset=selected_cols)
                    st.rerun()
        
        else:  # Fill Null Values
            columns_with_nulls = null_counts[null_counts > 0].index.tolist()
            selected_col = st.selectbox("Select column to fill", columns_with_nulls)
            
            fill_method = st.radio("Fill Method", 
                                   ["Mean", "Median", "Mode", "Forward Fill", "Backward Fill", "Custom Value"])
            
            if fill_method == "Custom Value":
                custom_value = st.text_input("Enter custom value")
                if st.button("Fill with Custom Value"):
                    save_state(f"Fill {selected_col} with custom value")
                    st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(custom_value)
                    st.rerun()
            
            elif fill_method == "Mean":
                if st.session_state.df[selected_col].dtype in ['int64', 'float64']:
                    if st.button("Fill with Mean"):
                        save_state(f"Fill {selected_col} with mean")
                        mean_val = st.session_state.df[selected_col].mean()
                        st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(mean_val)
                        st.rerun()
                else:
                    st.error("❌ Mean can only be used for numeric columns")
            
            elif fill_method == "Median":
                if st.session_state.df[selected_col].dtype in ['int64', 'float64']:
                    if st.button("Fill with Median"):
                        save_state(f"Fill {selected_col} with median")
                        median_val = st.session_state.df[selected_col].median()
                        st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(median_val)
                        st.rerun()
                else:
                    st.error("❌ Median can only be used for numeric columns")
            
            elif fill_method == "Mode":
                if st.button("Fill with Mode"):
                    save_state(f"Fill {selected_col} with mode")
                    mode_val = st.session_state.df[selected_col].mode()[0]
                    st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(mode_val)
                    st.rerun()
            
            elif fill_method == "Forward Fill":
                if st.button("Forward Fill"):
                    save_state(f"Forward fill {selected_col}")
                    st.session_state.df[selected_col] = st.session_state.df[selected_col].ffill()
                    st.rerun()
            
            elif fill_method == "Backward Fill":
                if st.button("Backward Fill"):
                    save_state(f"Backward fill {selected_col}")
                    st.session_state.df[selected_col] = st.session_state.df[selected_col].bfill()
                    st.rerun()
