from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("English Practice")
        import os
        icon_path = os.path.join(os.getcwd(), 'data', 'app.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.resize(1000, 700)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
    def add_view(self, view) -> int:
        """Adds a view to the stack and returns its index."""
        return self.stacked_widget.addWidget(view)
        
    def show_view(self, index: int):
        """Switches the current visible view to the given index."""
        self.stacked_widget.setCurrentIndex(index)
        
    def closeEvent(self, event):
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, 'Xác nhận thoát',
            "Bạn có chắc chắn muốn thoát khỏi ứng dụng?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
