import sys
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QListWidget, QListWidgetItem, QLabel, 
    QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import requests

class FirebaseManager:
    def __init__(self, database_url):
        self.database_url = database_url.rstrip('/')
    
    def get_messages(self):
        """Retrieve all messages from Firebase using REST API"""
        try:
            url = f"{self.database_url}/messages.json"
            response = requests.get(url)
            
            if response.status_code == 200:
                messages = response.json()
                return messages if messages else {}
            else:
                print(f"HTTP Error: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return {}
    
    def delete_message(self, message_id):
        """Delete a specific message from Firebase"""
        try:
            url = f"{self.database_url}/messages/{message_id}.json"
            response = requests.delete(url)
            
            if response.status_code == 200:
                return True
            else:
                print(f"HTTP Error while deleting: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error deleting message: {e}")
            return False

class ModernMessageWidget(QWidget):
    def __init__(self, message_id, message_data, parent=None):
        super().__init__(parent)
        self.message_id = message_id
        self.message_data = message_data
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Set background and border
        self.setStyleSheet("""
            ModernMessageWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2D3250, stop: 1 #424769);
                border: 1px solid #5C6BC0;
                border-radius: 12px;
                margin: 5px;
            }
        """)
        
        # Header with name, date and delete button
        header_layout = QHBoxLayout()
        
        # Name
        name_label = QLabel(self.message_data.get('name', 'Unknown'))
        name_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        # Date
        timestamp = self.message_data.get('timestamp', '')
        if timestamp:
            try:
                date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%b %d, %Y at %I:%M %p')
            except:
                date_str = self.message_data.get('timeString', 'Unknown date')
        else:
            date_str = self.message_data.get('timeString', 'Unknown date')
            
        date_label = QLabel(date_str)
        date_label.setStyleSheet("""
            QLabel {
                color: #B0BEC5;
                font-size: 12px;
                background: transparent;
            }
        """)
        
        # Delete button
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: #FF6B6B;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FF5252;
            }
            QPushButton:pressed {
                background: #E53935;
            }
        """)
        delete_btn.setFixedSize(80, 30)
        delete_btn.clicked.connect(self.delete_message)
        
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        header_layout.addWidget(delete_btn)
        
        # Email
        email_label = QLabel(self.message_data.get('email', 'No email'))
        email_label.setStyleSheet("""
            QLabel {
                color: #90CAF9;
                font-size: 14px;
                background: transparent;
            }
        """)
        
        # Subject
        subject = self.message_data.get('subject', 'No subject')
        subject_label = QLabel(f"Subject: {subject}")
        subject_label.setStyleSheet("""
            QLabel {
                color: #FFB74D;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        # Message
        message_text = QTextEdit()
        message_text.setPlainText(self.message_data.get('message', 'No message'))
        message_text.setReadOnly(True)
        message_text.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: #E0E0E0;
                font-size: 14px;
                padding: 10px;
            }
        """)
        message_text.setFixedHeight(120)
        
        layout.addLayout(header_layout)
        layout.addWidget(email_label)
        layout.addWidget(subject_label)
        layout.addWidget(message_text)
        
        self.setLayout(layout)
    
    def delete_message(self):
        """Handle delete button click"""
        sender_name = self.message_data.get('name', 'Unknown')
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete the message from {sender_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.parent and hasattr(self.parent, 'delete_message'):
                self.parent.delete_message(self.message_id)

class MessageListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QListWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1A1A2E, stop: 1 #16213E);
                border: none;
                outline: none;
            }
            QListWidget::item {
                border: none;
                margin: 5px;
            }
            QListWidget::item:selected {
                background: transparent;
            }
        """)
        self.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)

class ModernMessageManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.firebase_manager = None
        self.current_messages = {}
        self.setup_ui()
        self.setup_firebase()
        
    def setup_ui(self):
        """Setup the main window UI"""
        self.setWindowTitle("Portfolio Messages - Jerome Felixraj")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply modern dark theme
        self.apply_modern_theme()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QLabel("Portfolio Contact Messages")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #6C63FF, stop: 1 #FF6B6B);
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                border: none;
            }
        """)
        header.setFixedHeight(70)
        main_layout.addWidget(header)
        
        # Messages area
        self.message_list = MessageListWidget()
        main_layout.addWidget(self.message_list)
        
        # Status bar
        self.status_label = QLabel("Loading messages...")
        self.status_label.setStyleSheet("""
            QLabel {
                background: #1A1A2E;
                color: #90CAF9;
                padding: 10px;
                border-top: 1px solid #6C63FF;
            }
        """)
        self.status_label.setFixedHeight(40)
        main_layout.addWidget(self.status_label)
        
        # Setup refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_messages)
        self.refresh_timer.start(10000)  # Refresh every 10 seconds
    
    def apply_modern_theme(self):
        """Apply modern gradient theme"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0F0F1A, stop: 1 #1A1A2E);
                color: #E0E0E0;
            }
        """)
    
    def setup_firebase(self):
        """Initialize Firebase connection"""
        database_url = "https://portfoliobackend-883c4-default-rtdb.firebaseio.com/"
        self.firebase_manager = FirebaseManager(database_url)
        self.refresh_messages()
    
    def refresh_messages(self):
        """Refresh messages from Firebase"""
        if not self.firebase_manager:
            self.status_label.setText("Firebase not initialized")
            return
        
        messages = self.firebase_manager.get_messages()
        self.current_messages = messages
        
        # Clear existing messages
        self.message_list.clear()
        
        if not messages:
            self.status_label.setText("No messages found")
            return
        
        # Add messages to list
        for message_id, message_data in messages.items():
            message_widget = ModernMessageWidget(message_id, message_data, self)
            item = QListWidgetItem()
            item.setSizeHint(message_widget.sizeHint())
            self.message_list.addItem(item)
            self.message_list.setItemWidget(item, message_widget)
        
        self.status_label.setText(f"Loaded {len(messages)} messages • Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def delete_message(self, message_id):
        """Delete a message and refresh the list"""
        if not self.firebase_manager:
            return
        
        success = self.firebase_manager.delete_message(message_id)
        
        if success:
            self.status_label.setText("Message deleted successfully")
            # Refresh messages after a short delay
            QTimer.singleShot(500, self.refresh_messages)
        else:
            QMessageBox.critical(self, "Error", "Failed to delete message. Please try again.")

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Portfolio Messages")
    app.setApplicationVersion("1.0")
    
    window = ModernMessageManager()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()