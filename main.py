import sys
import time
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from login_window import LoginWindow
from database_handler import db_conn

class SplashScreen(QSplashScreen):
    def __init__(self, text):
        pixmap = QPixmap(400, 200)  # Adjust the size as needed
        pixmap.fill(Qt.white)
        super().__init__(pixmap)

        # Set font and message
        font = QFont("Palatino Linotype", 20)
        self.setFont(font)
        self.showMessage(
            text,
            Qt.AlignCenter,
            Qt.black
        )

    def mousePressEvent(self, event):
        # Override to prevent closing on click
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    splash = SplashScreen('Connecting to Billboard Genie')
    splash.show()

    if db_conn():
        window = LoginWindow()
        window.showMaximized()
        splash.finish(window)
    else: 
        splash.close()
        splash = SplashScreen('No Internet Connection')
        splash.show()
        time.sleep(5)
        splash.close()
        exit()
    
    sys.exit(app.exec_())
