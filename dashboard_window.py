import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QSystemTrayIcon, QMenu, QDesktopWidget, QScrollArea
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from button_hover import HoverButton
from database_handler import insert_counts_data
import re
import datetime
import os
import sys

def resource_path(relative_path):
    return relative_path
    # try:
    #     base_path = sys._MEIPASS2
    # except Exception:
    #     base_path = os.path.abspath(".")

    # return os.path.join(base_path, relative_path)

class DashboardWindow(QWidget):
    def __init__(self, email, rtsp, previous_window):
    # def __init__(self, email, rtsp):
        super().__init__()
        self.email = email
        self.url = rtsp
        self.previous_window = previous_window
        self.model = YOLO(resource_path("Weights/weights.pt"))
        self.box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=1, text_scale=0.5)
        self.vehicle_counts = {"car": set(), "motorcycle": set(), "bus": set(), "truck": set()}
        self.tracking = False
        self.roi_confirmed = False
        self.line_points = [(0, 0)] * 4
        self.current_point_index = 0
        self.line_points_copy = [(0, 0)] * 4
        self.current_point_index_copy = 0
        self.current_date = datetime.date.today()
        self.initUI()
        self.display_first_frame()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Dashboard')
        self.setWindowIcon(QIcon(resource_path("media/icon.png")))
        self.setStyleSheet("background-color: white;")

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFixedSize(960, 540)

        video_layout = QHBoxLayout()
        video_layout.addStretch()
        video_layout.addWidget(self.video_label)
        video_layout.addStretch()

        self.roi_button = HoverButton(
            'Confirm ROI', 
            self, 
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #007fff; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style="background-color: grey; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px"
        )
        self.roi_button.setFont(QFont("Palatino Linotype", 12))
        self.roi_button.clicked.connect(self.confirm_roi)

        self.start_stop_button = HoverButton(
            'Start Tracking', 
            self, 
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #25C863; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style="background-color: grey; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px"
        )
        self.start_stop_button.setFont(QFont("Palatino Linotype", 12))
        self.start_stop_button.clicked.connect(self.toggle_tracking)
        self.start_stop_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.roi_button)
        button_layout.addWidget(self.start_stop_button)
        button_layout.addStretch()

        self.coordinates_label = QLabel('ROI Coordinates: Not Confirmed', self)
        self.coordinates_label.setFont(QFont("Palatino Linotype", 12))
        self.coordinates_label.setStyleSheet("padding: 10px;")

        coor_layout = QHBoxLayout()
        coor_layout.addStretch()
        coor_layout.addWidget(self.coordinates_label)
        coor_layout.addStretch()

        self.logout_button = HoverButton(
            'Exit', 
            self, 
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #F22C3D; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style="background-color: grey; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px"
        )
        self.logout_button.setFont(QFont("Palatino Linotype", 12))
        self.logout_button.clicked.connect(self.exit_app)

        logout_layout = QHBoxLayout()
        logout_layout.addStretch()
        logout_layout.addWidget(self.logout_button)
        logout_layout.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(video_layout)
        layout.addLayout(button_layout)
        layout.addLayout(coor_layout)
        layout.addLayout(logout_layout)
        self.setLayout(layout)

        self.tray_icon = QSystemTrayIcon(QIcon(resource_path('media/icon.png')), self)
        tray_menu = QMenu()
        restore_action = tray_menu.addAction("Restore")
        restore_action.triggered.connect(self.showMaximized)
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.close_application)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def display_first_frame(self):
        # Capture the first frame from the video stream
        self.cap = cv2.VideoCapture(self.url)
        ret, frame = self.cap.read()
        if not ret:
            QMessageBox.critical(self, "Error", "Failed to capture video stream.")
            return

        self.cap.release()

        # Resize the frame to fit the label
        frame = cv2.resize(frame, (self.video_label.width(), self.video_label.height()))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame in the QLabel
        self.current_frame = frame
        self.update_frame()

    def confirm_roi(self):
        self.coordinates_label.setText(f'ROI Coordinates: {self.line_points_copy}')
        self.update_frame()
        self.start_stop_button.setEnabled(True)

    def toggle_tracking(self):
        if self.tracking:
            self.stop_tracking()
        else:
            self.start_tracking()

    def start_tracking(self):
        self.tracking = True
        self.start_stop_button.setText('Stop Tracking')
        self.roi_button.setEnabled(False)
        self.roi_confirmed = True
        self.track()

    def stop_tracking(self):
        self.tracking = False
        self.start_stop_button.setText('Start Tracking')
        # self.roi_button.setEnabled(True)
        cv2.destroyAllWindows()  # Close the cv2 window

    def track(self):
        detections = self.model.track(self.url, stream=True, classes=[2, 3, 5, 7], tracker='bytetrack.yaml', persist=True, imgsz=(1080,1920))
        
        for result in detections:
            if not self.tracking:
                break
            
            frame = result.orig_img
            dets = sv.Detections.from_yolov8(result)
            dets = dets.filter_by_roi(self.line_points_copy)

            if result.boxes.id is not None:
                dets.tracker_id = result.boxes.id.cpu().numpy().astype(int)

            labels = [
                f"{tracker_id} {self.model.model.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, tracker_id in dets
            ]

            # Annotate the frame with bounding boxes and labels
            frame = self.box_annotator.annotate(scene=frame, detections=dets, labels=labels)

            # Count vehicles based on the tracker ID
            for label in labels:
                info = label.split()
                if info[1] == "car":
                    self.vehicle_counts["car"].add(f"{info[0]} {info[1]}")
                elif info[1] == "motorcycle":
                    self.vehicle_counts["motorcycle"].add(f"{info[0]} {info[1]}")
                elif info[1] == "bus":
                    self.vehicle_counts["bus"].add(f"{info[0]} {info[1]}")
                elif info[1] == "truck":
                    self.vehicle_counts["truck"].add(f"{info[0]} {info[1]}")
                
            self.vehicle_counts["total"] = len(self.vehicle_counts["motorcycle"]) + len(self.vehicle_counts["truck"]) + len(self.vehicle_counts["bus"]) + len(self.vehicle_counts["car"])

            # Check if the date has changed
            if datetime.date.today() != self.current_date:
                # Upload the counts to MongoDB
                self.upload_counts()
                
                # Reset the vehicle counts and update the current date
                self.vehicle_counts = {"car": set(), "motorcycle": set(), "bus": set(), "truck": set()}
                self.current_date = datetime.date.today()

            # Draw the ROI lines on the frame using self.line_points
            pts = np.array(self.line_points_copy, np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            # Display vehicle counts on the frame
            cv2.putText(frame, 
                        f"Car {len(self.vehicle_counts['car'])} Bike {len(self.vehicle_counts['motorcycle'])} "
                        f"Bus {len(self.vehicle_counts['bus'])} Truck {len(self.vehicle_counts['truck'])}",
                        (80, 30), 
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

            # Resize and display the frame in the tracking window
            frame = cv2.resize(frame, (960, 540))
            cv2.imshow("Billboard Genie", frame)
            cv2.waitKey(1)

    def upload_counts(self):
        # Insert the counts into MongoDB
        insert_counts_data(self.email, len(self.vehicle_counts["car"]), len(self.vehicle_counts["motorcycle"]), len(self.vehicle_counts["bus"]), len(self.vehicle_counts["truck"]), self.vehicle_counts["total"], self.current_date)

    def update_frame(self):
        # Update the frame with ROI lines
        frame = self.current_frame.copy()

        if self.current_point_index > 0 or self.roi_confirmed:
            pts = np.array(self.line_points, np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.set_image(qt_image)

    def set_image(self, image):
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.roi_confirmed:
            video_label_x = self.video_label.geometry().x()
            video_label_y = self.video_label.geometry().y()
            adjusted_x = event.x() - video_label_x
            adjusted_y = event.y() - video_label_y
            adjusted_x_copy = event.x()*2 + video_label_x -600
            adjusted_y_copy = event.y()*2 - video_label_y

            # Cycle through the four ROI points
            self.line_points[self.current_point_index] = (adjusted_x, adjusted_y)
            self.current_point_index = (self.current_point_index + 1) % 4
            self.line_points_copy[self.current_point_index_copy] = (adjusted_x_copy, adjusted_y_copy)
            self.current_point_index_copy = (self.current_point_index_copy + 1) % 4

            self.update_frame()

    def exit_app(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to Exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close_application()

    def close_application(self):
        self.tray_icon.hide()
        self.tracking = False
        self.close()
        cv2.destroyAllWindows()
        exit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage('Dashboard', 'Application is running in the background', QSystemTrayIcon.Information, 2000)




class CameraRTSPWindow(QWidget):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.initUI()

    def initUI(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Billboard Genie - Camera RTSP URL')
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

        self.url_label = QLabel('Enter the RTSP URL of your camera:')
        self.url_label.setStyleSheet("margin-left: 500px;")
        self.url_label.setFont(QFont("Palatino Linotype", 12))
        self.url_entry = QLineEdit()
        self.url_entry.setStyleSheet("border-radius: 10px; border: 2px solid gray; padding: 5px; height: 25px; margin-right: 500px; margin-left: 500px;")
        self.url_entry.setFont(QFont("Palatino Linotype", 12))
        center_layout.addWidget(self.url_label)
        center_layout.addWidget(self.url_entry)

        self.connect_button = HoverButton(
            'Connect',
            self,
            default_style="background-color: black; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            hover_style="background-color: #007fff; color: white; border-radius: 10px; padding: 10px; height: 20px; width:324px",
            disabled_style=""
        )
        self.connect_button.setFont(QFont("Palatino Linotype", 12))
        self.connect_button.clicked.connect(self.connect_camera)

        # # Add Go Back Button
        # self.go_back_button = HoverButton(
        #     '< Back',
        #     self,
        #     default_style="background-color: white; color: black; border-radius: 10px;",
        #     hover_style="background-color: white; color: #007fff; border-radius: 10px;",
        #     disabled_style=""
        # )
        # self.go_back_button.setFont(QFont("Palatino Linotype", 12))
        # self.go_back_button.clicked.connect(self.go_back)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.connect_button)
        button_layout.addStretch()
        
        # back_button_layout = QHBoxLayout()
        # back_button_layout.addStretch()
        # back_button_layout.addWidget(self.go_back_button)
        # back_button_layout.addStretch()

        center_layout.addLayout(button_layout)
        # center_layout.addLayout(back_button_layout)

        layout.addLayout(top_bar)
        layout.addStretch(1)
        layout.addLayout(center_layout)
        layout.addStretch(1)

        self.setLayout(layout)
        self.move((width - self.width()) // 2, (height - self.height()) // 2)

    def connect_camera(self):
        rtsp_url = self.url_entry.text()
        if not rtsp_url:
            QMessageBox.warning(self, 'Error', 'Please enter the RTSP URL of your camera.')
            return
        
        rtsp_regex = re.compile(
            r'^(rtsp://)'            # Protocol
            r'(?:(?:[a-zA-Z0-9_.-]+)'# Username
            r'(?:\:(?:[a-zA-Z0-9_.-]+))?@)?'  # Password (optional)
            r'(?:\d{1,3}\.){3}\d{1,3}' # IP address
            r'(?::\d{1,5})?'           # Port (optional)
            r'(?:/[a-zA-Z0-9_.-]+)*$'  # Path (optional)
        )
        
        if re.match(rtsp_regex, rtsp_url) is not None:
            self.dashboard = DashboardWindow(self.email, rtsp_url, self)
            self.dashboard.showMaximized()
            self.close()

        else:
            QMessageBox.critical(self, "Invalid Url", "RTSP URL should be in the format\n(rtsp://username:password@ip-address:port-number/path-of-stream)")
            return
        
        # Implement connection logic here
        # Example:
        # camera_connected = connect_to_camera(rtsp_url)
        # if camera_connected:
        #     self.camera_window = CameraFeedWindow(rtsp_url, self)
        #     self.camera_window.showMaximized()
        #     self.close()
        # else:
        #     QMessageBox.warning(self, 'Error', 'Failed to connect to camera. Please check the URL and try again.')

    def go_back(self):
        self.previous_window.showMaximized()
        self.close()

