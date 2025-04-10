#!/usr/bin/env python
"""
Prototype for a machine learning model to score user behavior.
"""
import os
import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Add the project root to the path so we can import Django settings
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'humanauth.settings')

import django
django.setup()


def train_scoring_model(dataset_path):
    """
    Train a machine learning model to predict if a session is human or bot.
    """
    # Load dataset
    df = pd.read_csv(dataset_path)
    
    if df.empty:
        print("Dataset is empty.")
        return
    
    print(f"Loaded dataset with {len(df)} records.")
    
    # Feature selection
    feature_columns = [
        'time_taken_ms', 'entropy_score', 
        'mouse_speed_mean', 'mouse_speed_std', 'mouse_speed_max', 'mouse_movements_count',
        'mouse_angle_change_mean', 'mouse_angle_change_std', 'mouse_angle_change_max',
        'keystroke_interval_mean', 'keystroke_interval_std', 'keystroke_count'
    ]
    
    # Filter to only include columns that exist in the dataset
    feature_columns = [col for col in feature_columns if col in df.columns]
    
    if not feature_columns:
        print("No valid feature columns found in dataset.")
        return
    
    # Target variable
    target = 'passed'
    
    # Drop rows with missing target
    df = df.dropna(subset=[target])
    
    # Prepare features and target
    X = df[feature_columns]
    y = df[target]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Create pipeline with preprocessing and model
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),  # Handle missing values
        ('scaler', StandardScaler()),  # Standardize features
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Train model
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate model
    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    if hasattr(pipeline['classifier'], 'feature_importances_'):
        importances = pipeline['classifier'].feature_importances_
        indices = np.argsort(importances)[::-1]
        
        print("\nFeature Ranking:")
        for i, idx in enumerate(indices):
            if i < len(feature_columns):
                print(f"{i+1}. {feature_columns[idx]} ({importances[idx]:.4f})")
    
    # Save model
    from joblib import dump
    output_dir = Path(settings.BASE_DIR) / 'scripts' / 'models'
    output_dir.mkdir(exist_ok=True, parents=True)
    
    model_path = output_dir / 'trust_score_model.joblib'
    dump(pipeline, model_path)
    print(f"\nModel saved to {model_path}")


if __name__ == "__main__":
    # Check if dataset path is provided
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
    else:
        # Use the most recent dataset if available
        datasets_dir = Path(settings.BASE_DIR) / 'scripts' / 'datasets'
        if datasets_dir.exists():
            datasets = list(datasets_dir.glob('*.csv'))
            if datasets:
                dataset_path = str(sorted(datasets)[-1])  # Most recent file
            else:
                print("No datasets found. Please generate a dataset first.")
                sys.exit(1)
        else:
            print("Datasets directory not found. Please generate a dataset first.")
            sys.exit(1)
    
    print(f"Using dataset: {dataset_path}")
    train_scoring_model(dataset_path)
