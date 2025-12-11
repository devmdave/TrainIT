"""
Style Manager for TrainIT Application
Provides dark and light themes with modern styling
"""


class StyleManager:
    """Manages application themes and styles"""
    
    def __init__(self):
        self.common_styles = """
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
            }
            
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            QPushButton:hover {
                transform: translateY(-2px);
            }
            
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 30px;
            }
            
            QSpinBox, QDoubleSpinBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 30px;
            }
            
            QCheckBox {
                spacing: 8px;
                padding: 5px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
            }
            
            QProgressBar {
                border-radius: 15px;
                text-align: center;
                font-weight: bold;
            }
            
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
            
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 5px;
                border-radius: 6px 6px 0 0;
                font-weight: 600;
            }
            
            QScrollBar:vertical {
                border: none;
                width: 12px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                border: none;
                height: 12px;
                margin: 0px;
            }
            
            QScrollBar::handle:horizontal {
                border-radius: 6px;
                min-width: 30px;
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """
    
    def get_dark_theme(self):
        """Get dark theme stylesheet"""
        return self.common_styles + """
            /* Main Window */
            QMainWindow, QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            
            /* Header */
            #header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #89b4fa, stop:1 #cba6f7);
                border-bottom: 3px solid #6c7086;
            }
            
            #appTitle {
                color: #ffffff;
                font-weight: bold;
            }
            
            #appSubtitle {
                color: #f5f5f5;
            }
            
            /* Buttons */
            #primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #89b4fa, stop:1 #74c7ec);
                color: #ffffff;
            }
            
            #primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #74c7ec, stop:1 #89b4fa);
            }
            
            #secondaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #cba6f7, stop:1 #f5c2e7);
                color: #ffffff;
            }
            
            #secondaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5c2e7, stop:1 #cba6f7);
            }
            
            #successButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a6e3a1, stop:1 #94e2d5);
                color: #1e1e2e;
                font-size: 13pt;
            }
            
            #successButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #94e2d5, stop:1 #a6e3a1);
            }
            
            #dangerButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f38ba8, stop:1 #eba0ac);
                color: #ffffff;
                font-size: 13pt;
            }
            
            #dangerButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #eba0ac, stop:1 #f38ba8);
            }
            
            #themeButton {
                background: #313244;
                color: #cdd6f4;
                border: 2px solid #6c7086;
            }
            
            #themeButton:hover {
                background: #45475a;
                border-color: #89b4fa;
            }
            
            /* Cards */
            #modernCard {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 12px;
            }
            
            #cardTitle {
                color: #cdd6f4;
                font-size: 14pt;
                font-weight: bold;
                padding: 5px;
            }
            
            /* Labels */
            #pathLabel {
                color: #89b4fa;
                padding: 8px;
                background: #1e1e2e;
                border-radius: 6px;
                border: 2px solid #45475a;
            }
            
            /* Input Fields */
            QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 2px solid #45475a;
            }
            
            QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
                border-color: #89b4fa;
            }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #cdd6f4;
                margin-right: 5px;
            }
            
            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background: #45475a;
                border: none;
                width: 20px;
            }
            
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
                background: #585b70;
            }
            
            /* CheckBox */
            QCheckBox {
                color: #cdd6f4;
            }
            
            QCheckBox::indicator {
                background: #1e1e2e;
                border: 2px solid #45475a;
            }
            
            QCheckBox::indicator:hover {
                border-color: #89b4fa;
            }
            
            QCheckBox::indicator:checked {
                background: #89b4fa;
                border-color: #89b4fa;
            }
            
            /* Progress Bar */
            #modernProgressBar {
                background-color: #1e1e2e;
                border: 2px solid #45475a;
                color: #1e1e2e;
            }
            
            #modernProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #89b4fa, stop:0.5 #cba6f7, stop:1 #f5c2e7);
                border-radius: 13px;
            }
            
            /* Console */
            #console {
                background-color: #181825;
                color: #a6e3a1;
                border: 2px solid #45475a;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            
            #resultsText {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 2px solid #45475a;
            }
            
            /* Tabs */
            #modernTabs QTabBar::tab {
                background: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
            }
            
            #modernTabs QTabBar::tab:selected {
                background: #45475a;
                border-bottom-color: #89b4fa;
                color: #89b4fa;
            }
            
            #modernTabs QTabBar::tab:hover:!selected {
                background: #3d3d52;
            }
            
            /* Status Indicator */
            #statusIndicator {
                background: #313244;
                border: 2px solid #45475a;
                border-radius: 8px;
                padding: 15px;
            }
            
            #statusText {
                color: #cdd6f4;
                font-size: 12pt;
                font-weight: bold;
            }
            
            /* ScrollBar */
            QScrollBar:vertical {
                background: #1e1e2e;
            }
            
            QScrollBar::handle:vertical {
                background: #45475a;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #585b70;
            }
            
            QScrollBar:horizontal {
                background: #1e1e2e;
            }
            
            QScrollBar::handle:horizontal {
                background: #45475a;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #585b70;
            }
            
            /* Status Bar */
            QStatusBar {
                background: #313244;
                color: #cdd6f4;
                border-top: 2px solid #45475a;
            }
        """
    
    def get_light_theme(self):
        """Get light theme stylesheet"""
        return self.common_styles + """
            /* Main Window */
            QMainWindow, QWidget {
                background-color: #f5f5f5;
                color: #2c3e50;
            }
            
            /* Header */
            #header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-bottom: 3px solid #e0e0e0;
            }
            
            #appTitle {
                color: #ffffff;
                font-weight: bold;
            }
            
            #appSubtitle {
                color: #f5f5f5;
            }
            
            /* Buttons */
            #primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #4facfe);
                color: #ffffff;
            }
            
            #primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4facfe, stop:1 #667eea);
            }
            
            #secondaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f093fb, stop:1 #f5576c);
                color: #ffffff;
            }
            
            #secondaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5576c, stop:1 #f093fb);
            }
            
            #successButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #43e97b, stop:1 #38f9d7);
                color: #ffffff;
                font-size: 13pt;
            }
            
            #successButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38f9d7, stop:1 #43e97b);
            }
            
            #dangerButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fa709a, stop:1 #fee140);
                color: #ffffff;
                font-size: 13pt;
            }
            
            #dangerButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fee140, stop:1 #fa709a);
            }
            
            #themeButton {
                background: #ffffff;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
            }
            
            #themeButton:hover {
                background: #f0f0f0;
                border-color: #667eea;
            }
            
            /* Cards */
            #modernCard {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
            }
            
            #cardTitle {
                color: #2c3e50;
                font-size: 14pt;
                font-weight: bold;
                padding: 5px;
            }
            
            /* Labels */
            #pathLabel {
                color: #667eea;
                padding: 8px;
                background: #f5f5f5;
                border-radius: 6px;
                border: 2px solid #e0e0e0;
            }
            
            /* Input Fields */
            QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #ffffff;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
            }
            
            QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
                border-color: #667eea;
            }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2c3e50;
                margin-right: 5px;
            }
            
            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background: #f0f0f0;
                border: none;
                width: 20px;
            }
            
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
                background: #e0e0e0;
            }
            
            /* CheckBox */
            QCheckBox {
                color: #2c3e50;
            }
            
            QCheckBox::indicator {
                background: #ffffff;
                border: 2px solid #e0e0e0;
            }
            
            QCheckBox::indicator:hover {
                border-color: #667eea;
            }
            
            QCheckBox::indicator:checked {
                background: #667eea;
                border-color: #667eea;
            }
            
            /* Progress Bar */
            #modernProgressBar {
                background-color: #f0f0f0;
                border: 2px solid #e0e0e0;
                color: #ffffff;
            }
            
            #modernProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border-radius: 13px;
            }
            
            /* Console */
            #console {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 2px solid #e0e0e0;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            
            #resultsText {
                background-color: #ffffff;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
            }
            
            /* Tabs */
            #modernTabs QTabBar::tab {
                background: #ffffff;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
            }
            
            #modernTabs QTabBar::tab:selected {
                background: #f0f0f0;
                border-bottom-color: #667eea;
                color: #667eea;
            }
            
            #modernTabs QTabBar::tab:hover:!selected {
                background: #f5f5f5;
            }
            
            /* Status Indicator */
            #statusIndicator {
                background: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
            
            #statusText {
                color: #2c3e50;
                font-size: 12pt;
                font-weight: bold;
            }
            
            /* ScrollBar */
            QScrollBar:vertical {
                background: #f5f5f5;
            }
            
            QScrollBar::handle:vertical {
                background: #c0c0c0;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            
            QScrollBar:horizontal {
                background: #f5f5f5;
            }
            
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #a0a0a0;
            }
            
            /* Status Bar */
            QStatusBar {
                background: #ffffff;
                color: #2c3e50;
                border-top: 2px solid #e0e0e0;
            }
        """
