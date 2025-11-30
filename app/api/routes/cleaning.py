"""
Data cleaning API routes
"""
from fastapi import APIRouter, HTTPException, status
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

from app.api.session import session_manager
from app.api.schemas import (
    NullHandlingRequest,
    DuplicateHandlingRequest,
    DataTypeConversionRequest,
    EncodingRequest,
    FilterRequest,
    ColumnManagementRequest
)
from app.api.responses import CleaningResponse, CleaningStats, DatasetInfo
from app.api.routes.upload import get_dataset_info

router = APIRouter()


@router.post("/nulls", response_model=CleaningResponse)
async def handle_nulls(request: NullHandlingRequest):
    """Handle null values in dataset"""
    
    df = session_manager.get_dataframe(request.session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    initial_nulls = df.isnull().sum().sum()
    
    try:
        if request.operation == "remove":
            # Remove rows with nulls
            if request.columns:
                df = df.dropna(subset=request.columns)
            else:
                df = df.dropna()
        
        elif request.operation == "fill":
            # Fill null values
            if not request.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Columns must be specified for fill operation"
                )
            
            for col in request.columns:
                if col not in df.columns:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Column '{col}' not found in dataset"
                    )
                
                if request.fill_method == "mean":
                    if df[col].dtype not in ['int64', 'float64']:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Mean can only be used for numeric columns. '{col}' is {df[col].dtype}"
                        )
                    df[col] = df[col].fillna(df[col].mean())
                
                elif request.fill_method == "median":
                    if df[col].dtype not in ['int64', 'float64']:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Median can only be used for numeric columns. '{col}' is {df[col].dtype}"
                        )
                    df[col] = df[col].fillna(df[col].median())
                
                elif request.fill_method == "mode":
                    mode_val = df[col].mode()
                    if len(mode_val) > 0:
                        df[col] = df[col].fillna(mode_val[0])
                
                elif request.fill_method == "ffill":
                    df[col] = df[col].ffill()
                
                elif request.fill_method == "bfill":
                    df[col] = df[col].bfill()
                
                elif request.fill_method == "custom":
                    if request.custom_value is None:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Custom value must be provided for custom fill method"
                        )
                    df[col] = df[col].fillna(request.custom_value)
        
        # Update session
        session_manager.set_dataframe(request.session_id, df, keep_original=False)
        
        final_nulls = df.isnull().sum().sum()
        
        return CleaningResponse(
            success=True,
            message=f"Handled {initial_nulls - final_nulls} null values",
            stats=CleaningStats(
                missing_values_fixed=int(initial_nulls - final_nulls),
                duplicates_removed=0,
                columns_encoded=0,
                rows_filtered=0
            ),
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error handling nulls: {str(e)}"
        )


