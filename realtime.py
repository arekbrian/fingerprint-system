# import tkinter as tk
# from tkinter import messagebox, scrolledtext, simpledialog
# import cv2
# import requests
# import pytesseract
# import random
# import time
# import json
# import os

# # -----------------------------------------------------------------------------
# # Database Functions (Simulated with a JSON file)
# # -----------------------------------------------------------------------------
# DATABASE_FILE = "fingerprint_db.json"


# def load_registered_fingerprints():
#     if os.path.exists(DATABASE_FILE):
#          with open(DATABASE_FILE, "r") as f:
#             return json.load(f)
#     else:
#         return {}


# def save_registered_fingerprints(db):
#     with open(DATABASE_FILE, "w") as f:
#         json.dump(db, f)


# # -----------------------------------------------------------------------------
# # Global Settings & Registries
# # -----------------------------------------------------------------------------
# ADMIN_PASSWORD = "admin123"
# # registered_fingerprints: key = student_id, value = {"name": student_name, "token": fingerprint_token}
# registered_fingerprints = load_registered_fingerprints()

# # Simulated Student Database (fallback if needed)
# STUDENT_DATABASE = {
#     "S1001": "Shadrack Njuguna",
#     "S1002": "Ray",
#     "S1003": "Carol Lee",
#     "S1004": "David Kim",
# }

# # Global Attendance Records List
# attendance_records = []  # Each record: {"id": student_id, "name": student_name, "time": timestamp, "method": method}

# # -----------------------------------------------------------------------------
# # API Endpoints (Simulated for demonstration)
# # -----------------------------------------------------------------------------
# API_BASE_URL = "http://localhost:5000/api"
# ATTENDANCE_REPORT_API = f"{API_BASE_URL}/attendance-report"


# # -----------------------------------------------------------------------------
# # Fingerprint Sensor Simulation Functions
# # -----------------------------------------------------------------------------
# def simulate_admin_fingerprint_scan():
#     """
#     Simulate fingerprint capture during registration.
#     In a real system, this would capture actual fingerprint data.
#     """
#     messagebox.showinfo("Fingerprint Capture", "Please scan the student's finger now.")
#     root.update()  # Refresh UI
#     time.sleep(2)  # Simulate scanning delay
#     return f"fingerprint_{random.randint(1000, 9999)}"


# def simulate_student_fingerprint_scan():
#     """
#     Simulate the fingerprint scanning process for a student.
#     Instead of randomly selecting a registered record, this function now
#     prompts the student to enter the fingerprint token (as captured during registration).
#     This allows a deterministic matching process.
#     """
#     scanned_token = simpledialog.askstring("Fingerprint Scan",
#                                            "Please place your finger on the sensor.\nFor simulation, enter your fingerprint token:")
#     if scanned_token:
#         for student_id, data in registered_fingerprints.items():
#             if data["token"] == scanned_token:
#                 return scanned_token, student_id
#     return None, None


# def authenticate_fingerprint():
#     """
#     Simulate fingerprint authentication for attendance.
#     The student is prompted (via the simulated sensor) to enter the token.
#     If the token matches a registered record, attendance is recorded.
#     """
#     scanned_token, student_id = simulate_student_fingerprint_scan()
#     if scanned_token is not None and student_id is not None:
#         student_info = registered_fingerprints[student_id]
#         student_name = student_info["name"]
#         messagebox.showinfo("Fingerprint Verified",
#                             f"Fingerprint recognized for {student_name} (ID: {student_id}).")
#         mark_attendance(student_id, student_name, method="Fingerprint")
#     else:
#         messagebox.showerror("Fingerprint Error",
#                              "Fingerprint not recognized. Please register with the admin if you haven't already.")


# def verify_fingerprint():
#     """
#     Called when a student wants to record attendance via fingerprint.
#     """
#     authenticate_fingerprint()


# # -----------------------------------------------------------------------------
# # Admin Fingerprint Registration Functions
# # -----------------------------------------------------------------------------
# def admin_register_fingerprint():
#     """
#     Allows the admin to register a student's fingerprint.
#     The admin must enter the password, then the student's details.
#     The admin then prompts the system to scan the student's fingerprint,
#     and the record is stored persistently in a JSON file.
#     """
#     pwd = simpledialog.askstring("Admin Authentication", "Enter admin password:", show="*")
#     if pwd != ADMIN_PASSWORD:
#         messagebox.showerror("Authentication Failed", "Incorrect admin password.")
#         return

