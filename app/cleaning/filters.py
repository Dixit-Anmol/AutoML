"""
Data Filtering Module
"""
import streamlit as st
from io import StringIO


def render_filters_page():
    """Render the Filter Data page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
    st.header("🔍 Filter Data (Analysis Only)")
    st.info("ℹ️ Filters are applied for analysis only and won't affect the main dataset")
    
    # Initialize filtered_df for analysis
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = st.session_state.df.copy()
    
    st.subheader("🛠️ Apply Filters")
    selected_col = st.selectbox("Select column to filter", st.session_state.df.columns.tolist())
    
    col_dtype = st.session_state.df[selected_col].dtype
    
    if col_dtype in ['int64', 'float64']:
        filter_type = st.radio("Filter Type", ["Range", "Greater Than", "Less Than", "Equal To"])
        
        if filter_type == "Range":
            min_val = st.number_input("Minimum value", value=float(st.session_state.df[selected_col].min()))
            max_val = st.number_input("Maximum value", value=float(st.session_state.df[selected_col].max()))
            
            if st.button("Apply Range Filter"):
                st.session_state.filtered_df = st.session_state.df[
                    (st.session_state.df[selected_col] >= min_val) & 
                    (st.session_state.df[selected_col] <= max_val)
                ]
                st.success(f"✅ Filtered data for analysis. Shape: {st.session_state.filtered_df.shape}")
                df = st.session_state.filtered_df.head().astype(str)
                st.dataframe(df, width='stretch')
                
                # Download button for filtered data
                csv_buffer = StringIO()
                st.session_state.filtered_df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv_data,
                    file_name="filtered_data.csv",
                    mime="text/csv"
                )
        
        elif filter_type == "Greater Than":
            threshold = st.number_input("Value")
            if st.button("Apply Filter"):
                st.session_state.filtered_df = st.session_state.df[st.session_state.df[selected_col] > threshold]
                st.success(f"✅ Filtered data for analysis. Shape: {st.session_state.filtered_df.shape}")
                df = st.session_state.filtered_df.head().astype(str)
                st.dataframe(df, width='stretch')
                
                csv_buffer = StringIO()
                st.session_state.filtered_df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv_data,
                    file_name="filtered_data.csv",
                    mime="text/csv"
                )
        
        elif filter_type == "Less Than":
            threshold = st.number_input("Value")
            if st.button("Apply Filter"):
                st.session_state.filtered_df = st.session_state.df[st.session_state.df[selected_col] < threshold]
                st.success(f"✅ Filtered data for analysis. Shape: {st.session_state.filtered_df.shape}")
                df = st.session_state.filtered_df.head().astype(str)
                st.dataframe(df, width='stretch')
                
                csv_buffer = StringIO()
                st.session_state.filtered_df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv_data,
                    file_name="filtered_data.csv",
                    mime="text/csv"
                )
        
        elif filter_type == "Equal To":
            value = st.number_input("Value")
            if st.button("Apply Filter"):
                st.session_state.filtered_df = st.session_state.df[st.session_state.df[selected_col] == value]
                st.success(f"✅ Filtered data for analysis. Shape: {st.session_state.filtered_df.shape}")
                df = st.session_state.filtered_df.head().astype(str)
                st.dataframe(df, width='stretch')
                
                csv_buffer = StringIO()
                st.session_state.filtered_df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv_data,
                    file_name="filtered_data.csv",
                    mime="text/csv"
                )
    
    else:  # String/Object columns
        unique_values = st.session_state.df[selected_col].unique().tolist()
        selected_values = st.multiselect("Select values to keep", unique_values)
        
        if st.button("Apply Filter"):
            st.session_state.filtered_df = st.session_state.df[st.session_state.df[selected_col].isin(selected_values)]
            st.success(f"✅ Filtered data for analysis. Shape: {st.session_state.filtered_df.shape}")
            df = st.session_state.filtered_df.head().astype(str)
            st.dataframe(df, width='stretch')
            
            csv_buffer = StringIO()
            st.session_state.filtered_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv_data,
                file_name="filtered_data.csv",
                mime="text/csv"
            )
