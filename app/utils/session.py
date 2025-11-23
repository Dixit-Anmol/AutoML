"""
Session State Management Utilities
"""
import streamlit as st
import pandas as pd

# Maximum number of history states to keep
MAX_HISTORY_SIZE = 10


def initialize_session_state():
    """Initialize all required session state variables."""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'original_df' not in st.session_state:
        st.session_state.original_df = None
    if 'workflow' not in st.session_state:
        st.session_state.workflow = None
    if 'trained_models' not in st.session_state:
        st.session_state.trained_models = {}
    if 'model_results' not in st.session_state:
        st.session_state.model_results = None
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = None
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'history_descriptions' not in st.session_state:
        st.session_state.history_descriptions = []


def reset_session_state():
    """Reset all session state variables."""
    st.session_state.df = None
    st.session_state.original_df = None
    st.session_state.workflow = None
    st.session_state.trained_models = {}
    st.session_state.model_results = None
    st.session_state.filtered_df = None
    st.session_state.history = []
    st.session_state.history_descriptions = []


def has_data():
    """Check if dataset is loaded."""
    return st.session_state.df is not None


def get_dataset():
    """Get the current dataset."""
    return st.session_state.df


def set_dataset(df):
    """Set the current dataset."""
    st.session_state.df = df
    if st.session_state.original_df is None:
        st.session_state.original_df = df.copy()


def save_state(description="Change"):
    """
    Save current dataset state to history.
    
    Args:
        description: Description of the change being made
    """
    if st.session_state.df is not None:
        # Create a deep copy of the current dataframe
        current_state = st.session_state.df.copy()
        
        # Add to history
        st.session_state.history.append(current_state)
        st.session_state.history_descriptions.append(description)
        
        # Limit history size to prevent memory issues
        if len(st.session_state.history) > MAX_HISTORY_SIZE:
            st.session_state.history.pop(0)
            st.session_state.history_descriptions.pop(0)


def undo():
    """Undo the last change by restoring previous state."""
    if can_undo():
        # Restore previous state
        st.session_state.df = st.session_state.history.pop()
        last_action = st.session_state.history_descriptions.pop()
        return True, last_action
    return False, None


def can_undo():
    """Check if undo is available."""
    return len(st.session_state.history) > 0


def get_history_count():
    """Get number of available undo states."""
    return len(st.session_state.history)


def get_last_action():
    """Get description of the last action."""
    if st.session_state.history_descriptions:
        return st.session_state.history_descriptions[-1]
    return None
