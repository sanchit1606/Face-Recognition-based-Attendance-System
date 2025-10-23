############################################# CORE LOGIC MODULE ################################################
import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import tkinter.messagebox as mess

class AttendanceSystem:
    def __init__(self):
        self.recognizer = None
        self.face_cascade = None
        self.camera = None
        self.is_attendance_active = False
        self.current_session = None
        self.setup_directories()
        self.load_face_recognizer()
        
    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            "TrainingImage",
            "TrainingImageLabel", 
            "StudentDetails",
            "Attendance",
            "StudentProfiles"
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
    def check_haarcascade_file(self):
        """Check if haarcascade file exists"""
        if not os.path.isfile("haarcascade_frontalface_default.xml"):
            mess.showerror("Missing File", "haarcascade_frontalface_default.xml not found!")
            return False
        return True
        
    def load_face_recognizer(self):
        """Load or create face recognizer"""
        try:
            self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            # Try different ways to create the face recognizer
            try:
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            except AttributeError:
                try:
                    self.recognizer = cv2.face_LBPHFaceRecognizer.create()
                except AttributeError:
                    print("Warning: Face recognition not available. Please install opencv-contrib-python")
                    self.recognizer = None
                    return False
            
            # Try to load existing trained model
            if self.recognizer and os.path.isfile("TrainingImageLabel/Trainner.yml"):
                self.recognizer.read("TrainingImageLabel/Trainner.yml")
                return True
            return False
        except Exception as e:
            print(f"Error loading face recognizer: {e}")
            return False
            
    def get_next_serial_number(self):
        """Get next serial number for student registration"""
        csv_file = "StudentDetails/StudentDetails.csv"
        if os.path.isfile(csv_file):
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                return len(rows)  # Return next serial number
        return 1
        
    def take_student_images(self, prn, first_name, last_name, gender, dob, roll_number, email, phone, department, course, year, semester):
        """Take face images for student registration"""
        if not self.check_haarcascade_file():
            return "Error: Missing haarcascade file"
            
        # Validate inputs
        if not all([prn, first_name, last_name, gender, dob, roll_number, email, phone, department, course, year, semester]):
            return "Error: All fields are required"
            
        # Check if student already exists
        if self.student_exists(prn):
            return "Error: Student with this PRN already exists"
            
        # Get next serial number
        serial = self.get_next_serial_number()
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            return "Error: Could not access camera"
            
        sample_count = 0
        max_samples = 100
        
        try:
            while sample_count < max_samples:
                ret, frame = self.camera.read()
                if not ret:
                    break
                    
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sample_count += 1
                    
                    # Save face image
                    face_img = gray[y:y + h, x:x + w]
                    filename = f"TrainingImage/{first_name}_{last_name}_{serial}_{prn}_{sample_count}.jpg"
                    cv2.imwrite(filename, face_img)
                    
                    # Display progress
                    cv2.putText(frame, f"Sample: {sample_count}/{max_samples}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Taking Images - Press Q to quit', frame)
                
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                    
            # Save student details
            self.save_student_details(serial, prn, first_name, last_name, gender, dob, roll_number, email, phone, department, course, year, semester)
            
            return f"Successfully captured {sample_count} images for {first_name} {last_name}"
            
        except Exception as e:
            return f"Error taking images: {str(e)}"
        finally:
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            
    def save_student_details(self, serial, prn, first_name, last_name, gender, dob, roll_number, email, phone, department, course, year, semester):
        """Save student details to CSV"""
        csv_file = "StudentDetails/StudentDetails.csv"
        
        # Create CSV with headers if it doesn't exist
        if not os.path.isfile(csv_file):
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Serial', 'PRN', 'First Name', 'Last Name', 'Gender', 
                               'Date of Birth', 'Roll Number', 'Email', 'Phone Number',
                               'Department', 'Course', 'Year', 'Semester', 'Registration Date'])
        
        # Add student record
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([serial, prn, first_name, last_name, gender, dob, roll_number, 
                           email, phone, department, course, year, semester, 
                           datetime.datetime.now().strftime('%d/%m/%Y')])
                           
    def student_exists(self, prn):
        """Check if student already exists"""
        csv_file = "StudentDetails/StudentDetails.csv"
        if os.path.isfile(csv_file):
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 1 and row[1] == prn:
                        return True
        return False
        
    def save_student_profile(self):
        """Train and save the face recognition model"""
        try:
            faces, ids = self.get_images_and_labels("TrainingImage")
            if len(faces) == 0:
                return "Error: No training images found. Please take images first."
                
            self.recognizer.train(faces, np.array(ids))
            self.recognizer.save("TrainingImageLabel/Trainner.yml")
            
            return f"Profile saved successfully! Trained on {len(faces)} images."
            
        except Exception as e:
            return f"Error saving profile: {str(e)}"
            
    def get_images_and_labels(self, path):
        """Get images and labels for training"""
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        faces = []
        ids = []
        
        for image_path in image_paths:
            try:
                # Load image
                pil_image = Image.open(image_path).convert('L')
                image_np = np.array(pil_image, 'uint8')
                
                # Extract ID from filename (format: name_serial_prn_sample.jpg)
                filename = os.path.basename(image_path)
                id_part = filename.split('_')[2]  # Get serial number
                face_id = int(id_part)
                
                faces.append(image_np)
                ids.append(face_id)
                
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
                continue
                
        return faces, ids
        
    def start_attendance(self, subject, faculty, date, time):
        """Start attendance session"""
        if not self.check_haarcascade_file():
            return "Error: Missing haarcascade file"
            
        if not self.recognizer or not os.path.isfile("TrainingImageLabel/Trainner.yml"):
            return "Error: No trained model found. Please train the system first."
            
        # Validate inputs
        if not all([subject, faculty, date, time]):
            return "Error: All session details are required"
            
        # Create session record
        self.current_session = {
            'subject': subject,
            'faculty': faculty,
            'date': date,
            'time': time,
            'start_time': datetime.datetime.now(),
            'attended_students': set()
        }
        
        self.is_attendance_active = True
        
        # Start camera for attendance
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            return "Error: Could not access camera"
            
        try:
            while self.is_attendance_active:
                ret, frame = self.camera.read()
                if not ret:
                    break
                    
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.2, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Recognize face
                    face_roi = gray[y:y + h, x:x + w]
                    try:
                        id, confidence = self.recognizer.predict(face_roi)
                        
                        if confidence < 50:  # Lower confidence = better match
                            student_info = self.get_student_info(id)
                            if student_info:
                                # Get student ID with flexible column mapping
                                student_id = student_info.get('PRN', student_info.get('ID', str(id)))
                                if student_id not in self.current_session['attended_students']:
                                    self.current_session['attended_students'].add(student_id)
                                    self.record_attendance(student_info, subject, faculty, date, time)
                                    
                                # Display name with flexible column mapping
                                first_name = student_info.get('First Name', student_info.get('NAME', 'Unknown'))
                                last_name = student_info.get('Last Name', '')
                                display_name = f"{first_name} {last_name}".strip()
                                
                                cv2.putText(frame, display_name, 
                                           (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                cv2.putText(frame, f"ID: {student_id}", 
                                           (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                            else:
                                cv2.putText(frame, "Unknown Student", (x, y - 10), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        else:
                            cv2.putText(frame, "Low Confidence", (x, y - 10), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    except Exception as e:
                        print(f"Error in face recognition: {e}")
                        cv2.putText(frame, "Recognition Error", (x, y - 10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Display session info
                cv2.putText(frame, f"Subject: {subject}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Faculty: {faculty}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Attended: {len(self.current_session['attended_students'])}", (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, "Press Q to stop", (10, frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow('Taking Attendance - Press Q to stop', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            return f"Attendance session completed. {len(self.current_session['attended_students'])} students attended."
            
        except Exception as e:
            return f"Error during attendance: {str(e)}"
        finally:
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            self.is_attendance_active = False
            
    def stop_attendance(self):
        """Stop the attendance session"""
        self.is_attendance_active = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        return "Attendance session stopped"
        
    def get_student_info(self, serial_id):
        """Get student information by serial ID"""
        csv_file = "StudentDetails/StudentDetails.csv"
        if os.path.isfile(csv_file):
            try:
                with open(csv_file, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Try different possible column names for serial
                        serial_key = None
                        for key in ['Serial', 'SERIAL NO.', 'serial', 'SERIAL']:
                            if key in row and row[key].strip():
                                serial_key = key
                                break
                        
                        if serial_key and int(row[serial_key]) == serial_id:
                            return row
            except Exception as e:
                print(f"Error reading student info: {e}")
                return None
        return None
        
    def record_attendance(self, student_info, subject, faculty, date, time):
        """Record attendance in CSV file"""
        attendance_file = f"Attendance/Attendance_{date.replace('/', '_')}.csv"
        
        # Create attendance file with headers if it doesn't exist
        if not os.path.isfile(attendance_file):
            with open(attendance_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['PRN', 'First Name', 'Last Name', 'Subject', 'Faculty', 
                               'Date', 'Time', 'Department', 'Year'])
        
        # Add attendance record with flexible column mapping
        try:
            with open(attendance_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    student_info.get('PRN', student_info.get('ID', '')),
                    student_info.get('First Name', student_info.get('NAME', '')),
                    student_info.get('Last Name', ''),
                    subject,
                    faculty,
                    date,
                    time,
                    student_info.get('Department', ''),
                    student_info.get('Year', '')
                ])
        except Exception as e:
            print(f"Error recording attendance: {e}")
            
    def get_attendance_records(self, date=None, subject=None):
        """Get attendance records with optional filters"""
        records = []
        
        # If no date specified, use today
        if not date:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            
        attendance_file = f"Attendance/Attendance_{date.replace('/', '_')}.csv"
        
        if os.path.isfile(attendance_file):
            with open(attendance_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Apply subject filter if specified
                    if subject and subject != "All" and row.get('Subject', '') != subject:
                        continue
                        
                    records.append([
                        row.get('PRN', ''),
                        f"{row.get('First Name', '')} {row.get('Last Name', '')}",
                        row.get('Subject', ''),
                        row.get('Faculty', ''),
                        row.get('Date', ''),
                        row.get('Time', ''),
                        'Present'
                    ])
                    
        return records
        
    def get_statistics(self):
        """Get system statistics"""
        stats = {
            'total_students': 0,
            'total_subjects': 0,
            'todays_attendance': 0,
            'attendance_rate': 0
        }
        
        # Count total students
        csv_file = "StudentDetails/StudentDetails.csv"
        if os.path.isfile(csv_file):
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                stats['total_students'] = len(list(reader)) - 1  # Subtract header
        
        # Count today's attendance
        today = datetime.datetime.now().strftime('%d/%m/%Y')
        today_records = self.get_attendance_records(today)
        stats['todays_attendance'] = len(today_records)
        
        # Calculate attendance rate (simplified)
        if stats['total_students'] > 0:
            stats['attendance_rate'] = round((stats['todays_attendance'] / stats['total_students']) * 100, 1)
            
        # Count unique subjects
        subjects = set()
        for record in today_records:
            if len(record) > 2:
                subjects.add(record[2])
        stats['total_subjects'] = len(subjects)
        
        return stats
        
    def export_attendance_report(self, date, format='csv'):
        """Export attendance report"""
        records = self.get_attendance_records(date)
        
        if format.lower() == 'csv':
            filename = f"Reports/Attendance_Report_{date.replace('/', '_')}.csv"
            os.makedirs("Reports", exist_ok=True)
            
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['PRN', 'Name', 'Subject', 'Faculty', 'Date', 'Time', 'Status'])
                writer.writerows(records)
                
            return f"Report exported to {filename}"
        else:
            return "Only CSV format is currently supported"
            
    def get_student_attendance_summary(self, prn):
        """Get attendance summary for a specific student"""
        summary = {
            'total_days': 0,
            'present_days': 0,
            'attendance_percentage': 0,
            'subjects': {}
        }
        
        # This would require more complex logic to track all attendance files
        # For now, return basic structure
        return summary
