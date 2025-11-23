"""
Pydantic models for API responses
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class DatasetInfo(BaseModel):
    """Dataset information response"""
    rows: int
    columns: int
    total_nulls: int
    total_duplicates: int
    memory_mb: float
    column_types: Dict[str, str]


class DatasetPreview(BaseModel):
    """Dataset preview response"""
    info: DatasetInfo
    head: List[Dict[str, Any]]
    description: Optional[Dict[str, Any]] = None


class CleaningStats(BaseModel):
    """Data cleaning statistics"""
    missing_values_fixed: int
    duplicates_removed: int
    columns_encoded: int
    rows_filtered: int


class UploadResponse(BaseModel):
    """File upload response"""
    session_id: str
    filename: str
    file_size_mb: float
    dataset_info: DatasetInfo
    message: str


class CleaningResponse(BaseModel):
    """Data cleaning operation response"""
    success: bool
    message: str
    stats: Optional[CleaningStats] = None
    dataset_info: DatasetInfo


class ModelMetrics(BaseModel):
    """Model performance metrics"""
    model_name: str
    
    # Classification metrics
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    
    # Regression metrics
    mse: Optional[float] = None
    rmse: Optional[float] = None
    mae: Optional[float] = None
    r2_score: Optional[float] = None


class TrainingResponse(BaseModel):
    """Model training response"""
    success: bool
    message: str
    problem_type: str
    models_trained: int
    results: List[ModelMetrics]
    best_model: str
    training_time_seconds: float


class TrainingStatusResponse(BaseModel):
    """Training status response"""
    session_id: str
    status: str  # "idle", "training", "completed", "failed"
    progress: float  # 0.0 to 1.0
    current_model: Optional[str] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: str
    timestamp: datetime = datetime.now()


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool
    message: str
    data: Optional[Any] = None
