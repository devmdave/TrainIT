"""
Model Trainer Module
Handles model training with various algorithms
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, confusion_matrix, classification_report)
import joblib
import time


class ModelTrainer:
    """Handles model training and evaluation"""
    
    def __init__(self, algorithm='Random Forest', auto_tune=False):
        self.algorithm = algorithm
        self.auto_tune = auto_tune
        self.model = None
        self.best_params = None
        self.training_history = []
        self.is_training = False
        
    def get_model(self, **params):
        """Get model instance based on algorithm"""
        models = {
            'Random Forest': RandomForestClassifier(random_state=42, **params),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42, **params),
            'Neural Network': MLPClassifier(random_state=42, max_iter=1000, **params),
            'Support Vector Machine': SVC(random_state=42, **params),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000, **params),
            'Decision Tree': DecisionTreeClassifier(random_state=42, **params)
        }
        
        return models.get(self.algorithm, RandomForestClassifier(random_state=42))
    
    def get_param_grid(self):
        """Get hyperparameter grid for tuning"""
        param_grids = {
            'Random Forest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10]
            },
            'Gradient Boosting': {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.3],
                'max_depth': [3, 5, 7]
            },
            'Neural Network': {
                'hidden_layer_sizes': [(50,), (100,), (50, 50)],
                'activation': ['relu', 'tanh'],
                'alpha': [0.0001, 0.001, 0.01]
            },
            'Support Vector Machine': {
                'C': [0.1, 1, 10],
                'kernel': ['rbf', 'linear'],
                'gamma': ['scale', 'auto']
            },
            'Logistic Regression': {
                'C': [0.1, 1, 10],
                'penalty': ['l2'],
                'solver': ['lbfgs', 'liblinear']
            },
            'Decision Tree': {
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        }
        
        return param_grids.get(self.algorithm, {})
    
    def train(self, X_train, y_train, X_val=None, y_val=None, 
              epochs=10, batch_size=32, learning_rate=0.001, 
              progress_callback=None, status_callback=None):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            epochs: Number of training iterations
            batch_size: Batch size for training
            learning_rate: Learning rate
            progress_callback: Callback for progress updates
            status_callback: Callback for status messages
            
        Returns:
            dict: Training results
        """
        self.is_training = True
        start_time = time.time()
        
        if status_callback:
            status_callback("Initializing model...")
        
        # Get model parameters
        params = {}
        if self.algorithm == 'Neural Network':
            params['learning_rate_init'] = learning_rate
        
        if self.auto_tune:
            if status_callback:
                status_callback("Performing hyperparameter tuning...")
            self.model = self.auto_tune_model(X_train, y_train, progress_callback)
        else:
            self.model = self.get_model(**params)
            
            if status_callback:
                status_callback("Training model...")
            
            # Simulate epochs for non-neural network models
            if self.algorithm != 'Neural Network':
                for epoch in range(epochs):
                    if not self.is_training:
                        break
                    
                    progress = int((epoch + 1) / epochs * 80)
                    if progress_callback:
                        progress_callback(progress)
                    
                    if status_callback:
                        status_callback(f"Epoch {epoch + 1}/{epochs}")
                    
                    time.sleep(0.1)  # Simulate training time
            
            # Actual model training
            self.model.fit(X_train, y_train)
        
        if not self.is_training:
            return None
        
        if progress_callback:
            progress_callback(90)
        
        # Evaluate on validation set if provided
        results = self.evaluate(X_train, y_train, X_val, y_val)
        
        if progress_callback:
            progress_callback(100)
        
        training_time = time.time() - start_time
        results['training_time'] = training_time
        results['algorithm'] = self.algorithm
        results['auto_tuned'] = self.auto_tune
        
        if self.best_params:
            results['best_params'] = self.best_params
        
        if status_callback:
            status_callback("Training completed successfully!")
        
        return results
    
    def auto_tune_model(self, X_train, y_train, progress_callback=None):
        """Perform automatic hyperparameter tuning"""
        base_model = self.get_model()
        param_grid = self.get_param_grid()
        
        if not param_grid:
            return base_model.fit(X_train, y_train)
        
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=3,
            scoring='accuracy',
            n_jobs=-1,
            verbose=0
        )
        
        grid_search.fit(X_train, y_train)
        
        self.best_params = grid_search.best_params_
        
        if progress_callback:
            progress_callback(70)
        
        return grid_search.best_estimator_
    
    def evaluate(self, X_train, y_train, X_val=None, y_val=None):
        """Evaluate the trained model"""
        results = {}
        
        # Training metrics
        y_train_pred = self.model.predict(X_train)
        results['train_accuracy'] = accuracy_score(y_train, y_train_pred)
        results['train_precision'] = precision_score(y_train, y_train_pred, average='weighted', zero_division=0)
        results['train_recall'] = recall_score(y_train, y_train_pred, average='weighted', zero_division=0)
        results['train_f1'] = f1_score(y_train, y_train_pred, average='weighted', zero_division=0)
        
        # Validation metrics if validation set provided
        if X_val is not None and y_val is not None:
            y_val_pred = self.model.predict(X_val)
            results['val_accuracy'] = accuracy_score(y_val, y_val_pred)
            results['val_precision'] = precision_score(y_val, y_val_pred, average='weighted', zero_division=0)
            results['val_recall'] = recall_score(y_val, y_val_pred, average='weighted', zero_division=0)
            results['val_f1'] = f1_score(y_val, y_val_pred, average='weighted', zero_division=0)
            results['confusion_matrix'] = confusion_matrix(y_val, y_val_pred).tolist()
            results['classification_report'] = classification_report(y_val, y_val_pred, zero_division=0)
        
        # Cross-validation score
        try:
            cv_scores = cross_val_score(self.model, X_train, y_train, cv=5, scoring='accuracy')
            results['cv_mean'] = cv_scores.mean()
            results['cv_std'] = cv_scores.std()
        except:
            pass
        
        return results
    
    def predict(self, X):
        """Make predictions on new data"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            raise ValueError(f"{self.algorithm} does not support probability predictions")
    
    def save_model(self, filepath):
        """Save the trained model"""
        if self.model is None:
            raise ValueError("No model to save")
        
        joblib.dump({
            'model': self.model,
            'algorithm': self.algorithm,
            'best_params': self.best_params
        }, filepath)
    
    def load_model(self, filepath):
        """Load a trained model"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.algorithm = data['algorithm']
        self.best_params = data.get('best_params')
    
    def stop_training(self):
        """Stop the training process"""
        self.is_training = False
