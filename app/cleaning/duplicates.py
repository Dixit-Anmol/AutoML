"""
Duplicate Handling Module
"""
import streamlit as st
from utils.session import save_state


def render_duplicates_page():
    """Render the Handle Duplicates page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
    st.header("🔄 Handle Duplicates")
    
    duplicate_count = st.session_state.df.duplicated().sum()
    
    if duplicate_count == 0:
        st.success("✅ No duplicate rows found in the dataset!")
    else:
        st.subheader("Duplicate Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Duplicate Rows", duplicate_count)
        with col2:
            st.metric("Percentage", f"{(duplicate_count/len(st.session_state.df)*100):.2f}%")
        
        st.subheader("Sample Duplicate Rows")
        df = st.session_state.df[st.session_state.df.duplicated(keep=False)].head(10).astype(str)
        st.dataframe(df, width='stretch')
        
        st.subheader("🛠️ Remove Duplicates")
        scope = st.radio("Scope", 
                        ["Remove all duplicates", "Remove duplicates based on specific column(s)"])
        
        if scope == "Remove all duplicates":
            if st.button("Remove All Duplicate Rows"):
                save_state("Remove all duplicates")
                st.session_state.df = st.session_state.df.drop_duplicates()
                st.success(f"✅ Removed all duplicate rows. New shape: {st.session_state.df.shape}")
                df = st.session_state.df.head().astype(str)
                st.dataframe(df, width='stretch')
        else:
            selected_cols = st.multiselect("Select columns to check for duplicates", 
                                          st.session_state.df.columns.tolist())
            
            if st.button("Remove Duplicates Based on Selected Columns"):
                save_state(f"Remove duplicates in {', '.join(selected_cols)}")
                st.session_state.df = st.session_state.df.drop_duplicates(subset=selected_cols)
                st.success(f"✅ Removed duplicates based on selected columns. New shape: {st.session_state.df.shape}")
                df = st.session_state.df.head().astype(str)
                st.dataframe(df, width='stretch')
