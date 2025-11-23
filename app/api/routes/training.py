"""
Model training API routes
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
import pandas as pd
import numpy as np
from pathlib import Path
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, mean_absolute_error
)

from app.api.session import session_manager
from app.api.schemas import TrainingConfigRequest
from app.api.responses import (
    TrainingResponse,
    TrainingStatusResponse,
    ModelMetrics
)

router = APIRouter()


def train_models_background(session_id: str, config: TrainingConfigRequest, models_dir: Path):
    """Background task for training models"""
    
    session_manager.set_training_status(session_id, "training", progress=0.0, current_model=None)
    
    try:
        # Get dataframe
        df = session_manager.get_dataframe(session_id)
        if df is None:
            session_manager.set_training_status(
                session_id, "failed",
                error_message="Dataset not found"
            )
            return
        
        # Prepare data
        X = df.drop(columns=[config.target_column])
        y = df[config.target_column]
        
        # Check for non-numeric columns
        non_numeric_cols = X.select_dtypes(include=['object']).columns.tolist()
        if non_numeric_cols:
            session_manager.set_training_status(
                session_id, "failed",
                error_message=f"Non-numeric columns found: {non_numeric_cols}. Please encode them first."
            )
            return
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=config.test_size, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Store test data
        session = session_manager.get_session(session_id)
        session["X_test_scaled"] = X_test_scaled
        session["y_test"] = y_test
        session["scaler"] = scaler
        
        results = []
        start_time = time.time()
        
        if config.problem_type == "classification":
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
                "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
                "Decision Tree": DecisionTreeClassifier(random_state=42),
                "SVM": SVC(kernel='rbf', random_state=42)
            }
            
            for idx, (name, model) in enumerate(models.items()):
                session_manager.set_training_status(
                    session_id, "training",
                    progress=(idx + 0.5) / len(models),
                    current_model=name
                )
                
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
                
                results.append(ModelMetrics(
                    model_name=name,
                    accuracy=round(float(accuracy), 4),
                    precision=round(float(precision), 4),
                    recall=round(float(recall), 4),
                    f1_score=round(float(f1), 4)
                ))
                
                # Save model
                session_manager.save_model(session_id, name, model, models_dir)
                
                session_manager.set_training_status(
                    session_id, "training",
                    progress=(idx + 1) / len(models),
                    current_model=name
                )
        
        else:  # Regression
            models = {
                "Linear Regression": LinearRegression(),
                "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "SVM": SVR(kernel='rbf'),
                "XGBoost": XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
            }
            
            for idx, (name, model) in enumerate(models.items()):
                session_manager.set_training_status(
                    session_id, "training",
                    progress=(idx + 0.5) / len(models),
                    current_model=name
                )
                
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                results.append(ModelMetrics(
                    model_name=name,
                    mse=round(float(mse), 4),
                    rmse=round(float(rmse), 4),
                    mae=round(float(mae), 4),
                    r2_score=round(float(r2), 4)
                ))
                
                # Save model
                session_manager.save_model(session_id, name, model, models_dir)
                
                session_manager.set_training_status(
                    session_id, "training",
                    progress=(idx + 1) / len(models),
                    current_model=name
                )
        
        training_time = time.time() - start_time
        
        # Find best model
        if config.problem_type == "classification":
            best_model = max(results, key=lambda x: x.accuracy).model_name
        else:
            best_model = min(results, key=lambda x: x.mse).model_name
        
        # Store results
        session_manager.set_training_status(
            session_id, "completed",
            progress=1.0,
            training_results={
                "success": True,
                "message": "Models trained successfully",
                "problem_type": config.problem_type,
                "models_trained": len(results),
                "results": [r.dict() for r in results],
                "best_model": best_model,
                "training_time_seconds": round(training_time, 2)
            }
        )
        
    except Exception as e:
        session_manager.set_training_status(
            session_id, "failed",
            error_message=str(e)
        )


@router.post("/train", response_model=TrainingStatusResponse)
async def start_training(config: TrainingConfigRequest, background_tasks: BackgroundTasks):
    """Start model training in background"""
    
    df = session_manager.get_dataframe(config.session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {config.session_id} not found"
        )
    
    if config.target_column not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Target column '{config.target_column}' not found in dataset"
        )
    
    # Get models directory from environment
    import os
    models_dir = Path(os.getenv("MODELS_DIR", "./models"))
    
    # Start training in background
    background_tasks.add_task(train_models_background, config.session_id, config, models_dir)
    
    return TrainingStatusResponse(
        session_id=config.session_id,
        status="training",
        progress=0.0,
        message="Training started"
    )


@router.get("/status/{session_id}", response_model=TrainingStatusResponse)
async def get_training_status(session_id: str):
    """Get training status"""
    
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    return TrainingStatusResponse(
        session_id=session_id,
        status=session.get("training_status", "idle"),
        progress=session.get("progress", 0.0),
        current_model=session.get("current_model"),
        message=session.get("error_message", "")
    )


@router.get("/results/{session_id}", response_model=TrainingResponse)
async def get_training_results(session_id: str):
    """Get training results"""
    
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    training_results = session.get("training_results")
    if not training_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No training results found. Please train models first."
        )
    
    # Convert dict results back to ModelMetrics objects
    results = [ModelMetrics(**r) for r in training_results["results"]]
    
    return TrainingResponse(
        success=training_results["success"],
        message=training_results["message"],
        problem_type=training_results["problem_type"],
        models_trained=training_results["models_trained"],
        results=results,
        best_model=training_results["best_model"],
        training_time_seconds=training_results["training_time_seconds"]
    )
