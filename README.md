# Face Recognition-based Attendance System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)

**A simple OpenCV based student attendance system**

[Features](#features) • [Requirements](#requirements) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots) • [Architecture](#architecture)

</div>

---

## Overview

**Face Recognition-Based Attendance System | Computer Vision | 3rd sem, 2023**  
Published in Springer, series: Advances in Information Communication Technology and Computing (AICTC 2024) – Developed a facial recognition attendance system using OpenCV (Haar + LBPH), achieving 90%+ recognition accuracy across 40+ student test cases in varied lighting.

**Research Paper**: [Face Recognition-based Attendance System](https://www.springerprofessional.de/en/face-recognition-based-attendance-system/50070728)


---

## Features

### **User Interface**
- **Dashboard**: Overview with statistics and quick actions
- **Student Registration**: Comprehensive form with personal and academic details
- **Take Attendance**: Real-time face recognition with live camera feed
- **View Attendance**: Filterable attendance records with detailed reports
- **Analytics**: Attendance insights and trends

### **Core Functionality**
- **Face Detection**: Advanced Haar Cascade classifier for accurate face detection
- **Face Recognition**: LBPH (Local Binary Patterns Histograms) algorithm for reliable recognition
- **Data Management**: CSV-based storage for students and attendance records
- **Real-time Processing**: Live camera feed with instant recognition feedback
- **Session Management**: Subject-wise attendance tracking with faculty information

### **Student Management**
- **Comprehensive Registration**: PRN, personal details, academic information
- **Image Capture**: Multiple face images for robust training
- **Profile Management**: Edit and update student information
- **Batch Operations**: Support for multiple student registrations

### **Attendance Analytics**
- **Daily Reports**: Date-wise attendance tracking
- **Subject-wise Analysis**: Attendance by subject and faculty
- **Statistics Dashboard**: Real-time attendance metrics
- **Export Functionality**: CSV export for external analysis

---

## Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.7 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Camera**: USB webcam or built-in camera

### Python Dependencies
```
opencv-contrib-python==4.8.1.78
pillow>=9.0.0
pandas>=1.3.0
numpy==1.26.4
```

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/face-recognition-attendance-system.git
cd face-recognition-attendance-system
```

### 2. Create Virtual Environment (Recommended)
```bash
# Using conda
conda create -n attendance_system python=3.9
conda activate attendance_system

# Or using venv
python -m venv attendance_system
source attendance_system/bin/activate  # On Windows: attendance_system\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python main.py
```

---

## Usage

### Quick Start

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Register Students**
   - Navigate to "Student Registration" tab
   - Fill in student details (Personal & Academic information)
   - Click "Take Face Images" to capture training photos
   - Click "Save Student Profile" to train the recognition model

3. **Take Attendance**
   - Go to "Take Attendance" tab
   - Select subject and enter faculty name
   - Click "Start Face Recognition"
   - Students will be automatically recognized and marked present
   - Press 'Q' to stop the session

4. **View Records**
   - Check "View Attendance" tab for attendance history
   - Use filters to view specific dates or subjects
   - Export data as needed

### Detailed Workflow

#### Student Registration Process
1. **Personal Information**: PRN, Name, Gender, DOB, Roll Number
2. **Academic Information**: Department, Course, Year, Semester, Contact details
3. **Face Training**: Capture multiple images for robust recognition
4. **Model Training**: Automatic training of face recognition model

#### Attendance Taking Process
1. **Session Setup**: Configure subject, faculty, date, and time
2. **Camera Activation**: Real-time face detection and recognition
3. **Automatic Recording**: Attendance marked with timestamp
4. **Session Management**: Start/stop controls with live feedback

---

## Screenshots

### Dashboard
The main dashboard provides an overview of the system with key statistics and quick access to all features.

![Dashboard](assets/Screenshot%20(122).png)
*Dashboard showing system overview, statistics cards, and quick action buttons*

### Student Registration
Comprehensive registration form with two-column layout for personal and academic information.

![Student Registration](assets/Screenshot%20(125).png)
*Student registration form with personal and academic information sections*

![Student Registration Form](assets/Screenshot%20(126).png)
*Registration form with action buttons for image capture and profile saving*

![Profile Saved Successfully](assets/Screenshot%20(127).png)
*Success message after completing student registration and model training*

### Take Attendance
Real-time face recognition system with live camera feed and automatic attendance marking.

![Take Attendance](assets/Screenshot%20(128).png)
*Live face recognition showing detected face, gender, and student identification*

### View Attendance
Attendance records viewer with filtering options and detailed reports.

![View Attendance](assets/Screenshot%20(129).png)
*Attendance records table with filtering options and detailed student information*

---

## Architecture

### Project Structure
```
face-recognition-attendance-system/
├── main.py                 # Application entry point
├── gui.py                  # GUI components and interface
├── core_logic.py           # Core business logic and face recognition
├── requirements.txt        # Python dependencies
├── haarcascade_frontalface_default.xml  # Face detection model
├── assets/                 # Screenshots and documentation
├── StudentDetails/         # Student data storage
│   └── StudentDetails.csv
└── Attendance/            # Attendance records storage
    └── Attendance_*.csv
```

### Technical Architecture

#### **Frontend (GUI Layer)**
- **Framework**: Tkinter with ttk widgets
- **Design**: Modern tabbed interface with responsive layout
- **Components**: Dashboard, Forms, Tables, Real-time displays

#### **Backend (Core Logic)**
- **Face Detection**: OpenCV Haar Cascade Classifier
- **Face Recognition**: LBPH Face Recognizer
- **Data Management**: CSV file operations with pandas
- **Image Processing**: PIL/Pillow for image manipulation

#### **Data Flow**
1. **Registration**: Student data → CSV storage → Image capture → Model training
2. **Recognition**: Camera feed → Face detection → Feature extraction → Recognition → Attendance recording
3. **Reporting**: Data retrieval → Filtering → Display/Export

---

## Configuration

### Camera Settings
- **Resolution**: Auto-detected (recommended: 640x480 or higher)
- **Frame Rate**: 30 FPS (adjustable in code)
- **Detection Sensitivity**: Configurable confidence thresholds

### Recognition Parameters
- **Training Images**: 100 images per student (configurable)
- **Recognition Threshold**: 80% confidence (adjustable)
- **Face Size**: Minimum 100x100 pixels