@router.post("/duplicates", response_model=CleaningResponse)
async def handle_duplicates(request: DuplicateHandlingRequest):
    """Handle duplicate rows in dataset"""
    
    df = session_manager.get_dataframe(request.session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    initial_rows = len(df)
    
    try:
        if request.columns:
            df = df.drop_duplicates(subset=request.columns)
        else:
            df = df.drop_duplicates()
        
        # Update session
        session_manager.set_dataframe(request.session_id, df, keep_original=False)
        
        duplicates_removed = initial_rows - len(df)
        
        return CleaningResponse(
            success=True,
            message=f"Removed {duplicates_removed} duplicate rows",
            stats=CleaningStats(
                missing_values_fixed=0,
                duplicates_removed=duplicates_removed,
                columns_encoded=0,
                rows_filtered=0
            ),
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error handling duplicates: {str(e)}"
        )


@router.post("/convert-type", response_model=CleaningResponse)
async def convert_data_type(request: DataTypeConversionRequest):
    """Convert column data type"""
    
    df = session_manager.get_dataframe(request.session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    if request.column not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Column '{request.column}' not found in dataset"
        )
    
    try:
        if request.target_type.value == "datetime64[ns]":
            df[request.column] = pd.to_datetime(df[request.column], errors='coerce')
        elif request.target_type.value in ["int64", "float64"]:
            # Clean numeric data
            def clean_numeric(val):
                import re
                if pd.isna(val):
                    return np.nan
                val_str = str(val).strip()
                
                # Remove currency symbols and separators
                val_str = val_str.replace('₹', '').replace('$', '').replace('€', '').replace('£', '')
                val_str = val_str.replace(',', '').strip()
                
                try:
                    return float(val_str)
                except ValueError:
                    pass
                
                # Extract numeric parts
                numeric_match = re.search(r'-?\d+\.?\d*', val_str)
                if numeric_match:
                    try:
                        return float(numeric_match.group())
                    except ValueError:
                        return np.nan
                
                return np.nan
            
            df[request.column] = df[request.column].apply(clean_numeric)
            df[request.column] = df[request.column].astype(request.target_type.value)
        else:
            df[request.column] = df[request.column].astype(request.target_type.value)
        
        # Update session
        session_manager.set_dataframe(request.session_id, df, keep_original=False)
        
        return CleaningResponse(
            success=True,
            message=f"Converted '{request.column}' to {request.target_type.value}",
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting data type: {str(e)}"
        )




@router.post("/encode", response_model=CleaningResponse)
async def encode_columns(request: EncodingRequest):
    """Encode categorical columns"""
    
    df = session_manager.get_dataframe(request.session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    # Validate columns
    for col in request.columns:
        if col not in df.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Column '{col}' not found in dataset"
            )
    
    try:
        if request.encoding_type.value == "label":
            for col in request.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
        
        elif request.encoding_type.value == "onehot":
            df = pd.get_dummies(df, columns=request.columns, drop_first=False)
        
        elif request.encoding_type.value == "ordinal":
            oe = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
            df[request.columns] = oe.fit_transform(df[request.columns])
        
        # Update session
        session_manager.set_dataframe(request.session_id, df, keep_original=False)
        
        return CleaningResponse(
            success=True,
            message=f"Applied {request.encoding_type.value} encoding to {len(request.columns)} column(s)",
            stats=CleaningStats(
                missing_values_fixed=0,
                duplicates_removed=0,
                columns_encoded=len(request.columns),
                rows_filtered=0
            ),
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error encoding columns: {str(e)}"
        )


@router.post("/filter", response_model=CleaningResponse)
async def filter_data(request: FilterRequest):
    """Filter dataset based on conditions"""
    
    df = session_manager.get_dataframe(request.session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    if request.column not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Column '{request.column}' not found in dataset"
        )
    
    initial_rows = len(df)
    
    try:
        if request.filter_type.value == "range":
            if request.min_value is None or request.max_value is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="min_value and max_value required for range filter"
                )
            df = df[(df[request.column] >= request.min_value) & (df[request.column] <= request.max_value)]
        
        elif request.filter_type.value == "gt":
            if request.value is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="value required for greater than filter"
                )
            df = df[df[request.column] > request.value]
        
        elif request.filter_type.value == "lt":
            if request.value is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="value required for less than filter"
                )
            df = df[df[request.column] < request.value]
        
        elif request.filter_type.value == "eq":
            if request.value is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="value required for equal to filter"
                )
            df = df[df[request.column] == request.value]
        
        elif request.filter_type.value == "in":
            if not request.values:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="values required for 'in' filter"
                )
            df = df[df[request.column].isin(request.values)]
        
        # Update session
        session_manager.set_dataframe(request.session_id, df, keep_original=False)
        
        rows_filtered = initial_rows - len(df)
        
        return CleaningResponse(
            success=True,
            message=f"Filtered dataset: {rows_filtered} rows removed",
            stats=CleaningStats(
                missing_values_fixed=0,
                duplicates_removed=0,
                columns_encoded=0,
                rows_filtered=rows_filtered
            ),
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error filtering data: {str(e)}"
        )


@router.post("/columns", response_model=CleaningResponse)
async def manage_columns(request: ColumnManagementRequest):
    """Drop or rename columns"""
    
    df = session_manager.get_dataframe(request.session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    try:
        if request.operation == "drop":
            if not request.columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="columns required for drop operation"
                )
            
            # Validate columns exist
            for col in request.columns:
                if col not in df.columns:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Column '{col}' not found in dataset"
                    )
            
            df = df.drop(columns=request.columns)
            message = f"Dropped {len(request.columns)} column(s)"
        
        elif request.operation == "rename":
            if not request.rename_mapping:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="rename_mapping required for rename operation"
                )
            
            # Validate columns exist
            for old_name in request.rename_mapping.keys():
                if old_name not in df.columns:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Column '{old_name}' not found in dataset"
                    )
            
            df = df.rename(columns=request.rename_mapping)
            message = f"Renamed {len(request.rename_mapping)} column(s)"
        
        # Update session
        session_manager.set_dataframe(request.session_id, df, keep_original=False)
        
        return CleaningResponse(
            success=True,
            message=message,
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error managing columns: {str(e)}"
        )


@router.post("/undo", response_model=CleaningResponse)
async def undo_operation(session_id: str):
    """Undo the last operation"""
    
    if not session_manager.can_undo(session_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No operations to undo"
        )
    
    try:
        df = session_manager.undo(session_id)
        if df is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to undo operation"
            )
        
        return CleaningResponse(
            success=True,
            message="Operation undone successfully",
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error undoing operation: {str(e)}"
        )


@router.post("/redo", response_model=CleaningResponse)
async def redo_operation(session_id: str):
    """Redo the last undone operation"""
    
    if not session_manager.can_redo(session_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No operations to redo"
        )
    
    try:
        df = session_manager.redo(session_id)
        if df is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to redo operation"
            )
        
        return CleaningResponse(
            success=True,
            message="Operation redone successfully",
            dataset_info=get_dataset_info(df)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error redoing operation: {str(e)}"
        )


@router.get("/history-status")
async def get_history_status(session_id: str):
    """Get the current undo/redo availability status"""
    
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    return {
        "can_undo": session_manager.can_undo(session_id),
        "can_redo": session_manager.can_redo(session_id)
    }
