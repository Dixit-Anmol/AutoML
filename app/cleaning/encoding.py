"""
Column Encoding Module
"""
import streamlit as st
import pandas as pd
from utils.session import save_state


def render_encoding_page():
    """Render the Column Encoding page."""
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        return
    
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
                    save_state(f"{encoding_type} on {', '.join(selected_cols)}")
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
