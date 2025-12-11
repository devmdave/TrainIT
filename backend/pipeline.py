"""
Training Pipeline
Coordinates data loading, preprocessing, and model training
"""

from backend.data_loader import DataLoader
from backend.model_trainer import ModelTrainer
import numpy as np


class TrainingPipeline:
    """Complete training pipeline for ML models"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.trainer = None
        self.X_train = None
        self.y_train = None
        self.X_val = None
        self.y_val = None
        self.X_test = None
        self.y_test = None
        self.train_data = None
        self.test_data = None
        
    def load_datasets(self, train_path, test_path=None, target_column=None, 
                     progress_callback=None, status_callback=None):
        """
        Load and preprocess datasets
        
        Args:
            train_path: Path to training dataset
            test_path: Path to test dataset (optional)
            target_column: Name of target column
            progress_callback: Callback for progress updates
            status_callback: Callback for status messages
            
        Returns:
            dict: Information about loaded datasets
        """
        try:
            if status_callback:
                status_callback("Loading training dataset...")
            
            # Load training data
            self.train_data = self.data_loader.load_data(train_path)
            
            if progress_callback:
                progress_callback(20)
            
            if status_callback:
                status_callback("Preprocessing training data...")
            
            # Preprocess training data
            X, y = self.data_loader.preprocess_data(self.train_data, target_column)
            
            if progress_callback:
                progress_callback(40)
            
            # Split training data into train and validation sets
            from sklearn.model_selection import train_test_split
            self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            if progress_callback:
                progress_callback(60)
            
            # Load test data if provided
            if test_path:
                if status_callback:
                    status_callback("Loading test dataset...")
                
                self.test_data = self.data_loader.load_data(test_path)
                
                if progress_callback:
                    progress_callback(80)
                
                if status_callback:
                    status_callback("Preprocessing test data...")
                
                # Preprocess test data
                self.X_test, self.y_test = self.data_loader.preprocess_data(
                    self.test_data, target_column
                )
            
            if progress_callback:
                progress_callback(100)
            
            if status_callback:
                status_callback("Data loading completed!")
            
            # Return dataset information
            info = {
                'train_samples': len(self.X_train),
                'val_samples': len(self.X_val),
                'test_samples': len(self.X_test) if self.X_test is not None else 0,
                'n_features': self.X_train.shape[1],
                'feature_names': self.data_loader.feature_names,
                'target_name': self.data_loader.target_name,
                'n_classes': len(np.unique(self.y_train))
            }
            
            return info
            
        except Exception as e:
            if status_callback:
                status_callback(f"Error loading data: {str(e)}")
            raise
    
    def train_model(self, algorithm='Random Forest', epochs=10, batch_size=32,
                   learning_rate=0.001, auto_tune=False,
                   progress_callback=None, status_callback=None):
        """
        Train a machine learning model
        
        Args:
            algorithm: ML algorithm to use
            epochs: Number of training iterations
            batch_size: Batch size for training
            learning_rate: Learning rate
            auto_tune: Whether to perform hyperparameter tuning
            progress_callback: Callback for progress updates
            status_callback: Callback for status messages
            
        Returns:
            dict: Training results
        """
        if self.X_train is None or self.y_train is None:
            raise ValueError("No training data loaded. Please load datasets first.")
        
        try:
            # Initialize trainer
            self.trainer = ModelTrainer(algorithm=algorithm, auto_tune=auto_tune)
            
            if status_callback:
                status_callback(f"Starting {algorithm} training...")
            
            # Train model
            results = self.trainer.train(
                self.X_train, self.y_train,
                self.X_val, self.y_val,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate,
                progress_callback=progress_callback,
                status_callback=status_callback
            )
            
            # Evaluate on test set if available
            if self.X_test is not None and self.y_test is not None:
                if status_callback:
                    status_callback("Evaluating on test set...")
                
                test_results = self.evaluate_on_test()
                results['test_metrics'] = test_results
            
            return results
            
        except Exception as e:
            if status_callback:
                status_callback(f"Training error: {str(e)}")
            raise
    
    def evaluate_on_test(self):
        """Evaluate model on test set"""
        if self.trainer is None or self.trainer.model is None:
            raise ValueError("No trained model available")
        
        if self.X_test is None or self.y_test is None:
            raise ValueError("No test data available")
        
        from sklearn.metrics import (accuracy_score, precision_score, 
                                    recall_score, f1_score, confusion_matrix)
        
        y_pred = self.trainer.predict(self.X_test)
        
        results = {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(self.y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(self.y_test, y_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(self.y_test, y_pred).tolist()
        }
        
        return results
    
    def save_model(self, filepath):
        """Save trained model and preprocessing objects"""
        if self.trainer is None or self.trainer.model is None:
            raise ValueError("No trained model to save")
        
        import joblib
        
        model_data = {
            'model': self.trainer.model,
            'algorithm': self.trainer.algorithm,
            'best_params': self.trainer.best_params,
            'scaler': self.data_loader.scaler,
            'label_encoders': self.data_loader.label_encoders,
            'feature_names': self.data_loader.feature_names,
            'target_name': self.data_loader.target_name
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath):
        """Load a saved model and preprocessing objects"""
        import joblib
        
        model_data = joblib.load(filepath)
        
        self.trainer = ModelTrainer(algorithm=model_data['algorithm'])
        self.trainer.model = model_data['model']
        self.trainer.best_params = model_data.get('best_params')
        
        self.data_loader.scaler = model_data['scaler']
        self.data_loader.label_encoders = model_data['label_encoders']
        self.data_loader.feature_names = model_data['feature_names']
        self.data_loader.target_name = model_data['target_name']
    
    def predict(self, X):
        """Make predictions on new data"""
        if self.trainer is None or self.trainer.model is None:
            raise ValueError("No trained model available")
        
        return self.trainer.predict(X)
    
    def stop_training(self):
        """Stop the training process"""
        if self.trainer:
            self.trainer.stop_training()
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if self.trainer is None or self.trainer.model is None:
            raise ValueError("No trained model available")
        
        model = self.trainer.model
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            feature_importance = dict(zip(self.data_loader.feature_names, importances))
            return sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        else:
            return None