#     # Create a registration window.
#     reg_window = tk.Toplevel(root)
#     reg_window.title("Fingerprint Registration")
#     reg_window.geometry("400x350")

#     tk.Label(reg_window, text="Register Student Fingerprint", font=font_title).pack(pady=10)

#     tk.Label(reg_window, text="Student ID:", font=font_entry).pack(pady=5)
#     entry_student_id = tk.Entry(reg_window, font=font_entry)
#     entry_student_id.pack(pady=5)

#     tk.Label(reg_window, text="Student Name:", font=font_entry).pack(pady=5)
#     entry_student_name = tk.Entry(reg_window, font=font_entry)
#     entry_student_name.pack(pady=5)

#     # Dictionary to hold the captured fingerprint token.
#     captured_token = {"token": None}

#     def scan_fingerprint():
#         token = simulate_admin_fingerprint_scan()
#         captured_token["token"] = token
#         messagebox.showinfo("Fingerprint Captured", f"Fingerprint token captured: {token}")

#     def register_student():
#         student_id = entry_student_id.get().strip()
#         student_name = entry_student_name.get().strip()
#         token = captured_token["token"]
#         if not student_id or not student_name:
#             messagebox.showerror("Input Error", "Please enter both student ID and name.")
#             return
#         if not token:
#             messagebox.showerror("Fingerprint Not Captured", "Please scan the fingerprint first.")
#             return
#         # Save record in the in-memory database and persist it.
#         registered_fingerprints[student_id] = {"name": student_name, "token": token}
#         save_registered_fingerprints(registered_fingerprints)
#         messagebox.showinfo("Registration Successful",
#                             f"Fingerprint registered for {student_name} (ID: {student_id}).\nToken: {token}")
#         reg_window.destroy()

#     tk.Button(reg_window, text="Scan Fingerprint", font=font_button, bg=button_bg, fg=button_fg,
#               command=scan_fingerprint).pack(pady=15)
#     tk.Button(reg_window, text="Register Student", font=font_button, bg=button_bg, fg=button_fg,
#               command=register_student).pack(pady=10)


# # -----------------------------------------------------------------------------
# # ID Card Camera Scan Functions (with OCR)
# # -----------------------------------------------------------------------------
# def scan_id_with_camera():
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     if not cap.isOpened():
#         messagebox.showerror("Camera Error", "Unable to access the camera.")
#         return

#     messagebox.showinfo("ID Camera Scanner", "Press 's' to scan your ID, or 'q' to cancel.")
#     captured_frame = None

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         cv2.imshow("ID Card Scanner - Press 's' to scan", frame)
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('s'):
#             captured_frame = frame.copy()
#             break
#         elif key == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     if captured_frame is not None:
#         process_id_camera_scan(captured_frame)
#     else:
#         messagebox.showinfo("Cancelled", "ID scanning cancelled.")


# def process_id_camera_scan(image):
#     try:
#         ocr_text = pytesseract.image_to_string(image)
#     except Exception as e:
#         messagebox.showerror("OCR Error", f"Tesseract OCR error: {e}\n"
#                                           "Please ensure Tesseract is installed and in your PATH.")
#         return

#     lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
#     if lines:
#         student_name = lines[0]
#         student_id = "Unknown"  # Extend OCR logic as needed.
#         messagebox.showinfo("ID Scanned",
#                             f"ID card recognized:\nName: {student_name}\nID: {student_id}")
#         mark_attendance(student_id, student_name, method="ID Camera Scan")
#     else:
#         messagebox.showerror("Scan Failed", "No text recognized on the ID. Please try again.")


# # -----------------------------------------------------------------------------
# # Attendance Recording Functions
# # -----------------------------------------------------------------------------
# def mark_attendance(student_id, student_name, method):
#     timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#     record = {"id": student_id, "name": student_name, "time": timestamp, "method": method}
#     attendance_records.append(record)

#     # Attempt to post the record to the backend API.
#     try:
#         response = requests.post(ATTENDANCE_REPORT_API, json=record)
#         if response.status_code == 200:
#             messagebox.showinfo("Attendance Recorded",
#                                 f"Attendance marked for {student_name} at {timestamp}.")
#         else:
#             messagebox.showerror("Server Error", "Failed to record attendance on the server.")
#     except Exception as e:
#         # If the API call fails, log and notify but still update locally.
#         print(f"API call failed: {e}")
#         messagebox.showinfo("Attendance Recorded",
#                             f"Attendance marked locally for {student_name} at {timestamp}.")

