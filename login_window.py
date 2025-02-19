from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QDesktopWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
# from QT_dashboard_old import DashboardWindow
from dashboard_window_copy import CameraRTSPWindow
from database_handler import authenticate_user, exising_email, update_db_password
from signup_window import SignupWindow
from button_hover import HoverButton
import random
import requests
import re
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Billboard Genie - Login')
        self.setWindowIcon(QIcon(resource_path("media\icon.png")))
        self.setStyleSheet("background-color: white;")

        # Top Bar
        top_bar = QHBoxLayout()
        self.logo = QLabel()
        self.logo.setPixmap(QIcon(resource_path("media\icon.png")).pixmap(100, 100))
        
        self.title_label = QLabel('Billboard Genie')
        self.title_label.setFont(QFont("Palatino Linotype", 64))
        self.title_label.setStyleSheet("margin-left: 20px;")
        
        top_bar.addStretch()
        top_bar.addWidget(self.logo)
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        # top_bar.setContentsMargins(20, 20, 20, 0)  # Adjust margins as needed
        
        layout = QVBoxLayout()
        center_layout = QVBoxLayout()

        self.email_label = QLabel('Email:')
        self.email_label.setStyleSheet("margin-left: 500px;")
        self.email_label.setFont(QFont("Palatino Linotype", 12))
        self.email_entry = QLineEdit()
        self.email_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.email_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.email_label)
        center_layout.addWidget(self.email_entry)

        self.password_label = QLabel('Password:')
        self.password_label.setStyleSheet("margin-left: 500px;")
        self.password_label.setFont(QFont("Palatino Linotype", 12))
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.password_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.password_label)
        center_layout.addWidget(self.password_entry)

        #Login  Button
        self.login_button = HoverButton(
            'Login', 
            self, 
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #25C863; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style=""
        )
        self.login_button.setFont(QFont("Palatino Linotype", 12))
        self.login_button.clicked.connect(self.validate_fields)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addStretch()
        center_layout.addLayout(button_layout)

                
        layout.addLayout(top_bar)
        layout.addStretch(1)
        layout.addLayout(center_layout)
        layout.addStretch(1)

        self.forgot_password_label = QLabel('<a href="#">Forgot password?</a>')
        self.forgot_password_label.setStyleSheet("color: blue; text-decoration: none;")
        self.forgot_password_label.setFont(QFont("Palatino Linotype", 12))
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        self.forgot_password_label.setOpenExternalLinks(False)
        self.forgot_password_label.linkActivated.connect(self.show_reset_password)
        center_layout.addWidget(self.forgot_password_label)

        self.sign_up_label = QLabel('<a href="#">Don\'t have an account? Sign up now</a>')
        self.sign_up_label.setStyleSheet("color: blue;")
        self.sign_up_label.setFont(QFont("Palatino Linotype", 12))
        self.sign_up_label.setAlignment(Qt.AlignCenter)
        self.sign_up_label.setOpenExternalLinks(False)
        self.sign_up_label.linkActivated.connect(self.show_signup)
        center_layout.addWidget(self.sign_up_label)

        self.setLayout(layout)

        # Centering the window
        self.move((width - self.width()) // 2, (height - self.height()) // 2)

    def validate_email(self, email):
        # Regular expression for validating email format
        pattern = r'^[a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z_.]+$'
        return re.match(pattern, email)

    def validate_fields(self):
        email = self.email_entry.text()
        password = self.password_entry.text()

        if not(email and password):
            QMessageBox.warning(self, "Login Failed", "Fill all the fields")
            return
    
        if not self.validate_email(email):
            QMessageBox.warning(self, "Signup Failed", "Invalid email format (should be like 'someone@domain.com')")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Signup Failed", "Passwords must be 8 characters long")
            return
        
        self.login()
                
    def login(self):
        email = self.email_entry.text()
        password = self.password_entry.text()
        
        user = authenticate_user(email, password)
        if user[0] != None:
            self.dashboard_window = CameraRTSPWindow(self.email_entry.text())
            # self.dashboard_window = DashboardWindow(self.email_entry.text())
            self.dashboard_window.showMaximized()
            self.close()
        else:
            QMessageBox.critical(self, "Error", user[1])

    def show_signup(self):
        self.signup_window = SignupWindow()
        self.signup_window.showMaximized()
        self.close()

    def show_reset_password(self):
        self.reset_password_window = ResetPasswordWindow(self)
        self.reset_password_window.showMaximized()
        self.close()


        
class ResetPasswordWindow(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.initUI()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Billboard Genie - Reset Password')
        self.setWindowIcon(QIcon(resource_path("media\icon.png")))
        self.setStyleSheet("background-color: white;")

        # Top Bar
        top_bar = QHBoxLayout()
        self.logo = QLabel()
        self.logo.setPixmap(QIcon(resource_path("media\icon.png")).pixmap(100, 100))
        
        self.title_label = QLabel('Billboard Genie')
        self.title_label.setFont(QFont("Palatino Linotype", 64))
        self.title_label.setStyleSheet("margin-left: 20px;")
        
        top_bar.addStretch()
        top_bar.addWidget(self.logo)
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()

        layout = QVBoxLayout()
        center_layout = QVBoxLayout()

        self.email_label = QLabel('Enter your registered Email:')
        self.email_label.setStyleSheet("margin-left: 500px;")
        self.email_label.setFont(QFont("Palatino Linotype", 12))
        self.email_entry = QLineEdit()
        self.email_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.email_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.email_label)
        center_layout.addWidget(self.email_entry)

        self.send_otp_button = HoverButton(
            'Send OTP',
            self,
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #007fff; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style=""
        )
        self.send_otp_button.setFont(QFont("Palatino Linotype", 12))
        self.send_otp_button.clicked.connect(self.send_otp)

        # Add Go Back Button
        self.go_back_button = HoverButton(
            '< Back',
            self,
            default_style="background-color: white; color: black; border-radius: 10px;",
            hover_style="background-color: white; color: #007fff; border-radius: 10px;",
            disabled_style=""
        )
        self.go_back_button.setFont(QFont("Palatino Linotype", 12))
        self.go_back_button.clicked.connect(self.go_back)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.send_otp_button)
        button_layout.addStretch()
        
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button_layout.addWidget(self.go_back_button)
        back_button_layout.addStretch()

        center_layout.addLayout(button_layout)
        center_layout.addLayout(back_button_layout)

        layout.addLayout(top_bar)
        layout.addStretch(1)
        layout.addLayout(center_layout)
        layout.addStretch(1)

        self.setLayout(layout)
        self.move((width - self.width()) // 2, (height - self.height()) // 2)

    def send_otp(self):
        email = self.email_entry.text()
        if not email:
            QMessageBox.warning(self, 'Error', 'Please enter your registered email address.')
            return
        
        ex_email = exising_email(email)
        if ex_email[0]:
            QMessageBox.critical(self, 'Error', 'Cannot find your email.')
            return
        else:
            user_name = ex_email[2]['fullname']

            otp = random.randint(100000, 999999)
            url = "https://api.brevo.com/v3/smtp/email"

            payload = {
                "sender": {
                    "name": "Billboard Genie",
                    "email": "munam880834@gmail.com"
                },
                "to": [
                    {
                        "email": email,
                        "name": user_name
                    }
                ],
                "htmlContent": f"<html><body><p>Hello {user_name}</p><p>This is your OTP to reset your Billboard Genie password.</p><h1>{otp}</h1></body></html>",
                "subject": "OTP for Password Reset"
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": "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"
            }

            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 201:
                self.otp_window = OTPResetWindow(email, otp, self)
                self.otp_window.showMaximized()
                self.close()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to send OTP. Please try again.')

    def go_back(self):
        self.previous_window.showMaximized()
        self.close()



class OTPResetWindow(QWidget):
    def __init__(self, email, otp, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.email = email
        self.otp = otp
        self.initUI()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Billboard Genie - OTP Verification')
        self.setWindowIcon(QIcon(resource_path("media\icon.png")))
        self.setStyleSheet("background-color: white;")

        # Top Bar
        top_bar = QHBoxLayout()
        self.logo = QLabel()
        self.logo.setPixmap(QIcon(resource_path("media\icon.png")).pixmap(100, 100))
        
        self.title_label = QLabel('Billboard Genie')
        self.title_label.setFont(QFont("Palatino Linotype", 64))
        self.title_label.setStyleSheet("margin-left: 20px;")
        
        top_bar.addStretch()
        top_bar.addWidget(self.logo)
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()

        layout = QVBoxLayout()
        center_layout = QVBoxLayout()

        self.otp_label = QLabel(f'Enter OTP sent to {self.email}')
        self.otp_label.setStyleSheet("margin-left: 500px;")
        self.otp_label.setFont(QFont("Palatino Linotype", 12))
        self.otp_entry = QLineEdit()
        self.otp_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.otp_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.otp_label)
        center_layout.addWidget(self.otp_entry)

        self.verify_button = HoverButton(
            'Verify OTP',
            self,
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #25C863; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style=""
        )
        self.verify_button.setFont(QFont("Palatino Linotype", 12))
        self.verify_button.clicked.connect(self.verify_otp)

        # Add Go Back Button
        self.go_back_button = HoverButton(
            'Incorrect Email? Change',
            self,
            default_style="background-color: white; color: black; border-radius: 10px;",
            hover_style="background-color: white; color: #007fff; border-radius: 10px;",
            disabled_style=""
        )
        self.go_back_button.setFont(QFont("Palatino Linotype", 12))
        self.go_back_button.clicked.connect(self.go_back)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.verify_button)
        button_layout.addStretch()
        
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button_layout.addWidget(self.go_back_button)
        back_button_layout.addStretch()

        center_layout.addLayout(button_layout)
        center_layout.addLayout(back_button_layout)

        layout.addLayout(top_bar)
        layout.addStretch(1)
        layout.addLayout(center_layout)
        layout.addStretch(1)

        self.setLayout(layout)
        self.move((width - self.width()) // 2, (height - self.height()) // 2)
    
    def isnum(self, otp):
        try:
            int(otp)
            return True
        except ValueError:
            return False

    def verify_otp(self):
        if not self.isnum(self.otp_entry.text()) or not self.otp_entry.text() or len(self.otp_entry.text())!=6:
            QMessageBox.warning(self, 'OTP Verification Failed', 'OTP must be a 6 digit number.') 
            self.otp_entry.clear()
            return

        entered_otp = int(self.otp_entry.text())
        if entered_otp == self.otp:
            self.reset_password_window = ResetPasswordWindowConfirmed(self.email)
            self.reset_password_window.showMaximized()
            self.close()
        else:
            QMessageBox.warning(self, 'OTP Verification Failed', 'Invalid OTP. Please try again.')
            self.otp_entry.clear()
    
    def go_back(self):
        self.previous_window.showMaximized()
        self.close()



class ResetPasswordWindowConfirmed(QWidget):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.initUI()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Billboard Genie - Reset Password')
        self.setWindowIcon(QIcon(resource_path("media\icon.png")))
        self.setStyleSheet("background-color: white;")

        # Top Bar
        top_bar = QHBoxLayout()
        self.logo = QLabel()
        self.logo.setPixmap(QIcon(resource_path("media\icon.png")).pixmap(100, 100))
        
        self.title_label = QLabel('Billboard Genie')
        self.title_label.setFont(QFont("Palatino Linotype", 64))
        self.title_label.setStyleSheet("margin-left: 20px;")
        
        top_bar.addStretch()
        top_bar.addWidget(self.logo)
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()

        layout = QVBoxLayout()
        center_layout = QVBoxLayout()

        self.new_password_label = QLabel('Enter New Password:')
        self.new_password_label.setStyleSheet("margin-left: 500px;")
        self.new_password_label.setFont(QFont("Palatino Linotype", 12))
        self.new_password_entry = QLineEdit()
        self.new_password_entry.setEchoMode(QLineEdit.Password)
        self.new_password_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.new_password_entry.setFont(QFont("Palatino Linotype", 12))

        self.confirm_password_label = QLabel('Confirm New Password:')
        self.confirm_password_label.setStyleSheet("margin-left: 500px;")
        self.confirm_password_label.setFont(QFont("Palatino Linotype", 12))
        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.confirm_password_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.confirm_password_entry.setFont(QFont("Palatino Linotype", 12))

        center_layout.addWidget(self.new_password_label)
        center_layout.addWidget(self.new_password_entry)
        center_layout.addWidget(self.confirm_password_label)
        center_layout.addWidget(self.confirm_password_entry)

        self.reset_button = HoverButton(
            'Reset Password',
            self,
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #007fff; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style=""
        )
        self.reset_button.setFont(QFont("Palatino Linotype", 12))
        self.reset_button.clicked.connect(self.reset_password)

        # Add Go Back Button
        self.go_back_button = HoverButton(
            'Cancel',
            self,
            default_style="background-color: white; color: black; border-radius: 10px;",
            hover_style="background-color: white; color: #007fff; border-radius: 10px;",
            disabled_style=""
        )
        self.go_back_button.setFont(QFont("Palatino Linotype", 12))
        self.go_back_button.clicked.connect(self.go_back)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        back_button_layout.addWidget(self.go_back_button)
        back_button_layout.addStretch()

        center_layout.addLayout(button_layout)
        center_layout.addLayout(back_button_layout)

        layout.addLayout(top_bar)
        layout.addStretch(1)
        layout.addLayout(center_layout)
        layout.addStretch(1)

        self.setLayout(layout)
        self.move((width - self.width()) // 2, (height - self.height()) // 2)

    def reset_password(self):
        new_password = self.new_password_entry.text()
        confirm_password = self.confirm_password_entry.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, 'Error', 'Please fill all fields.')
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, 'Error', 'Passwords do not match.')
            return
        
        if len(new_password) < 8:
            QMessageBox.warning(self, "Error", "Passwords must be 8 characters long")
            return

        if update_password(self.email, new_password):
            QMessageBox.information(self, 'Success', 'Password reset successful!')
            self.login_window = LoginWindow()
            self.login_window.showMaximized()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Failed to reset password. Please try again.')
            return

    def go_back(self):
        self.cancel = LoginWindow()
        self.cancel.showMaximized()
        self.close()

def update_password(email, new_password):
    update_db_password(email, new_password)
    if update_db_password:
        return True
    else:
        return False