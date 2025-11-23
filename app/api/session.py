"""
Session management service for storing datasets and state
"""
import uuid
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import pickle
import os


class SessionManager:
    """Manages user sessions and dataset storage"""
    
    def __init__(self, upload_dir: str = "./data/uploads", cleaned_dir: str = "./data/cleaned"):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.upload_dir = Path(upload_dir)
        self.cleaned_dir = Path(cleaned_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.cleaned_dir.mkdir(parents=True, exist_ok=True)
        
    def create_session(self) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
            "df": None,
            "original_df": None,
            "training_status": "idle",
            "trained_models": {},
            "training_results": None
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        session = self.sessions.get(session_id)
        if session:
            session["last_accessed"] = datetime.now()
        return session
    
    def set_dataframe(self, session_id: str, df: pd.DataFrame, keep_original: bool = True):
        """Store dataframe in session"""
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        
        session["df"] = df.copy()
        if keep_original and session["original_df"] is None:
            session["original_df"] = df.copy()
    
    def get_dataframe(self, session_id: str) -> Optional[pd.DataFrame]:
        """Get dataframe from session"""
        session = self.get_session(session_id)
        if session and session["df"] is not None:
            return session["df"].copy()
        return None
    
    def save_file(self, session_id: str, file_path: Path, file_type: str = "upload") -> Path:
        """Save uploaded or cleaned file"""
        target_dir = self.upload_dir if file_type == "upload" else self.cleaned_dir
        target_path = target_dir / f"{session_id}_{file_path.name}"
        return target_path
    
    def cleanup_old_sessions(self, hours: int = 24):
        """Remove sessions older than specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if session["last_accessed"] < cutoff
        ]
        
        for sid in expired_sessions:
            # Clean up files
            for file in self.upload_dir.glob(f"{sid}_*"):
                file.unlink()
            for file in self.cleaned_dir.glob(f"{sid}_*"):
                file.unlink()
            
            # Remove session
            del self.sessions[sid]
        
        return len(expired_sessions)
    
    def set_training_status(self, session_id: str, status: str, **kwargs):
        """Update training status"""
        session = self.get_session(session_id)
        if session:
            session["training_status"] = status
            for key, value in kwargs.items():
                session[key] = value
    
    def save_model(self, session_id: str, model_name: str, model: Any, model_dir: Path):
        """Save trained model"""
        model_path = model_dir / f"{session_id}_{model_name}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        session = self.get_session(session_id)
        if session:
            if "model_paths" not in session:
                session["model_paths"] = {}
            session["model_paths"][model_name] = str(model_path)
        
        return model_path


# Global session manager instance
session_manager = SessionManager()
