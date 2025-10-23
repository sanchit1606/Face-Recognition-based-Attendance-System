############################################# MAIN LAUNCHER ################################################
"""
Smart Attendance Management System
Main launcher for the face recognition attendance system
"""

import sys
import os
from gui import ModernAttendanceGUI

def main():
    """Main entry point for the application"""
    try:
        # Check if required files exist
        if not os.path.exists("haarcascade_frontalface_default.xml"):
            print("Error: haarcascade_frontalface_default.xml not found!")
            print("Please ensure the haarcascade file is in the same directory as main.py")
            return
        
        # Launch the modern GUI
        print("Starting Face Recognition-based Attendance System...")
        app = ModernAttendanceGUI()
        if app and hasattr(app, 'root'):
            app.run()
        else:
            print("Failed to initialize the application. Please check the error messages above.")
        
    except ImportError as e:
        print(f"Error: Missing required module - {e}")
        print("Please install required packages: pip install opencv-contrib-python pillow pandas numpy")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()