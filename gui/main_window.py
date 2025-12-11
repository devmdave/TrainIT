"""
Main Window for TrainIT Application
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QComboBox,
                             QProgressBar, QTextEdit, QGroupBox, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QTabWidget, QSplitter,
                             QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from gui.styles import StyleManager
from gui.widgets import ModernCard, AnimatedButton, StatusIndicator
import os


class TrainingThread(QThread):
    """Background thread for model training"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.is_running = False
    
    def run(self):
        """Run the training process"""
        self.is_running = True
        try:
            self.status.emit("Loading datasets...")
            self.progress.emit(10)
            
            # Simulate training process
            import time
            for i in range(10, 100, 10):
                if not self.is_running:
                    break
                time.sleep(0.5)
                self.progress.emit(i)
                self.status.emit(f"Training... {i}%")
            
            if self.is_running:
                self.progress.emit(100)
                self.status.emit("Training completed!")
                results = {
                    'accuracy': 0.95,
                    'loss': 0.05,
                    'epochs': self.config.get('epochs', 10)
                }
                self.finished.emit(results)
        except Exception as e:
            self.status.emit(f"Error: {str(e)}")
    
    def stop(self):
        """Stop the training process"""
        self.is_running = False


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.training_thread = None
        self.train_dataset_path = ""
        self.test_dataset_path = ""
        self.style_manager = StyleManager()
        self.is_dark_theme = True
        
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("TrainIT - Automated ML Training")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Configuration
        left_panel = self.create_configuration_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Monitoring
        right_panel = self.create_monitoring_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_header(self):
        """Create application header"""
        header = QFrame()
        header.setObjectName("header")
        header.setMinimumHeight(80)
        header.setMaximumHeight(80)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 10, 30, 10)
        
        # Logo and title
        title_layout = QVBoxLayout()
        title = QLabel("🚀 TrainIT")
        title.setObjectName("appTitle")
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title.setFont(title_font)
        
        subtitle = QLabel("Automated Machine Learning Training")
        subtitle.setObjectName("appSubtitle")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle.setFont(subtitle_font)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_layout.setSpacing(0)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Theme toggle button
        self.theme_btn = AnimatedButton("🌙 Dark Mode")
        self.theme_btn.setObjectName("themeButton")
        self.theme_btn.setMinimumSize(140, 45)
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        header_layout.addWidget(self.theme_btn)
        
        return header
    
    def create_configuration_panel(self):
        """Create left configuration panel"""
        panel = QScrollArea()
        panel.setWidgetResizable(True)
        panel.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Dataset Selection Card
        dataset_card = ModernCard("📁 Dataset Selection")
        dataset_layout = QVBoxLayout()
        
        # Training dataset
        train_layout = QHBoxLayout()
        self.train_path_label = QLabel("No file selected")
        self.train_path_label.setObjectName("pathLabel")
        self.train_path_label.setWordWrap(True)
        train_btn = AnimatedButton("Browse Training Data")
        train_btn.setObjectName("primaryButton")
        train_btn.clicked.connect(self.select_train_dataset)
        train_layout.addWidget(self.train_path_label, 1)
        train_layout.addWidget(train_btn)
        
        # Test dataset
        test_layout = QHBoxLayout()
        self.test_path_label = QLabel("No file selected")
        self.test_path_label.setObjectName("pathLabel")
        self.test_path_label.setWordWrap(True)
        test_btn = AnimatedButton("Browse Test Data")
        test_btn.setObjectName("secondaryButton")
        test_btn.clicked.connect(self.select_test_dataset)
        test_layout.addWidget(self.test_path_label, 1)
        test_layout.addWidget(test_btn)
        
        dataset_layout.addLayout(train_layout)
        dataset_layout.addLayout(test_layout)
        dataset_card.set_content_layout(dataset_layout)
        
        # Model Configuration Card
        model_card = ModernCard("⚙️ Model Configuration")
        model_layout = QVBoxLayout()
        
        # Algorithm selection
        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithm:")
        algo_label.setMinimumWidth(120)
        self.algo_combo = QComboBox()
        self.algo_combo.setObjectName("modernComboBox")
        self.algo_combo.addItems([
            "Random Forest",
            "Gradient Boosting",
            "Neural Network",
            "Support Vector Machine",
            "Logistic Regression",
            "Decision Tree"
        ])
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo, 1)
        
        # Epochs
        epochs_layout = QHBoxLayout()
        epochs_label = QLabel("Epochs:")
        epochs_label.setMinimumWidth(120)
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(1, 1000)
        self.epochs_spin.setValue(10)
        epochs_layout.addWidget(epochs_label)
        epochs_layout.addWidget(self.epochs_spin, 1)
        
        # Learning rate
        lr_layout = QHBoxLayout()
        lr_label = QLabel("Learning Rate:")
        lr_label.setMinimumWidth(120)
        self.lr_spin = QDoubleSpinBox()
        self.lr_spin.setRange(0.0001, 1.0)
        self.lr_spin.setValue(0.001)
        self.lr_spin.setDecimals(4)
        self.lr_spin.setSingleStep(0.0001)
        lr_layout.addWidget(lr_label)
        lr_layout.addWidget(self.lr_spin, 1)
        
        # Batch size
        batch_layout = QHBoxLayout()
        batch_label = QLabel("Batch Size:")
        batch_label.setMinimumWidth(120)
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 1024)
        self.batch_spin.setValue(32)
        batch_layout.addWidget(batch_label)
        batch_layout.addWidget(self.batch_spin, 1)
        
        # Auto-tuning checkbox
        self.auto_tune_cb = QCheckBox("Enable Automatic Hyperparameter Tuning")
        self.auto_tune_cb.setObjectName("modernCheckBox")
        
        model_layout.addLayout(algo_layout)
        model_layout.addLayout(epochs_layout)
        model_layout.addLayout(lr_layout)
        model_layout.addLayout(batch_layout)
        model_layout.addWidget(self.auto_tune_cb)
        model_card.set_content_layout(model_layout)
        
        # Training Controls Card
        controls_card = ModernCard("🎯 Training Controls")
        controls_layout = QVBoxLayout()
        
        buttons_layout = QHBoxLayout()
        self.train_btn = AnimatedButton("🚀 Start Training")
        self.train_btn.setObjectName("successButton")
        self.train_btn.setMinimumHeight(50)
        self.train_btn.clicked.connect(self.start_training)
        
        self.stop_btn = AnimatedButton("⏹️ Stop Training")
        self.stop_btn.setObjectName("dangerButton")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_training)
        
        buttons_layout.addWidget(self.train_btn)
        buttons_layout.addWidget(self.stop_btn)
        
        controls_layout.addLayout(buttons_layout)
        controls_card.set_content_layout(controls_layout)
        
        # Add cards to layout
        layout.addWidget(dataset_card)
        layout.addWidget(model_card)
        layout.addWidget(controls_card)
        layout.addStretch()
        
        panel.setWidget(container)
        return panel
    
    def create_monitoring_panel(self):
        """Create right monitoring panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Status Card
        status_card = ModernCard("📊 Training Status")
        status_layout = QVBoxLayout()
        
        self.status_indicator = StatusIndicator()
        status_layout.addWidget(self.status_indicator)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("modernProgressBar")
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        status_layout.addWidget(self.progress_bar)
        
        status_card.set_content_layout(status_layout)
        
        # Metrics Card
        metrics_card = ModernCard("📈 Training Metrics")
        metrics_layout = QVBoxLayout()
        
        # Tabs for different metrics
        self.metrics_tabs = QTabWidget()
        self.metrics_tabs.setObjectName("modernTabs")
        
        # Console tab
        self.console = QTextEdit()
        self.console.setObjectName("console")
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 9))
        self.metrics_tabs.addTab(self.console, "📝 Console")
        
        # Results tab
        self.results_text = QTextEdit()
        self.results_text.setObjectName("resultsText")
        self.results_text.setReadOnly(True)
        self.metrics_tabs.addTab(self.results_text, "📊 Results")
        
        metrics_layout.addWidget(self.metrics_tabs)
        metrics_card.set_content_layout(metrics_layout)
        
        # Export Card
        export_card = ModernCard("💾 Export Model")
        export_layout = QVBoxLayout()
        
        self.export_btn = AnimatedButton("Export Trained Model")
        self.export_btn.setObjectName("primaryButton")
        self.export_btn.setMinimumHeight(45)
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_model)
        
        export_layout.addWidget(self.export_btn)
        export_card.set_content_layout(export_layout)
        
        # Add cards to layout
        layout.addWidget(status_card, 1)
        layout.addWidget(metrics_card, 3)
        layout.addWidget(export_card, 0)
        
        return panel
    
    def select_train_dataset(self):
        """Select training dataset"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Training Dataset",
            "",
            "Data Files (*.csv *.xlsx *.json *.parquet);;All Files (*.*)"
        )
        if file_path:
            self.train_dataset_path = file_path
            self.train_path_label.setText(os.path.basename(file_path))
            self.log_message(f"✅ Training dataset loaded: {os.path.basename(file_path)}")
    
    def select_test_dataset(self):
        """Select test dataset"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Test Dataset",
            "",
            "Data Files (*.csv *.xlsx *.json *.parquet);;All Files (*.*)"
        )
        if file_path:
            self.test_dataset_path = file_path
            self.test_path_label.setText(os.path.basename(file_path))
            self.log_message(f"✅ Test dataset loaded: {os.path.basename(file_path)}")
    
    def start_training(self):
        """Start model training"""
        if not self.train_dataset_path:
            self.log_message("❌ Please select a training dataset first!")
            return
        
        # Disable/enable buttons
        self.train_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.export_btn.setEnabled(False)
        
        # Get configuration
        config = {
            'algorithm': self.algo_combo.currentText(),
            'epochs': self.epochs_spin.value(),
            'learning_rate': self.lr_spin.value(),
            'batch_size': self.batch_spin.value(),
            'auto_tune': self.auto_tune_cb.isChecked(),
            'train_data': self.train_dataset_path,
            'test_data': self.test_dataset_path
        }
        
        self.log_message(f"\n{'='*50}")
        self.log_message(f"🚀 Starting Training Session")
        self.log_message(f"{'='*50}")
        self.log_message(f"Algorithm: {config['algorithm']}")
        self.log_message(f"Epochs: {config['epochs']}")
        self.log_message(f"Learning Rate: {config['learning_rate']}")
        self.log_message(f"Batch Size: {config['batch_size']}")
        self.log_message(f"Auto-tune: {config['auto_tune']}")
        self.log_message(f"{'='*50}\n")
        
        # Start training thread
        self.training_thread = TrainingThread(config)
        self.training_thread.progress.connect(self.update_progress)
        self.training_thread.status.connect(self.update_status)
        self.training_thread.finished.connect(self.training_finished)
        self.training_thread.start()
        
        self.status_indicator.set_status("running")
    
    def stop_training(self):
        """Stop training process"""
        if self.training_thread:
            self.training_thread.stop()
            self.log_message("\n⏹️ Training stopped by user")
            self.train_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status_indicator.set_status("stopped")
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def update_status(self, message):
        """Update status message"""
        self.statusBar().showMessage(message)
        self.log_message(message)
    
    def training_finished(self, results):
        """Handle training completion"""
        self.train_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.export_btn.setEnabled(True)
        self.status_indicator.set_status("completed")
        
        self.log_message(f"\n{'='*50}")
        self.log_message("✅ Training Completed Successfully!")
        self.log_message(f"{'='*50}\n")
        
        # Display results
        results_text = f"""
Training Results
================

Algorithm: {self.algo_combo.currentText()}
Epochs Completed: {results['epochs']}
Final Accuracy: {results['accuracy']*100:.2f}%
Final Loss: {results['loss']:.4f}

Model is ready for export!
"""
        self.results_text.setPlainText(results_text)
        self.metrics_tabs.setCurrentIndex(1)
    
    def export_model(self):
        """Export trained model"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Model",
            "trained_model.pkl",
            "Model Files (*.pkl *.h5 *.joblib);;All Files (*.*)"
        )
        if file_path:
            self.log_message(f"💾 Model exported to: {file_path}")
            self.statusBar().showMessage(f"Model exported successfully to {os.path.basename(file_path)}")
    
    def log_message(self, message):
        """Add message to console"""
        self.console.append(message)
        # Auto-scroll to bottom
        cursor = self.console.textCursor()
        cursor.movePosition(cursor.End)
        self.console.setTextCursor(cursor)
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme"""
        if self.is_dark_theme:
            self.setStyleSheet(self.style_manager.get_dark_theme())
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.setStyleSheet(self.style_manager.get_light_theme())
            self.theme_btn.setText("🌙 Dark Mode")
