"""
Custom widgets for TrainIT Application
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect
from PyQt5.QtGui import QColor


class ModernCard(QFrame):
    """Modern card widget with shadow effect"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("modernCard")
        self.init_ui(title)
        self.add_shadow()
    
    def init_ui(self, title):
        """Initialize card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            layout.addWidget(title_label)
            
            # Separator line
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setMaximumHeight(2)
            layout.addWidget(separator)
        
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
    
    def set_content_layout(self, content_layout):
        """Set the content layout of the card"""
        # Clear existing content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add new content
        while content_layout.count():
            item = content_layout.takeAt(0)
            if item.widget():
                self.content_layout.addWidget(item.widget())
            elif item.layout():
                self.content_layout.addLayout(item.layout())
            else:
                self.content_layout.addItem(item)
    
    def add_shadow(self):
        """Add drop shadow effect"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)


class AnimatedButton(QPushButton):
    """Button with hover animation"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.default_style = ""
    
    def enterEvent(self, event):
        """Mouse enter event"""
        # Add slight scaling effect through minimum size
        self.setMinimumHeight(self.minimumHeight() + 2)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Mouse leave event"""
        # Reset size
        if self.minimumHeight() > 2:
            self.setMinimumHeight(self.minimumHeight() - 2)
        super().leaveEvent(event)


class StatusIndicator(QWidget):
    """Status indicator widget with animated dot"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusIndicator")
        self.current_status = "idle"
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Status dot
        self.dot = QLabel("●")
        self.dot.setObjectName("statusDot")
        self.dot.setAlignment(Qt.AlignCenter)
        dot_font = self.dot.font()
        dot_font.setPointSize(24)
        self.dot.setFont(dot_font)
        
        # Status text
        self.status_text = QLabel("Ready to train")
        self.status_text.setObjectName("statusText")
        
        layout.addWidget(self.dot)
        layout.addWidget(self.status_text, 1)
        
        self.set_status("idle")
    
    def set_status(self, status):
        """Set status (idle, running, completed, stopped, error)"""
        self.current_status = status
        
        status_config = {
            "idle": ("●", "#94e2d5", "Ready to train"),
            "running": ("●", "#a6e3a1", "Training in progress..."),
            "completed": ("✓", "#a6e3a1", "Training completed!"),
            "stopped": ("■", "#f38ba8", "Training stopped"),
            "error": ("✗", "#f38ba8", "Error occurred")
        }
        
        symbol, color, text = status_config.get(status, status_config["idle"])
        
        self.dot.setText(symbol)
        self.dot.setStyleSheet(f"color: {color};")
        self.status_text.setText(text)
        
        # Animate for running status
        if status == "running":
            self.animate_dot()
    
    def animate_dot(self):
        """Animate the status dot"""
        # Simple color animation through timer
        from PyQt5.QtCore import QTimer
        
        if not hasattr(self, 'animation_timer'):
            self.animation_timer = QTimer(self)
            self.animation_timer.timeout.connect(self.toggle_dot_brightness)
            self.animation_state = True
        
        if self.current_status == "running":
            self.animation_timer.start(500)
        else:
            self.animation_timer.stop()
    
    def toggle_dot_brightness(self):
        """Toggle dot brightness for animation"""
        if self.animation_state:
            self.dot.setStyleSheet("color: #a6e3a1;")
        else:
            self.dot.setStyleSheet("color: #60a060;")
        self.animation_state = not self.animation_state


class MetricCard(QFrame):
    """Card to display a single metric"""
    
    def __init__(self, title, value="0", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.init_ui(title, value)
    
    def init_ui(self, title, value):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 10pt; color: #888;")
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignCenter)
        value_font = self.value_label.font()
        value_font.setPointSize(20)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
    
    def set_value(self, value):
        """Update the metric value"""
        self.value_label.setText(str(value))
