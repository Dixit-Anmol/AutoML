/**
 * API Type Definitions
 */

export interface DatasetInfo {
    rows: number;
    columns: number;
    total_nulls: number;
    total_duplicates: number;
    memory_mb: number;
    column_types: Record<string, string>;
}

export interface DatasetPreview {
    info: DatasetInfo;
    head: Record<string, any>[];
    description?: Record<string, any>;
}

export interface CleaningStats {
    missing_values_fixed: number;
    duplicates_removed: number;
    columns_encoded: number;
    rows_filtered: number;
}

export interface UploadResponse {
    session_id: string;
    filename: string;
    file_size_mb: number;
    dataset_info: DatasetInfo;
    message: string;
}

export interface CleaningResponse {
    success: boolean;
    message: string;
    stats?: CleaningStats;
    dataset_info: DatasetInfo;
}

export interface ModelMetrics {
    model_name: string;
    // Classification metrics
    accuracy?: number;
    precision?: number;
    recall?: number;
    f1_score?: number;
    // Regression metrics
    mse?: number;
    rmse?: number;
    mae?: number;
    r2_score?: number;
}

export interface TrainingResponse {
    success: boolean;
    message: string;
    problem_type: string;
    models_trained: number;
    results: ModelMetrics[];
    best_model: string;
    training_time_seconds: number;
}

export interface TrainingStatus {
    session_id: string;
    status: "idle" | "training" | "completed" | "failed";
    progress: number;
    current_model?: string;
    message?: string;
}

export type FillMethod = "mean" | "median" | "mode" | "ffill" | "bfill" | "custom";
export type EncodingType = "label" | "onehot" | "ordinal";
export type FilterType = "range" | "gt" | "lt" | "eq" | "in";
export type ProblemType = "classification" | "regression";
