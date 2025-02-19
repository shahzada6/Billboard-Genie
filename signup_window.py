from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QDesktopWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from database_handler import signup_user, exising_email
from button_hover import HoverButton
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

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Billboard Genie - Signup')
        self.setWindowIcon(QIcon(resource_path("media/icon.png")))
        self.setStyleSheet("background-color: white;")

        # Top Bar
        top_bar = QHBoxLayout()
        self.logo = QLabel()
        self.logo.setPixmap(QIcon(resource_path("media/icon.png")).pixmap(100, 100))
        
        self.title_label = QLabel('Billboard Genie')
        self.title_label.setFont(QFont("Palatino Linotype", 64))
        self.title_label.setStyleSheet("margin-left: 20px;")
        
        top_bar.addStretch()
        top_bar.addWidget(self.logo)
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()

        layout = QVBoxLayout()
        center_layout = QVBoxLayout()

        # Full Name
        self.fullname_label = QLabel('Full Name:')
        self.fullname_label.setStyleSheet("margin-left: 500px;")
        self.fullname_label.setFont(QFont("Palatino Linotype", 12))
        self.fullname_entry = QLineEdit()
        self.fullname_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding-right: 5px; padding-left:5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.fullname_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.fullname_label)
        center_layout.addWidget(self.fullname_entry)

        self.email_label = QLabel('Email:')
        self.email_label.setStyleSheet("margin-left: 500px;")
        self.email_label.setFont(QFont("Palatino Linotype", 12))
        self.email_entry = QLineEdit()
        self.email_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding-right: 5px; padding-left:5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.email_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.email_label)
        center_layout.addWidget(self.email_entry)

        self.phone_label = QLabel('Phone:')
        self.phone_label.setStyleSheet("margin-left: 500px;")
        self.phone_label.setFont(QFont("Palatino Linotype", 12))
        self.phone_entry = QLineEdit()
        self.phone_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.phone_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.phone_label)
        center_layout.addWidget(self.phone_entry)

        self.password_label = QLabel('Password:')
        self.password_label.setStyleSheet("margin-left: 500px;")
        self.password_label.setFont(QFont("Palatino Linotype", 12))
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.password_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.password_label)
        center_layout.addWidget(self.password_entry)

        # Confirm Password
        self.confirm_password_label = QLabel('Confirm Password:')
        self.confirm_password_label.setStyleSheet("margin-left: 500px;")
        self.confirm_password_label.setFont(QFont("Palatino Linotype", 12))
        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.confirm_password_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.confirm_password_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.confirm_password_label)
        center_layout.addWidget(self.confirm_password_entry)

        # Billboard Location
        self.billboard_location_label = QLabel('Billboard Location:')
        self.billboard_location_label.setStyleSheet("margin-left: 500px;")
        self.billboard_location_label.setFont(QFont("Palatino Linotype", 12))
        self.billboard_location_entry = QLineEdit()
        self.billboard_location_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding-right: 5px; padding-left:5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.billboard_location_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.billboard_location_label)
        center_layout.addWidget(self.billboard_location_entry)

        # CPM
        self.cpm_label = QLabel('CPM:')
        self.cpm_label.setStyleSheet("margin-left: 500px;")
        self.cpm_label.setFont(QFont("Palatino Linotype", 12))
        self.cpm_entry = QLineEdit()
        self.cpm_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.cpm_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.cpm_label)
        center_layout.addWidget(self.cpm_entry)

        # Monthly Cost
        self.monthly_cost_label = QLabel('Monthly Cost:')
        self.monthly_cost_label.setStyleSheet("margin-left: 500px;")
        self.monthly_cost_label.setFont(QFont("Palatino Linotype", 12))
        self.monthly_cost_entry = QLineEdit()
        self.monthly_cost_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.monthly_cost_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.monthly_cost_label)
        center_layout.addWidget(self.monthly_cost_entry)

        # Signup Button
        self.signup_button = HoverButton(
            'Signup', 
            self, 
            default_style="background-color: black; color: white; border-radius: 10px; padding: 4px; width:336px",
            hover_style="background-color: #007fff; color: white; border-radius: 10px; padding: 4px; width:336px",
            disabled_style=""
        )
        self.signup_button.setFont(QFont("Palatino Linotype", 12))
        self.signup_button.clicked.connect(self.validate_fields)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.signup_button)
        button_layout.addStretch()
        center_layout.addLayout(button_layout)

        layout.addLayout(top_bar)
        layout.addStretch(1)
        layout.addLayout(center_layout)
        layout.addStretch(1)

        self.sign_up_label = QLabel('<a href="#">Already have an account? Login now</a>')
        self.sign_up_label.setStyleSheet("color: blue;")
        self.sign_up_label.setFont(QFont("Palatino Linotype", 12))
        self.sign_up_label.setAlignment(Qt.AlignCenter)
        self.sign_up_label.setOpenExternalLinks(False)
        self.sign_up_label.linkActivated.connect(self.show_login)
        center_layout.addWidget(self.sign_up_label)

        self.setLayout(layout)

        self.move((width - self.width()) // 2, (height - self.height()) // 2)

    def show_login(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()
    
    def send_verification_email(self):
        import random
        otp = random.randint(100000, 999999)

        url = "https://api.brevo.com/v3/smtp/email"

        payload = {
            "sender": {
                "name": "Billboard Genie",
                "email": "munam880834@gmail.com"
            },
            "to": [
                {
                    "email": self.email_entry.text(),
                    "name": self.fullname_entry.text()
                }
            ],
            "htmlContent": f"<html><body><p>Hello {self.fullname_entry.text()}</p><p>This is your OTP for Billboard Genie account verification.</p><h1>{otp}</h1></body></html>",
            "subject": "OTP for Signup"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": "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"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            user_data = {
                'fullname': self.fullname_entry.text(),
                'email': self.email_entry.text(),
                'phone': self.phone_entry.text(),
                'password': self.password_entry.text(),
                'confirm_password': self.confirm_password_entry.text(),
                'billboard_location': self.billboard_location_entry.text(),
                'cpm': self.cpm_entry.text(),
                'monthly_cost': self.monthly_cost_entry.text()
            }
            self.otp_window = OTPVerificationWindow(self.email_entry.text(), otp, user_data, self)
            self.otp_window.showMaximized()
            self.close()
        else:
            self.send_verification_email()

    def validate_fields(self):        
        fullname = self.fullname_entry.text()
        email = self.email_entry.text()
        phone = self.phone_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        billboard_location = self.billboard_location_entry.text()
        cpm = self.cpm_entry.text()
        monthly_cost = self.monthly_cost_entry.text()

        if not(fullname and email and phone and password and confirm_password and billboard_location and cpm and monthly_cost):
            QMessageBox.warning(self, "Signup Failed", "Fill all the fields")
            return
        
        ex_email = exising_email(email)
        if ex_email[0]:
            if not self.is_string(fullname):
                QMessageBox.warning(self, "Signup Failed", "Name can only contain alphabets (Aa-Zz)\nNumbers and special characters are not allowed")
                return

            if not self.validate_email(email):
                QMessageBox.warning(self, "Signup Failed", "Invalid email format (should be like 'someone@domain.com')")
                return

            if not self.validate_phone(phone):
                QMessageBox.warning(self, "Signup Failed", "Invalid phone number format\nShould be 11 digits starting from 03")
                return

            if len(password) < 8:
                QMessageBox.warning(self, "Signup Failed", "Passwords must be 8 characters long")
                return

            if password != confirm_password:
                QMessageBox.warning(self, "Signup Failed", "Passwords should match")
                return

            if not self.is_string(billboard_location):
                QMessageBox.warning(self, "Signup Failed", "Location can only contain alphabets (Aa-Zz)\nNumbers and special characters are not allowed")
                return

            if not self.is_float(cpm):
                QMessageBox.warning(self, "Signup Failed", "CPM should be a number")
                return

            if not self.is_float(monthly_cost):
                QMessageBox.warning(self, "Signup Failed", "Monthly Cost should be a number")
                return
            
            self.send_verification_email()
        
        elif ex_email[0] == False:
            QMessageBox.critical(self, "Signup Failed", ex_email[1])
            return
        
    def is_string(self, fullname):
        # Regular expression for validating fullname (only letters and spaces)
        pattern = r'^[A-Za-z\s]+$'
        return re.match(pattern, fullname)    
    
    def validate_email(self, email):
        # Regular expression for validating email format
        pattern = r'^[a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z_.]+$'
        return re.match(pattern, email)

    def validate_phone(self, phone):
        # Regular expression for validating phone number (11 digits)
        pattern = r'^03[0-9]{9}$'
        return re.match(pattern, phone)

    def is_float(self, input_value):
        # Check if the input can be split into two parts by a dot
        if "." in input_value:
            # If it contains a dot, check if both parts are digits
            before_dot, after_dot = input_value.split(".")
            if before_dot.isdigit() and after_dot.isdigit():
                return True
        # If it doesn't contain a dot, just check if it consists of digits
        elif input_value.isdigit():
            return True
        return False        
    


class OTPVerificationWindow(QWidget):
    def __init__(self, email, otp, user_data, previous_window):
        super().__init__()
        self.email = email
        self.otp = otp
        self.user_data = user_data
        self.previous_window = previous_window
        self.initUI()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Billboard Genie - OTP Verification')
        self.setWindowIcon(QIcon(resource_path("media/icon.png")))
        self.setStyleSheet("background-color: white;")

        # Top Bar
        top_bar = QHBoxLayout()
        self.logo = QLabel()
        self.logo.setPixmap(QIcon(resource_path("media/icon.png")).pixmap(100, 100))
        
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
            hover_style="background-color: #08d15c; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
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
            fullname = self.user_data['fullname']
            email = self.user_data['email']
            phone = self.user_data['phone']
            password= self.user_data['password']
            billboard_location = self.user_data['billboard_location']
            cpm = self.user_data['cpm']
            monthly_cost = self.user_data['monthly_cost']

            create_user = signup_user(fullname, email, phone, password, billboard_location, cpm, monthly_cost)
            if create_user[0]:    
                QMessageBox.information(self, 'Signup Successful!', 'OTP Verified.\nPress Ok to Login')
                self.show_login()
            elif create_user[0] == False:
                QMessageBox.warning(self, 'Signup Failed', create_user[1])
        else:
            QMessageBox.warning(self, 'OTP Verification Failed', 'Invalid OTP. Please try again.')
            self.otp_entry.clear()
            return
    
    def show_login(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()

    def go_back(self):
        self.previous_window.showMaximized()
        self.close()