# Billboard Genie

Billboard Genie is a comprehensive traffic monitoring and vehicle counting system designed to streamline real-time traffic analysis using a live CCTV stream.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Real-Time Traffic Analysis**: Efficiently captures and processes CCTV footage to identify and count vehicles (Cars, Buses, Trucks, Motorcycles).
- **User Authentication**: Ensures data security by allowing access to dashboard only after login.
- **High Performance**: Utilizes YOLOv8 and ByteTrack for reliable and accurate vehicle detection and tracking.

## Technologies Used

- **Programming Languages**: Python
- **Libraries**: OpenCV, YOLOv8, ByteTrack(Roboflow) and more...
- **Database**: MongoDB

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/billboard-genie.git
   cd billboard-genie
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database (MongoDB):
   - Configure your MongoDB connection details in the application.

4. Run the application:
   ```bash
   python main.py
   ```
   
## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.
