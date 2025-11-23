"""
File upload API routes
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
import pandas as pd
from pathlib import Path
import aiofiles
from io import BytesIO

from app.api.session import session_manager
from app.api.responses import UploadResponse, DatasetInfo

router = APIRouter()


def get_dataset_info(df: pd.DataFrame) -> DatasetInfo:
    """Extract dataset information"""
    return DatasetInfo(
        rows=int(df.shape[0]),
        columns=int(df.shape[1]),
        total_nulls=int(df.isnull().sum().sum()),
        total_duplicates=int(df.duplicated().sum()),
        memory_mb=float(df.memory_usage(deep=True).sum() / 1024 / 1024),
        column_types={col: str(dtype) for col, dtype in df.dtypes.items()}
    )


@router.post("/", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    """Upload a CSV or Excel file"""
    
    # Validate file type
    allowed_extensions = {'.csv', '.xlsx', '.xls'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {allowed_extensions}"
        )
    
    try:
        # Read file content
        content = await file.read()
        file_size_mb = len(content) / 1024 / 1024
        
        # Check file size (max 200MB)
        if file_size_mb > 200:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 200MB limit"
            )
        
        # Parse file based on extension
        if file_ext == '.csv':
            df = pd.read_csv(BytesIO(content))
        else:  # Excel
            df = pd.read_excel(BytesIO(content))
        
        # Create session
        session_id = session_manager.create_session()
        session_manager.set_dataframe(session_id, df, keep_original=True)
        
        # Save file
        file_path = session_manager.upload_dir / f"{session_id}_{file.filename}"
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Get dataset info
        dataset_info = get_dataset_info(df)
        
        return UploadResponse(
            session_id=session_id,
            filename=file.filename,
            file_size_mb=round(file_size_mb, 2),
            dataset_info=dataset_info,
            message="File uploaded successfully"
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/{session_id}/info", response_model=DatasetInfo)
async def get_dataset_info_endpoint(session_id: str):
    """Get dataset information for a session"""
    
    df = session_manager.get_dataframe(session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found or has no dataset"
        )
    
    return get_dataset_info(df)


@router.get("/{session_id}/preview")
async def get_dataset_preview(session_id: str, rows: int = 10):
    """Get dataset preview"""
    
    df = session_manager.get_dataframe(session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found or has no dataset"
        )
    
    # Get head of dataset
    head_data = df.head(rows).to_dict(orient='records')
    
    # Get dataset info
    info = get_dataset_info(df)
    
    # Get description
    description = df.describe().to_dict()
    
    return {
        "info": info,
        "head": head_data,
        "description": description
    }


@router.get("/{session_id}/download")
async def download_dataset(session_id: str, cleaned: bool = True):
    """Download the current dataset (original or cleaned)"""
    
    df = session_manager.get_dataframe(session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found or has no dataset"
        )
    
    # Save to temporary file
    output_dir = session_manager.cleaned_dir if cleaned else session_manager.upload_dir
    filename = f"{session_id}_{'cleaned' if cleaned else 'original'}.csv"
    file_path = output_dir / filename
    
    df.to_csv(file_path, index=False)
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )
