"""
Download Helper Functions
"""
import io
import pickle
from io import StringIO
import streamlit as st


def download_csv(df, filename="data.csv"):
    """Create download button for CSV."""
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label=f"📥 Download {filename}",
        data=csv_data,
        file_name=filename,
        mime="text/csv"
    )


def download_excel(df, filename="data.xlsx"):
    """Create download button for Excel."""
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_data = excel_buffer.getvalue()
    
    st.download_button(
        label=f"📥 Download {filename}",
        data=excel_data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def download_model(model, model_name):
    """Create download button for trained model."""
    model_data = pickle.dumps(model)
    filename = f"{model_name.replace(' ', '_')}.pkl"
    
    st.download_button(
        label=f"📥 Download {model_name}",
        data=model_data,
        file_name=filename,
        mime="application/octet-stream"
    )
