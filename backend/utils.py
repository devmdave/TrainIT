"""
Utility functions for TrainIT backend
"""

import os
import json
from datetime import datetime


def create_directories():
    """Create necessary directories for the application"""
    dirs = ['models', 'data', 'logs']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


def log_training_session(config, results, log_dir='logs'):
    """Log training session details"""
    create_directories()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'training_log_{timestamp}.json')
    
    log_data = {
        'timestamp': timestamp,
        'config': config,
        'results': results
    }
    
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=4, default=str)
    
    return log_file


def format_time(seconds):
    """Format time in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"


def get_model_size(model):
    """Get approximate size of model in MB"""
    import sys
    import pickle
    
    try:
        model_bytes = pickle.dumps(model)
        size_mb = sys.getsizeof(model_bytes) / (1024 * 1024)
        return f"{size_mb:.2f} MB"
    except:
        return "Unknown"


def validate_dataset(filepath):
    """Validate if dataset file exists and is readable"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found: {filepath}")
    
    if not os.path.isfile(filepath):
        raise ValueError(f"Path is not a file: {filepath}")
    
    # Check file extension
    valid_extensions = ['.csv', '.xlsx', '.xls', '.json', '.parquet']
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext not in valid_extensions:
        raise ValueError(f"Unsupported file format: {file_ext}. "
                        f"Supported formats: {', '.join(valid_extensions)}")
    
    return True