#     update_attendance_report()


# def update_attendance_report():
#     attendance_text.config(state=tk.NORMAL)
#     attendance_text.delete("1.0", tk.END)
#     if not attendance_records:
#         attendance_text.insert(tk.END, "No attendance records available.")
#     else:
#         for record in attendance_records:
#             line = f"{record['time']} - {record['name']} (ID: {record['id']}) via {record['method']}\n"
#             attendance_text.insert(tk.END, line)
#     attendance_text.config(state=tk.DISABLED)


# # -----------------------------------------------------------------------------
# # Navigation Functions
# # -----------------------------------------------------------------------------
# def hide_all_frames():
#     for frame in (frame_fingerprint, frame_id_camera, frame_attendance_report):
#         frame.pack_forget()


# def show_fingerprint_frame():
#     hide_all_frames()
#     frame_fingerprint.pack(pady=20, fill=tk.BOTH, expand=True)


# def show_id_camera_frame():
#     hide_all_frames()
#     frame_id_camera.pack(pady=20, fill=tk.BOTH, expand=True)


# def show_attendance_report_frame():
#     hide_all_frames()
#     frame_attendance_report.pack(pady=20, fill=tk.BOTH, expand=True)
#     update_attendance_report()


# # -----------------------------------------------------------------------------
# # Main Window Setup
# # -----------------------------------------------------------------------------
# root = tk.Tk()
# root.title("Real-Time Student Attendance System")
# root.geometry("1000x600")
# root.configure(bg="darkblue")

# # -----------------------------------------------------------------------------
# # Style Settings
# # -----------------------------------------------------------------------------
# font_title = ("Helvetica", 18, "bold")
# font_header = ("Helvetica", 24, "bold")
# font_entry = ("Helvetica", 12)
# font_button = ("Helvetica", 12, "bold")
# button_bg = "#4CAF50"
# button_fg = "white"

# # -----------------------------------------------------------------------------
# # Main Dashboard Frame
# # -----------------------------------------------------------------------------
# frame_dashboard = tk.Frame(root, bg="darkblue")
# frame_dashboard.pack(fill=tk.BOTH, expand=True)

# header_label = tk.Label(frame_dashboard, text="Real-Time Student Attendance System",
#                         font=font_header, bg="darkblue", fg="white")
# header_label.pack(pady=20)

# # -----------------------------------------------------------------------------
# # Navigation Bar
# # -----------------------------------------------------------------------------
# frame_nav = tk.Frame(frame_dashboard, bg="darkblue")
# frame_nav.pack(pady=10)

# btn_fingerprint = tk.Button(frame_nav, text="Fingerprint Sensor",
#                             command=show_fingerprint_frame, font=font_button, bg=button_bg, fg=button_fg)
# btn_id_camera = tk.Button(frame_nav, text="Scan ID with Camera",
#                           command=show_id_camera_frame, font=font_button, bg=button_bg, fg=button_fg)
# btn_attendance_report = tk.Button(frame_nav, text="Attendance Report",
#                                   command=show_attendance_report_frame, font=font_button, bg=button_bg, fg=button_fg)
# btn_admin_register = tk.Button(frame_nav, text="Admin Registration",
#                                command=admin_register_fingerprint, font=font_button, bg=button_bg, fg=button_fg)

# btn_fingerprint.pack(side=tk.LEFT, padx=10)
# btn_id_camera.pack(side=tk.LEFT, padx=10)
# btn_attendance_report.pack(side=tk.LEFT, padx=10)
# btn_admin_register.pack(side=tk.LEFT, padx=10)

# # -----------------------------------------------------------------------------
# # Frame Definitions
# # -----------------------------------------------------------------------------

# # Fingerprint Sensor Frame
# frame_fingerprint = tk.Frame(frame_dashboard, bg="#1E1E1E", bd=2, relief="groove")
# label_fingerprint = tk.Label(frame_fingerprint, text="Fingerprint Sensor",
#                              font=font_title, bg="#1E1E1E", fg="white")
# label_fingerprint.pack(pady=10)
# # Display a simulated fingerprint icon.
# canvas_fingerprint = tk.Canvas(frame_fingerprint, width=200, height=200, bg="white")
# canvas_fingerprint.create_text(100, 100, text="Fingerprint\nSensor", fill="gray", font=("Helvetica", 12))
# canvas_fingerprint.pack(pady=10)
# btn_scan_fingerprint = tk.Button(frame_fingerprint, text="Scan Fingerprint",
#                                  font=font_button, bg=button_bg, fg=button_fg, command=verify_fingerprint)
# btn_scan_fingerprint.pack(pady=20)

# # ID Camera Scan Frame
# frame_id_camera = tk.Frame(frame_dashboard, bg="#1E1E1E", bd=2, relief="groove")
# label_id_camera = tk.Label(frame_id_camera, text="ID Card Scanner (Camera)",
#                            font=font_title, bg="#1E1E1E", fg="white")
# label_id_camera.pack(pady=10)
# label_camera_info = tk.Label(frame_id_camera, text="Your laptop camera will activate to scan your ID card.",
#                              font=font_entry, bg="#1E1E1E", fg="white")
# label_camera_info.pack(pady=5)
# btn_scan_id_camera = tk.Button(frame_id_camera, text="Scan ID with Camera",
#                                font=font_button, bg=button_bg, fg=button_fg, command=scan_id_with_camera)
# btn_scan_id_camera.pack(pady=20)

# # Attendance Report Frame
# frame_attendance_report = tk.Frame(frame_dashboard, bg="#1E1E1E", bd=2, relief="groove")
# label_attendance_report = tk.Label(frame_attendance_report, text="Attendance Report",
#                                    font=font_title, bg="#1E1E1E", fg="white")
# label_attendance_report.pack(pady=10)
# attendance_text = scrolledtext.ScrolledText(frame_attendance_report, wrap=tk.WORD,
#                                             font=font_entry, bg="white", fg="black", height=15, state=tk.DISABLED)
# attendance_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# # -----------------------------------------------------------------------------
# # Show Default Frame (Fingerprint Sensor)
# # -----------------------------------------------------------------------------
# show_fingerprint_frame()

# root.mainloop()


# import tkinter as tk
# from tkinter import simpledialog, messagebox
# import json
# import os
# from datetime import datetime

# # Simulate the fingerprint scanning
# def simulate_admin_fingerprint_scan():
#     import random
#     return f"fingerprint_{random.randint(1000, 9999)}"

# # Initialize the window
# root = tk.Tk()
# root.title("Attendance System")
# root.geometry("400x300")

# # Registered fingerprints dictionary
# registered_fingerprints = {}

# # Load registered fingerprints from file
# def load_registered_fingerprints():
#     global registered_fingerprints
#     if os.path.exists("fingerprints.json"):
#         with open("fingerprints.json", "r") as f:
#             registered_fingerprints = json.load(f)
#     else:
#         registered_fingerprints = {}

# # Save registered fingerprints to file
# def save_registered_fingerprints(fingerprints):
#     with open("fingerprints.json", "w") as f:
#         json.dump(fingerprints, f)

# # Load attendance records from file
# def load_attendance_records():
#     if os.path.exists("attendance.json"):
#         with open("attendance.json", "r") as f:
#             return json.load(f)
#     else:
#         return {}

# # Save attendance records to file
# def save_attendance_records(attendance_records):
#     with open("attendance.json", "w") as f:
#         json.dump(attendance_records, f)

# # Admin Fingerprint Registration
# def admin_register_fingerprint():
#     pwd = simpledialog.askstring("Admin Password", "Enter admin password:", show="*")
#     if pwd != "admin123":
#         messagebox.showerror("Error", "Incorrect admin password.")
#         return

#     student_id = simpledialog.askstring("Student Registration", "Enter Student ID:")
    
#     # Check if student ID is already registered
#     if student_id in registered_fingerprints:
#         messagebox.showerror("Error", "This Student ID is already registered.")
#         return
    
#     student_name = simpledialog.askstring("Student Registration", "Enter Student Name:")
    
#     if student_id and student_name:
#         token = simulate_admin_fingerprint_scan()
#         registered_fingerprints[student_id] = {"name": student_name, "token": token}
#         save_registered_fingerprints(registered_fingerprints)

#         # Display the fingerprint token to the admin
#         messagebox.showinfo("Registration", f"Fingerprint registered for {student_name}.\nFingerprint Token: {token}")

#         print(f"Student ID: {student_id}, Name: {student_name}, Token: {token}")
#     else:
#         messagebox.showerror("Error", "Student ID and Name cannot be empty.")

# # Check if the student has already marked attendance today
# def has_already_attended_today(student_id):
#     attendance_records = load_attendance_records()
#     today_date = datetime.now().strftime("%Y-%m-%d")

#     if student_id in attendance_records:
#         for record in attendance_records[student_id]:
#             if record['time'].startswith(today_date):
#                 return True
#     return False

# # Mark attendance and record time
# def mark_attendance():
#     student_id = simpledialog.askstring("Attendance", "Enter Student ID:")
#     token = simpledialog.askstring("Attendance", "Enter Fingerprint Token:")
    
#     if student_id in registered_fingerprints:
#         if registered_fingerprints[student_id]["token"] == token:
#             # Check if the student has already marked attendance today
#             if has_already_attended_today(student_id):
#                 messagebox.showwarning("Warning", f"Attendance for {registered_fingerprints[student_id]['name']} has already been marked today.")
#                 return
            
#             # Record the time of attendance
#             current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             attendance_records = load_attendance_records()

#             # Save attendance time
#             if student_id not in attendance_records:
#                 attendance_records[student_id] = []
#             attendance_records[student_id].append({
#                 "name": registered_fingerprints[student_id]["name"],
#                 "time": current_time
#             })
#             save_attendance_records(attendance_records)

#             messagebox.showinfo("Attendance", f"Attendance marked for {registered_fingerprints[student_id]['name']} at {current_time}.")
#         else:
#             messagebox.showerror("Error", "Fingerprint token does not match.")
#     else:
#         messagebox.showerror("Error", "Student not registered.")

# # Generate attendance report (admin only)
# def generate_report():
#     pwd = simpledialog.askstring("Admin Password", "Enter admin password to generate the report:", show="*")
#     if pwd == "admin123":
#         attendance_records = load_attendance_records()
#         if attendance_records:
#             report_window = tk.Toplevel(root)
#             report_window.title("Attendance Report")
#             report_window.geometry("400x300")

#             report_text = tk.Text(report_window)
#             report_text.pack(expand=True, fill='both')

#             for student_id, records in attendance_records.items():
#                 report_text.insert(tk.END, f"Student ID: {student_id}, Name: {records[0]['name']}\n")
#                 for record in records:
#                     report_text.insert(tk.END, f"  - Attended at: {record['time']}\n")
#                 report_text.insert(tk.END, "\n")
#         else:
#             messagebox.showinfo("Report", "No attendance records found.")
#     else:
#         messagebox.showerror("Error", "Incorrect admin password.")

# # Create buttons for admin registration, attendance, and report generation
# register_button = tk.Button(root, text="Register Fingerprint (Admin)", command=admin_register_fingerprint)
# register_button.pack(pady=10)

# attendance_button = tk.Button(root, text="Mark Attendance", command=mark_attendance)
# attendance_button.pack(pady=10)

# report_button = tk.Button(root, text="Generate Attendance Report (Admin)", command=generate_report)
# report_button.pack(pady=10)

# # Load fingerprints on startup
# load_registered_fingerprints()

# root.mainloop()


# import tkinter as tk
# from tkinter import simpledialog, messagebox
# import json
# import os
# from datetime import datetime
# import cv2
# import pytesseract

# # Point pytesseract to the location of the Tesseract executable (modify based on your system)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your installation path

# # Simulate fingerprint scanning
# def simulate_admin_fingerprint_scan():
#     import random
#     return f"fingerprint_{random.randint(1000, 9999)}"

# # Initialize the window
# root = tk.Tk()
# root.title("Smart Attendance System")
# root.geometry("500x400")
# root.config(bg="#F0F0F0")  # Background color

# registered_fingerprints = {}

# # Load registered fingerprints
# def load_registered_fingerprints():
#     global registered_fingerprints
#     if os.path.exists("fingerprints.json"):
#         with open("fingerprints.json", "r") as f:
#             registered_fingerprints = json.load(f)
#     else:
#         registered_fingerprints = {}

# # Save fingerprints
# def save_registered_fingerprints(fingerprints):
#     with open("fingerprints.json", "w") as f:
#         json.dump(fingerprints, f)

# # Load attendance records
# def load_attendance_records():
#     if os.path.exists("attendance.json"):
#         with open("attendance.json", "r") as f:
#             return json.load(f)
#     else:
#         return {}

# # Save attendance records
# def save_attendance_records(attendance_records):
#     with open("attendance.json", "w") as f:
#         json.dump(attendance_records, f)

# # Admin registration for fingerprints
# def admin_register_fingerprint():
#     pwd = simpledialog.askstring("Admin Password", "Enter admin password:", show="*")
#     if pwd != "admin123":
#         messagebox.showerror("Error", "Incorrect admin password.")
#         return

#     student_id = simpledialog.askstring("Student Registration", "Enter Student ID:")
    
#     # Check if the student ID is already registered
#     if student_id in registered_fingerprints:
#         messagebox.showerror("Error", "This Student ID is already registered.")
#         return
    
#     student_name = simpledialog.askstring("Student Registration", "Enter Student Name:")
    
#     if student_id and student_name:
#         token = simulate_admin_fingerprint_scan()
#         registered_fingerprints[student_id] = {"name": student_name, "token": token}
#         save_registered_fingerprints(registered_fingerprints)

#         # Display the fingerprint token to the admin
#         messagebox.showinfo("Registration", f"Fingerprint registered for {student_name}.\nFingerprint Token: {token}")

#         print(f"Student ID: {student_id}, Name: {student_name}, Token: {token}")
#     else:
#         messagebox.showerror("Error", "Student ID and Name cannot be empty.")

# # Check if the student already marked attendance today
# def has_already_attended_today(student_id):
#     attendance_records = load_attendance_records()
#     today_date = datetime.now().strftime("%Y-%m-%d")

#     if student_id in attendance_records:
#         for record in attendance_records[student_id]:
#             if record['time'].startswith(today_date):
#                 return True
#     return False

# # Mark attendance with fingerprint or ID scan
# def mark_attendance():
#     student_id = simpledialog.askstring("Attendance", "Enter Student ID or leave blank to scan ID:")
#     if not student_id:
#         student_id = scan_school_id()  # Scan the ID if no input
    
#     if not student_id:
#         messagebox.showerror("Error", "No Student ID detected.")
#         return

#     token = simpledialog.askstring("Attendance", "Enter Fingerprint Token or leave blank if using ID scan:")
    
#     # Check if student is registered
#     if student_id in registered_fingerprints:
#         if registered_fingerprints[student_id]["token"] == token or token == "":
#             if has_already_attended_today(student_id):
#                 messagebox.showwarning("Warning", f"Attendance for {registered_fingerprints[student_id]['name']} has already been marked today.")
#                 return

#             # Record attendance time
#             current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             attendance_records = load_attendance_records()

#             if student_id not in attendance_records:
#                 attendance_records[student_id] = []
#             attendance_records[student_id].append({
#                 "name": registered_fingerprints[student_id]["name"],
#                 "time": current_time
#             })
#             save_attendance_records(attendance_records)

#             messagebox.showinfo("Attendance", f"Attendance marked for {registered_fingerprints[student_id]['name']} at {current_time}.")
#         else:
#             messagebox.showerror("Error", "Fingerprint token does not match.")
#     else:
#         messagebox.showerror("Error", "Student not registered.")

# # Generate attendance report (admin only)
# def generate_report():
#     pwd = simpledialog.askstring("Admin Password", "Enter admin password to generate the report:", show="*")
#     if pwd == "admin123":
#         attendance_records = load_attendance_records()
#         if attendance_records:
#             report_window = tk.Toplevel(root)
#             report_window.title("Attendance Report")
#             report_window.geometry("400x300")
#             report_window.config(bg="#F8F8F8")

#             report_text = tk.Text(report_window, bg="#E8E8E8", padx=10, pady=10)
#             report_text.pack(expand=True, fill='both')

#             for student_id, records in attendance_records.items():
#                 report_text.insert(tk.END, f"Student ID: {student_id}, Name: {records[0]['name']}\n")
#                 for record in records:
#                     report_text.insert(tk.END, f"  - Attended at: {record['time']}\n")
#                 report_text.insert(tk.END, "\n")
#         else:
#             messagebox.showinfo("Report", "No attendance records found.")
#     else:
#         messagebox.showerror("Error", "Incorrect admin password.")

# # Use OpenCV to scan the school ID using the camera
# def scan_school_id():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         messagebox.showerror("Error", "Camera not detected.")
#         return None
    
#     messagebox.showinfo("Info", "Please show your School ID card to the camera.")
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             messagebox.showerror("Error", "Failed to capture image.")
#             return None

#         cv2.imshow("Scan School ID", frame)

#         # Wait for 's' key to be pressed to capture the ID
#         if cv2.waitKey(1) & 0xFF == ord('s'):
#             cv2.imwrite("id_card.png", frame)
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     # Extract text from the ID card image using OCR
#     img = cv2.imread("id_card.png")
#     student_id_text = pytesseract.image_to_string(img)
#     student_id_text = student_id_text.strip().replace("\n", "")
    
#     if student_id_text:
#         return student_id_text
#     else:
#         messagebox.showerror("Error", "Unable to extract text from the ID card.")
#         return None

# # Create a frame for the title and buttons
# frame = tk.Frame(root, bg="#FFFFFF", pady=20)
# frame.pack(fill="both", expand=True)

# # Title label
# title_label = tk.Label(frame, text="Smart Attendance System", font=("Helvetica", 16, "bold"), bg="#FFFFFF")
# title_label.pack(pady=10)

# # Create buttons for admin registration, attendance, and report generation
# register_button = tk.Button(frame, text="Register Fingerprint (Admin)", command=admin_register_fingerprint, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
# register_button.pack(pady=10)

# attendance_button = tk.Button(frame, text="Mark Attendance", command=mark_attendance, font=("Helvetica", 12), bg="#2196F3", fg="white", padx=20, pady=10)
# attendance_button.pack(pady=10)

# report_button = tk.Button(frame, text="Generate Attendance Report (Admin)", command=generate_report, font=("Helvetica", 12), bg="#F44336", fg="white", padx=20, pady=10)
# report_button.pack(pady=10)

# # Load fingerprints on startup
# load_registered_fingerprints()

# root.mainloop()


import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from datetime import datetime
import cv2
import pytesseract

# Point pytesseract to the location of the Tesseract executable (modify based on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your installation path

# Simulate fingerprint scanning
def simulate_admin_fingerprint_scan():
    import random
    return f"fingerprint_{random.randint(1000, 9999)}"

# Initialize the window
root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("500x400")
root.config(bg="#F0F0F0")  # Background color

registered_fingerprints = {}

# Load registered fingerprints
def load_registered_fingerprints():
    global registered_fingerprints
    if os.path.exists("fingerprints.json"):
        with open("fingerprints.json", "r") as f:
            registered_fingerprints = json.load(f)
    else:
        registered_fingerprints = {}

# Save fingerprints
def save_registered_fingerprints(fingerprints):
    with open("fingerprints.json", "w") as f:
        json.dump(fingerprints, f)

# Load attendance records
def load_attendance_records():
    if os.path.exists("attendance.json"):
        with open("attendance.json", "r") as f:
            return json.load(f)
    else:
        return {}

# Save attendance records
def save_attendance_records(attendance_records):
    with open("attendance.json", "w") as f:
        json.dump(attendance_records, f)

# Admin registration for fingerprints
def admin_register_fingerprint():
    pwd = simpledialog.askstring("Admin Password", "Enter admin password:", show="*")
    if pwd != "admin123":
        messagebox.showerror("Error", "Incorrect admin password.")
        return

    student_id = simpledialog.askstring("Student Registration", "Enter Student ID:")
    
    # Check if the student ID is already registered
    if student_id in registered_fingerprints:
        messagebox.showerror("Error", "This Student ID is already registered.")
        return
    
    student_name = simpledialog.askstring("Student Registration", "Enter Student Name:")
    
    if student_id and student_name:
        token = simulate_admin_fingerprint_scan()
        registered_fingerprints[student_id] = {"name": student_name, "token": token}
        save_registered_fingerprints(registered_fingerprints)

        # Display the fingerprint token to the admin
        messagebox.showinfo("Registration", f"Fingerprint registered for {student_name}.\nFingerprint Token: {token}")

        print(f"Student ID: {student_id}, Name: {student_name}, Token: {token}")
    else:
        messagebox.showerror("Error", "Student ID and Name cannot be empty.")

# Check if the student already marked attendance today
def has_already_attended_today(student_id):
    attendance_records = load_attendance_records()
    today_date = datetime.now().strftime("%Y-%m-%d")

    if student_id in attendance_records:
        for record in attendance_records[student_id]:
            if record['time'].startswith(today_date):
                return True
    return False

# Mark attendance with fingerprint or ID scan
def mark_attendance():
    student_id = simpledialog.askstring("Attendance", "Enter Student ID or leave blank to scan ID:")
    if not student_id:
        student_id = scan_school_id()  # Scan the ID if no input
    
    if not student_id:
        messagebox.showerror("Error", "No Student ID detected.")
        return

    token = simpledialog.askstring("Attendance", "Enter Fingerprint Token or leave blank if using ID scan:")
    
    # Check if student is registered
    if student_id in registered_fingerprints:
        if registered_fingerprints[student_id]["token"] == token or token == "":
            if has_already_attended_today(student_id):
                messagebox.showwarning("Warning", f"Attendance for {registered_fingerprints[student_id]['name']} has already been marked today.")
                return

            # Record attendance time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attendance_records = load_attendance_records()

            if student_id not in attendance_records:
                attendance_records[student_id] = []
            attendance_records[student_id].append({
                "name": registered_fingerprints[student_id]["name"],
                "time": current_time
            })
            save_attendance_records(attendance_records)

            messagebox.showinfo("Attendance", f"Attendance marked for {registered_fingerprints[student_id]['name']} at {current_time}.")
        else:
            messagebox.showerror("Error", "Fingerprint token does not match.")
    else:
        messagebox.showerror("Error", "Student not registered.")

# Generate attendance report (admin only)
def generate_report():
    pwd = simpledialog.askstring("Admin Password", "Enter admin password to generate the report:", show="*")
    if pwd == "admin123":
        attendance_records = load_attendance_records()
        if attendance_records:
            report_window = tk.Toplevel(root)
            report_window.title("Attendance Report")
            report_window.geometry("500x400")
            report_window.config(bg="#F0F0F0")

            title_label = tk.Label(report_window, text="Attendance Report", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
            title_label.pack(pady=10)

            canvas = tk.Canvas(report_window)
            scrollbar = tk.Scrollbar(report_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for student_id, records in attendance_records.items():
                student_frame = tk.Frame(scrollable_frame, bg="#E8E8E8", bd=2, relief="solid", padx=5, pady=5)
                student_frame.pack(fill="x", padx=10, pady=5)

                student_label = tk.Label(student_frame, text=f"Student ID: {student_id} - Name: {records[0]['name']}", font=("Helvetica", 12, "bold"), bg="#E8E8E8")
                student_label.pack(anchor="w")

                for record in records:
                    record_label = tk.Label(student_frame, text=f"  - Attended at: {record['time']}", font=("Helvetica", 10), bg="#FFFFFF")
                    record_label.pack(anchor="w", padx=10, pady=2)
        else:
            messagebox.showinfo("Report", "No attendance records found.")
    else:
        messagebox.showerror("Error", "Incorrect admin password.")

# Use OpenCV to scan the school ID using the camera
def scan_school_id():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not detected.")
        return None
    
    messagebox.showinfo("Info", "Please show your School ID card to the camera.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image.")
            return None

        cv2.imshow("Scan School ID", frame)

        # Wait for 's' key to be pressed to capture the ID
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("id_card.png", frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    # Extract text from the ID card image using OCR
    img = cv2.imread("id_card.png")
    student_id_text = pytesseract.image_to_string(img)
    student_id_text = student_id_text.strip().replace("\n", "")
    
    if student_id_text:
        return student_id_text
    else:
        messagebox.showerror("Error", "Unable to extract text from the ID card.")
        return None

# Create a frame for the title and buttons
frame = tk.Frame(root, bg="#FFFFFF", pady=20)
frame.pack(fill="both", expand=True)

# Title label
title_label = tk.Label(frame, text="Smart Attendance System", font=("Helvetica", 16, "bold"), bg="#FFFFFF")
title_label.pack(pady=10)

# Create buttons for admin registration, attendance, and report generation
register_button = tk.Button(frame, text="Register Fingerprint (Admin)", command=admin_register_fingerprint, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
register_button.pack(pady=10)

attendance_button = tk.Button(frame, text="Mark Attendance", command=mark_attendance, font=("Helvetica", 12), bg="#2196F3", fg="white", padx=20, pady=10)
attendance_button.pack(pady=10)

report_button = tk.Button(frame, text="Generate Attendance Report (Admin)", command=generate_report, font=("Helvetica", 12), bg="#FF9800", fg="white", padx=20, pady=10)
report_button.pack(pady=10)

# Load registered fingerprints on startup
load_registered_fingerprints()

# Start the main loop
root.mainloop()
