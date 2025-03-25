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
root.title("Attendance System")
root.geometry("400x300")

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
            report_window.geometry("400x300")

            report_text = tk.Text(report_window)
            report_text.pack(expand=True, fill='both')

            for student_id, records in attendance_records.items():
                report_text.insert(tk.END, f"Student ID: {student_id}, Name: {records[0]['name']}\n")
                for record in records:
                    report_text.insert(tk.END, f"  - Attended at: {record['time']}\n")
                report_text.insert(tk.END, "\n")
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

# Create buttons for admin registration, attendance, and report generation
register_button = tk.Button(root, text="Register Fingerprint (Admin)", command=admin_register_fingerprint)
register_button.pack(pady=10)

attendance_button = tk.Button(root, text="Mark Attendance", command=mark_attendance)
attendance_button.pack(pady=10)

report_button = tk.Button(root, text="Generate Attendance Report (Admin)", command=generate_report)
report_button.pack(pady=10)

# Load fingerprints on startup
load_registered_fingerprints()

root.mainloop()

