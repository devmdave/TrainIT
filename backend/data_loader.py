"""
Data Loader Module
Handles loading and preprocessing of datasets
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import json


class DataLoader:
    """Handles dataset loading and preprocessing"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.target_name = None
        
    def load_data(self, file_path):
        """
        Load data from various file formats
        
        Args:
            file_path: Path to the data file
            
        Returns:
            DataFrame: Loaded data
        """
        file_extension = file_path.lower().split('.')[-1]
        
        try:
            if file_extension == 'csv':
                data = pd.read_csv(file_path)
            elif file_extension in ['xlsx', 'xls']:
                data = pd.read_excel(file_path)
            elif file_extension == 'json':
                data = pd.read_json(file_path)
            elif file_extension == 'parquet':
                data = pd.read_parquet(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            return data
        except Exception as e:
            raise Exception(f"Error loading data from {file_path}: {str(e)}")
    
    def preprocess_data(self, data, target_column=None):
        """
        Preprocess the data for training
        
        Args:
            data: DataFrame containing the data
            target_column: Name of the target column (if None, assumes last column)
            
        Returns:
            tuple: (X, y) preprocessed features and target
        """
        if data is None or data.empty:
            raise ValueError("Data is empty or None")
        
        # Handle missing values
        data = self.handle_missing_values(data)
        
        # Determine target column
        if target_column is None:
            target_column = data.columns[-1]
        
        self.target_name = target_column
        
        # Separate features and target
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        self.feature_names = X.columns.tolist()
        
        # Encode categorical variables
        X = self.encode_categorical_features(X)
        y = self.encode_target(y)
        
        # Scale numerical features
        X = self.scale_features(X)
        
        return X, y
    
    def handle_missing_values(self, data):
        """Handle missing values in the dataset"""
        # For numerical columns, fill with median
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if data[col].isnull().any():
                data[col].fillna(data[col].median(), inplace=True)
        
        # For categorical columns, fill with mode
        categorical_cols = data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if data[col].isnull().any():
                data[col].fillna(data[col].mode()[0] if not data[col].mode().empty else 'Unknown', inplace=True)
        
        return data
    
    def encode_categorical_features(self, X):
        """Encode categorical features"""
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
        
        return X
    
    def encode_target(self, y):
        """Encode target variable if categorical"""
        if y.dtype == 'object' or y.dtype.name == 'category':
            le = LabelEncoder()
            y = le.fit_transform(y)
            self.label_encoders['target'] = le
        
        return y
    
    def scale_features(self, X):
        """Scale features using StandardScaler"""
        X_scaled = self.scaler.fit_transform(X)
        return pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    def get_data_info(self, data):
        """Get information about the dataset"""
        info = {
            'shape': data.shape,
            'columns': data.columns.tolist(),
            'dtypes': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'numerical_columns': data.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': data.select_dtypes(include=['object']).columns.tolist(),
        }
        return info
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into training and validation sets"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
