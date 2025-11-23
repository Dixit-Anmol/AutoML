"""
ML Yantra - Machine Learning Instrument
Main Application Entry Point
"""
import streamlit as st
from config import PAGE_TITLE, PAGE_LAYOUT
from utils.session import initialize_session_state

# Import cleaning modules
from cleaning.upload import render_upload_page
from cleaning.nulls import render_nulls_page
from cleaning.duplicates import render_duplicates_page
from cleaning.conversion import render_conversion_page
from cleaning.encoding import render_encoding_page
from cleaning.filters import render_filters_page
from cleaning.columns import render_columns_page
from cleaning.download_page import render_download_page

# Import training modules
from training.trainer import render_trainer_page


# Configure Streamlit page
st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)

# Initialize session state
initialize_session_state()

# Initialize page variable
page = None

# Main page selector
if st.session_state.workflow is None:
    # Landing page with workflow selection
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1>🚀 ML Yantra - Your Machine Learning Instrument</h1>
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
    
    # Undo functionality
    from utils.session import can_undo, undo, get_history_count, get_last_action
    
    if can_undo():
        st.sidebar.subheader("⏮️ Undo")
        
        # Show last action
        last_action = get_last_action()
        if last_action:
            st.sidebar.info(f"Last: {last_action}")
        
        col1, col2 = st.sidebar.columns([2, 1])
        with col1:
            if st.button("↶ Undo Last Change", key="undo_btn", use_container_width=True):
                success, action = undo()
                if success:
                    st.success(f"✅ Undone: {action}")
                    st.rerun()
        with col2:
            st.metric("", get_history_count())
        
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


# Route to appropriate page
if page == "Upload & Explore":
    render_upload_page()
elif page == "Handle Null Values":
    render_nulls_page()
elif page == "Handle Duplicates":
    render_duplicates_page()
elif page == "Data Type Conversion":
    render_conversion_page()
elif page == "Column Encoding":
    render_encoding_page()
elif page == "Filter Data":
    render_filters_page()
elif page == "Column Management":
    render_columns_page()
elif page == "Download":
    render_download_page()
elif page == "Model Trainer":
    render_trainer_page()
