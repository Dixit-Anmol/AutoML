import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import pickle
import io
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="ML Trainer", layout="wide")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None

# Initialize workflow state
if 'workflow' not in st.session_state:
    st.session_state.workflow = None

# Initialize page variable
page = None

# Main page selector
if st.session_state.workflow is None:
    # Landing page with workflow selection
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1>🚀 Train Your Machine Learning Model</h1>
        <p style="font-size: 18px; color: #666;">Choose your workflow to get started with data preparation and model training</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="border: 2px solid #f0f0f0; border-radius: 10px; padding: 30px; text-align: center; background-color: #fff5f5;">
            <div style="font-size: 40px; margin-bottom: 15px;">📊</div>
            <h3>Data Cleaning</h3>
            <p style="color: #666; margin-bottom: 20px;">Prepare and clean your dataset for optimal model training</p>
            <ul style="text-align: left; color: #666; margin-bottom: 20px;">
                <li>✓ Remove duplicates and handle missing values</li>
                <li>✓ Normalize and standardize data formats</li>
                <li>✓ Filter outliers and validate data quality</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Cleaning", key="start_cleaning", use_container_width=True):
            st.session_state.workflow = "cleaning"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="border: 2px solid #f0f0f0; border-radius: 10px; padding: 30px; text-align: center; background-color: #f0f8f0;">
            <div style="font-size: 40px; margin-bottom: 15px;">🤖</div>
            <h3>Model Training</h3>
            <p style="color: #666; margin-bottom: 20px;">Train and optimize your machine learning models</p>
            <ul style="text-align: left; color: #666; margin-bottom: 20px;">
                <li>✓ Upload and organize training samples</li>
                <li>✓ Configure model parameters and hyperparameters</li>
                <li>✓ Test and export your trained model</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Training", key="start_training", use_container_width=True):
            st.session_state.workflow = "training"
            st.rerun()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
        <p style="color: #999; font-size: 14px;">No coding required. Train models directly in your browser with an intuitive interface designed for both beginners and experts.</p>
    </div>
    """, unsafe_allow_html=True)

# Data Cleaning Workflow
elif st.session_state.workflow == "cleaning":
    # Sidebar for cleaning navigation
    st.sidebar.title("🔧 Data Cleaning")
    if st.sidebar.button("← Back to Home"):
        st.session_state.workflow = None
        st.rerun()
    
    st.sidebar.divider()
    
    cleaning_page = st.sidebar.radio("Select Operation", [
        "Upload & Explore",
        "Handle Null Values",
        "Handle Duplicates",
        "Data Type Conversion",
        "Column Encoding",
        "Filter Data",
        "Column Management",
        "Download"
    ])
    
    page = cleaning_page

# Model Training Workflow
elif st.session_state.workflow == "training":
    # Sidebar for training navigation
    st.sidebar.title("🤖 Model Training")
    if st.sidebar.button("← Back to Home"):
        st.session_state.workflow = None
        st.rerun()
    
    st.sidebar.divider()
    
    page = "Model Trainer"

# ==================== UPLOAD & EXPLORE ====================
if page == "Upload & Explore":
    st.header("📁 Upload & Explore Dataset")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.original_df = st.session_state.df.copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Dataset Head")
            df = st.session_state.df.head(10).astype(str)
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

# ==================== HANDLE NULL VALUES ====================
elif page == "Handle Null Values":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
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
                        st.session_state.df = st.session_state.df.dropna()
                        st.rerun()
                
                else:
                    columns_with_nulls = null_counts[null_counts > 0].index.tolist()
                    selected_cols = st.multiselect("Select columns", columns_with_nulls)
                    
                    if st.button("Remove Rows with Nulls in Selected Columns"):
                        st.session_state.df = st.session_state.df.dropna(subset=selected_cols)
                        st.rerun()
            
            else:  # Fill Null Values
                columns_with_nulls = null_counts[null_counts > 0].index.tolist()
                selected_col = st.selectbox("Select column to fill", columns_with_nulls)
                
                fill_method = st.radio("Fill Method", ["Mean", "Median", "Mode", "Forward Fill", "Backward Fill", "Custom Value"])
                
                if fill_method == "Custom Value":
                    custom_value = st.text_input("Enter custom value")
                    if st.button("Fill with Custom Value"):
                        st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(custom_value)
                        st.rerun()
                
                elif fill_method == "Mean":
                    if st.session_state.df[selected_col].dtype in ['int64', 'float64']:
                        if st.button("Fill with Mean"):
                            mean_val = st.session_state.df[selected_col].mean()
                            st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(mean_val)
                            st.rerun()
                    else:
                        st.error("❌ Mean can only be used for numeric columns")
                
                elif fill_method == "Median":
                    if st.session_state.df[selected_col].dtype in ['int64', 'float64']:
                        if st.button("Fill with Median"):
                            median_val = st.session_state.df[selected_col].median()
                            st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(median_val)
                            st.rerun()
                    else:
                        st.error("❌ Median can only be used for numeric columns")
                
                elif fill_method == "Mode":
                    if st.button("Fill with Mode"):
                        mode_val = st.session_state.df[selected_col].mode()[0]
                        st.session_state.df[selected_col] = st.session_state.df[selected_col].fillna(mode_val)
                        st.rerun()
                
                elif fill_method == "Forward Fill":
                    if st.button("Forward Fill"):
                        st.session_state.df[selected_col] = st.session_state.df[selected_col].ffill()
                        st.rerun()
                
                elif fill_method == "Backward Fill":
                    if st.button("Backward Fill"):
                        st.session_state.df[selected_col] = st.session_state.df[selected_col].bfill()
                        st.rerun()

# ==================== HANDLE DUPLICATES ====================
elif page == "Handle Duplicates":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
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
            scope = st.radio("Scope", ["Remove all duplicates", "Remove duplicates based on specific column(s)"])
            
            if scope == "Remove all duplicates":
                if st.button("Remove All Duplicate Rows"):
                    st.session_state.df = st.session_state.df.drop_duplicates()
                    st.success(f"✅ Removed all duplicate rows. New shape: {st.session_state.df.shape}")
                    df = st.session_state.df.head().astype(str)
                    st.dataframe(df, width='stretch')
            
            else:
                selected_cols = st.multiselect("Select columns to check for duplicates", st.session_state.df.columns.tolist())
                
                if st.button("Remove Duplicates Based on Selected Columns"):
                    st.session_state.df = st.session_state.df.drop_duplicates(subset=selected_cols)
                    st.success(f"✅ Removed duplicates based on selected columns. New shape: {st.session_state.df.shape}")
                    df = st.session_state.df.head().astype(str)
                    st.dataframe(df, width='stretch')

# ==================== DATA TYPE CONVERSION ====================
elif page == "Data Type Conversion":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
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
                if new_type == "datetime64[ns]":
                    st.session_state.df[selected_col] = pd.to_datetime(st.session_state.df[selected_col], errors='coerce')
                elif new_type in ["int64", "float64"]:
                    # Clean the data for numeric conversion
                    def clean_numeric(val):
                        import re
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

# ==================== COLUMN ENCODING ====================
elif page == "Column Encoding":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        st.header("🔐 Column Encoding")
        
        # Get categorical columns
        categorical_cols = st.session_state.df.select_dtypes(include=['object']).columns.tolist()
        
        if not categorical_cols:
            st.info("ℹ️ No categorical columns found in the dataset")
        else:
            st.subheader("🛠️ Select Columns to Encode")
            selected_cols = st.multiselect("Select one or more columns to encode", categorical_cols)
            
            if selected_cols:
                encoding_type = st.radio("Select Encoding Type", [
                    "Label Encoding",
                    "One-Hot Encoding",
                    "Ordinal Encoding"
                ])
                
                st.info("ℹ️ Encoding Information:")
                if encoding_type == "Label Encoding":
                    st.write("- Converts categories to numeric labels (0, 1, 2, ...)")
                    st.write("- Best for: Tree-based models")
                elif encoding_type == "One-Hot Encoding":
                    st.write("- Creates binary columns for each category")
                    st.write("- Best for: Linear models, neural networks")
                elif encoding_type == "Ordinal Encoding":
                    st.write("- Assigns numeric values based on order")
                    st.write("- Best for: Ordinal categorical data")
                
                if st.button("Apply Encoding"):
                    try:
                        from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
                        
                        df_encoded = st.session_state.df.copy()
                        
                        if encoding_type == "Label Encoding":
                            le_dict = {}
                            for col in selected_cols:
                                le = LabelEncoder()
                                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                                le_dict[col] = dict(zip(le.classes_, le.transform(le.classes_)))
                            
                            st.success(f"✅ Applied Label Encoding to {len(selected_cols)} column(s)")
                            
                            with st.expander("View Encoding Mapping"):
                                for col, mapping in le_dict.items():
                                    st.write(f"**{col}:**")
                                    st.json(mapping)
                        
                        elif encoding_type == "One-Hot Encoding":
                            df_encoded = pd.get_dummies(df_encoded, columns=selected_cols, drop_first=False)
                            st.success(f"✅ Applied One-Hot Encoding to {len(selected_cols)} column(s)")
                            st.info(f"ℹ️ Original columns removed. New binary columns created.")
                        
                        elif encoding_type == "Ordinal Encoding":
                            oe = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
                            df_encoded[selected_cols] = oe.fit_transform(df_encoded[selected_cols])
                            st.success(f"✅ Applied Ordinal Encoding to {len(selected_cols)} column(s)")
                        
                        # Update the main dataframe
                        st.session_state.df = df_encoded
                        
                        st.subheader("📊 Encoded Dataset Preview")
                        df = st.session_state.df.head(10).astype(str)
                        st.dataframe(df, width='stretch')
                        
                        st.subheader("Dataset Info After Encoding")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Rows", st.session_state.df.shape[0])
                        with col2:
                            st.metric("Total Columns", st.session_state.df.shape[1])
                        with col3:
                            st.metric("Data Types", st.session_state.df.dtypes.nunique())
                        
                    except ImportError:
                        st.error("❌ scikit-learn is required for encoding. Install it with: pip install scikit-learn")
                    except Exception as e:
                        st.error(f"❌ Error during encoding: {str(e)}")

# ==================== FILTER DATA ====================
elif page == "Filter Data":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
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
                    st.session_state.filtered_df = st.session_state.df[(st.session_state.df[selected_col] >= min_val) & 
                                                                        (st.session_state.df[selected_col] <= max_val)]
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

# ==================== COLUMN MANAGEMENT ====================
elif page == "Column Management":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        st.header("📋 Column Management")
        
        operation = st.radio("Select Operation", ["Drop Columns", "Rename Columns"])
        
        if operation == "Drop Columns":
            st.subheader("🛠️ Drop Columns")
            columns_to_drop = st.multiselect("Select columns to drop", st.session_state.df.columns.tolist())
            
            if st.button("Drop Selected Columns"):
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
                    st.session_state.df = st.session_state.df.rename(columns=rename_dict)
                    st.success(f"✅ Renamed columns: {rename_dict}")
                    df = st.session_state.df.head().astype(str)
                    st.dataframe(df, width='stretch')
                else:
                    st.info("ℹ️ No columns to rename")

# ==================== MODEL TRAINER ====================
elif page == "Model Trainer":
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
        st.header("🤖 Machine Learning Model Trainer")
        
        # Initialize session state for models
        if 'trained_models' not in st.session_state:
            st.session_state.trained_models = {}
        if 'model_results' not in st.session_state:
            st.session_state.model_results = None
        
        # Sidebar configuration
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
            
            st.divider()
            
            # Problem type selection
            st.write("**Select Problem Type**")
            problem_type = st.radio("Problem Type", ["Classification", "Regression"])
            
            st.divider()
            
            # Test set size
            st.write("**Test Set Size**")
            test_size = st.slider("Test Set Size (%)", 10, 50, 20, step=5) / 100
            
            st.divider()
            
            train_button = st.button("🚀 Train Models", use_container_width=True, key="train_models_btn")
        
        # Main content area
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
        
        # Import required libraries for training and testing
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.linear_model import LogisticRegression, LinearRegression
        from sklearn.svm import SVC, SVR
        from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
        from xgboost import XGBRegressor
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, confusion_matrix, classification_report
        
        # Train models
        if train_button:
            try:
                
                # Prepare data
                X = st.session_state.df.drop(columns=[target_col])
                y = st.session_state.df[target_col]
                
                # Check for non-numeric columns
                non_numeric_cols = X.select_dtypes(include=['object']).columns.tolist()
                if non_numeric_cols:
                    st.error(f"❌ Non-numeric columns found: {non_numeric_cols}. Please encode them first.")
                else:
                    # Split data
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                    
                    # Scale features
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    
                    # Store test data in session state for testing section
                    st.session_state.X_test_scaled = X_test_scaled
                    st.session_state.y_test = y_test
                    st.session_state.problem_type = problem_type
                    
                    results = []
                    
                    if problem_type == "Classification":
                        st.info("🔄 Training Classification Models...")
                        progress_bar = st.progress(0)
                        
                        models = {
                            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
                            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
                            "Decision Tree": DecisionTreeClassifier(random_state=42),
                            "SVM": SVC(kernel='rbf', random_state=42)
                        }
                        
                        for idx, (name, model) in enumerate(models.items()):
                            model.fit(X_train_scaled, y_train)
                            y_pred = model.predict(X_test_scaled)
                            
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
                    
                    else:  # Regression
                        st.info("🔄 Training Regression Models...")
                        progress_bar = st.progress(0)
                        
                        models = {
                            "Linear Regression": LinearRegression(),
                            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
                            "Decision Tree": DecisionTreeRegressor(random_state=42),
                            "SVM": SVR(kernel='rbf'),
                            "XGBoost": XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
                        }
                        
                        for idx, (name, model) in enumerate(models.items()):
                            model.fit(X_train_scaled, y_train)
                            y_pred = model.predict(X_test_scaled)
                            
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
                    
                    st.session_state.model_results = pd.DataFrame(results)
                    st.success("✅ Models trained successfully!")
            
            except Exception as e:
                st.error(f"❌ Error during training: {str(e)}")
        
        # Display results
        if st.session_state.model_results is not None:
            st.subheader("📊 Model Results")
            df = st.session_state.model_results.astype(str)
            st.dataframe(df, width='stretch')
            
            # Visualization section
            st.subheader("📈 Training Visualizations")
            
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                st.write("**Model Performance Comparison**")
                if problem_type == "Classification":
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=st.session_state.model_results['Model'],
                        y=st.session_state.model_results['Accuracy'],
                        marker_color='#1f77b4'
                    ))
                    fig.update_layout(title="Accuracy Comparison", height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=st.session_state.model_results['Model'],
                        y=st.session_state.model_results['R² Score'],
                        marker_color='#2ca02c'
                    ))
                    fig.update_layout(title="R² Score Comparison", height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            
            with viz_col2:
                st.write("**Error Metrics Comparison**")
                if problem_type == "Classification":
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=st.session_state.model_results['Model'],
                        y=st.session_state.model_results['F1-Score'],
                        marker_color='#ff7f0e'
                    ))
                    fig.update_layout(title="F1-Score Comparison", height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=st.session_state.model_results['Model'],
                        y=st.session_state.model_results['RMSE'],
                        marker_color='#d62728'
                    ))
                    fig.update_layout(title="RMSE Comparison", height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Model Ranking
            st.subheader("📊 Model Ranking")
            
            if problem_type == "Classification":
                ranking_df = st.session_state.model_results[['Model', 'Accuracy']].sort_values('Accuracy', ascending=False).reset_index(drop=True)
                ranking_df.index = ranking_df.index + 1
                ranking_df.index.name = 'Rank'
            else:
                ranking_df = st.session_state.model_results[['Model', 'R² Score']].sort_values('R² Score', ascending=False).reset_index(drop=True)
                ranking_df.index = ranking_df.index + 1
                ranking_df.index.name = 'Rank'
            
            df = ranking_df.astype(str)
            st.dataframe(df, width='stretch')
            
            # Test Model Section
            st.subheader("🧪 Test Model on Test Data")
            
            test_col1, test_col2, test_col3 = st.columns([2, 2, 1])
            
            with test_col1:
                test_model_name = st.selectbox("Select model to test", list(st.session_state.trained_models.keys()), key="test_model_select")
            
            with test_col3:
                test_button_clicked = st.button("🚀 Test Model", use_container_width=True, key="test_model_btn")
            
            if test_button_clicked:
                try:
                    # Get test data from session state
                    X_test_scaled = st.session_state.X_test_scaled
                    y_test = st.session_state.y_test
                    problem_type_test = st.session_state.problem_type
                    
                    selected_test_model = st.session_state.trained_models[test_model_name]
                    y_test_pred = selected_test_model.predict(X_test_scaled)
                    
                    st.subheader(f"📊 Test Results for {test_model_name}")
                    
                    if problem_type_test == "Classification":
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
                    
                    else:  # Regression
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
                    
                    st.success("✅ Model testing completed!")
                
                except Exception as e:
                    st.error(f"❌ Error testing model: {str(e)}")
            
            st.subheader("📥 Download Models")
            selected_model = st.selectbox("Select model to download", list(st.session_state.trained_models.keys()))
            
            if selected_model:
                model_data = pickle.dumps(st.session_state.trained_models[selected_model])
                st.download_button(
                    label=f"📥 Download {selected_model}",
                    data=model_data,
                    file_name=f"{selected_model.replace(' ', '_')}.pkl",
                    mime="application/octet-stream"
                )
                
                # Show model metrics
                model_row = st.session_state.model_results[st.session_state.model_results['Model'] == selected_model].iloc[0]
                
                st.subheader(f"📈 {selected_model} Metrics")
                metric_items = [(col_name, value) for col_name, value in model_row.items() if col_name not in ["Model", "Type"]]
                metric_cols = st.columns(len(metric_items))
                
                for idx, (col_name, value) in enumerate(metric_items):
                    with metric_cols[idx]:
                        st.metric(col_name, value)

# ==================== DOWNLOAD ====================
elif page == "Download":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
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
        
        # Download as CSV
        csv_buffer = StringIO()
        st.session_state.df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )
        
        # Download as Excel
        excel_buffer = io.BytesIO()
        st.session_state.df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="📥 Download as Excel",
            data=excel_data,
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
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
