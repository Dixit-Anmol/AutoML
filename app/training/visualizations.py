"""
Training Visualizations Module
"""
import streamlit as st
import plotly.graph_objects as go


def render_visualizations():
    """Render training visualizations."""
    st.subheader("📈 Training Visualizations")
    
    viz_col1, viz_col2 = st.columns(2)
    
    problem_type = st.session_state.get('problem_type')
    
    with viz_col1:
        st.write("**Model Performance Comparison**")
        if problem_type == "Classification":
            render_classification_performance_chart()
        else:
            render_regression_performance_chart()
    
    with viz_col2:
        st.write("**Error Metrics Comparison**")
        if problem_type == "Classification":
            render_classification_error_chart()
        else:
            render_regression_error_chart()
    
    # Model Ranking
    render_model_ranking()


def render_classification_performance_chart():
    """Render classification performance chart (Accuracy)."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=st.session_state.model_results['Model'],
        y=st.session_state.model_results['Accuracy'],
        marker_color='#1f77b4'
    ))
    fig.update_layout(title="Accuracy Comparison", height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_classification_error_chart():
    """Render classification error chart (F1-Score)."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=st.session_state.model_results['Model'],
        y=st.session_state.model_results['F1-Score'],
        marker_color='#ff7f0e'
    ))
    fig.update_layout(title="F1-Score Comparison", height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_regression_performance_chart():
    """Render regression performance chart (R² Score)."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=st.session_state.model_results['Model'],
        y=st.session_state.model_results['R² Score'],
        marker_color='#2ca02c'
    ))
    fig.update_layout(title="R² Score Comparison", height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_regression_error_chart():
    """Render regression error chart (RMSE)."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=st.session_state.model_results['Model'],
        y=st.session_state.model_results['RMSE'],
        marker_color='#d62728'
    ))
    fig.update_layout(title="RMSE Comparison", height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_model_ranking():
    """Render model ranking table."""
    st.subheader("📊 Model Ranking")
    
    problem_type = st.session_state.get('problem_type')
    
    if problem_type == "Classification":
        ranking_df = st.session_state.model_results[['Model', 'Accuracy']].sort_values(
            'Accuracy', ascending=False).reset_index(drop=True)
        ranking_df.index = ranking_df.index + 1
        ranking_df.index.name = 'Rank'
    else:
        ranking_df = st.session_state.model_results[['Model', 'R² Score']].sort_values(
            'R² Score', ascending=False).reset_index(drop=True)
        ranking_df.index = ranking_df.index + 1
        ranking_df.index.name = 'Rank'
    
    df = ranking_df.astype(str)
    st.dataframe(df, width='stretch')
