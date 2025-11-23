"""
Pydantic models for API request validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum


class FillMethod(str, Enum):
    """Fill methods for null values"""
    MEAN = "mean"
    MEDIAN = "median"
    MODE = "mode"
    FORWARD_FILL = "ffill"
    BACKWARD_FILL = "bfill"
    CUSTOM = "custom"


class EncodingType(str, Enum):
    """Encoding types for categorical data"""
    LABEL = "label"
    ONEHOT = "onehot"
    ORDINAL = "ordinal"


class DataType(str, Enum):
    """Data types for conversion"""
    INT64 = "int64"
    FLOAT64 = "float64"
    OBJECT = "object"
    BOOL = "bool"
    DATETIME = "datetime64[ns]"


class FilterType(str, Enum):
    """Filter types for data filtering"""
    RANGE = "range"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    EQUAL_TO = "eq"
    IN = "in"


class NullHandlingRequest(BaseModel):
    """Request for handling null values"""
    session_id: str
    operation: Literal["remove", "fill"]
    columns: Optional[List[str]] = None  # None means all columns
    fill_method: Optional[FillMethod] = None
    custom_value: Optional[str] = None


class DuplicateHandlingRequest(BaseModel):
    """Request for handling duplicates"""
    session_id: str
    operation: Literal["remove"]
    columns: Optional[List[str]] = None  # None means all columns


class DataTypeConversionRequest(BaseModel):
    """Request for data type conversion"""
    session_id: str
    column: str
    target_type: DataType


class EncodingRequest(BaseModel):
    """Request for encoding categorical data"""
    session_id: str
    columns: List[str]
    encoding_type: EncodingType


class FilterRequest(BaseModel):
    """Request for filtering data"""
    session_id: str
    column: str
    filter_type: FilterType
    value: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    values: Optional[List[str]] = None  # For 'in' filter


class ColumnManagementRequest(BaseModel):
    """Request for column management"""
    session_id: str
    operation: Literal["drop", "rename"]
    columns: Optional[List[str]] = None
    rename_mapping: Optional[dict] = None


class TrainingConfigRequest(BaseModel):
    """Request for model training configuration"""
    session_id: str
    target_column: str
    problem_type: Literal["classification", "regression"]
    test_size: float = Field(default=0.2, ge=0.1, le=0.5)
    models: Optional[List[str]] = None  # None means train all available models
