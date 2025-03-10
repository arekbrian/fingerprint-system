import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import cv2
import requests
import pytesseract
import random
import time
import json
import os

# -----------------------------------------------------------------------------
# Database Functions (Simulated with a JSON file)
# -----------------------------------------------------------------------------
DATABASE_FILE = "fingerprint_db.json"


def load_registered_fingerprints():
    if os.path.exists(DATABASE_FILE):
         with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    else:
        return {}


def save_registered_fingerprints(db):
    with open(DATABASE_FILE, "w") as f:
        json.dump(db, f)


# -----------------------------------------------------------------------------
# Global Settings & Registries
# -----------------------------------------------------------------------------
ADMIN_PASSWORD = "admin123"
# registered_fingerprints: key = student_id, value = {"name": student_name, "token": fingerprint_token}
registered_fingerprints = load_registered_fingerprints()

# Simulated Student Database (fallback if needed)
STUDENT_DATABASE = {
    "S1001": "Shadrack Njuguna",
    "S1002": "Ray",
    "S1003": "Carol Lee",
    "S1004": "David Kim",
}

# Global Attendance Records List
attendance_records = []  # Each record: {"id": student_id, "name": student_name, "time": timestamp, "method": method}

# -----------------------------------------------------------------------------
# API Endpoints (Simulated for demonstration)
# -----------------------------------------------------------------------------
API_BASE_URL = "http://localhost:5000/api"
ATTENDANCE_REPORT_API = f"{API_BASE_URL}/attendance-report"


# -----------------------------------------------------------------------------
# Fingerprint Sensor Simulation Functions
# -----------------------------------------------------------------------------
def simulate_admin_fingerprint_scan():
    """
    Simulate fingerprint capture during registration.
    In a real system, this would capture actual fingerprint data.
    """
    messagebox.showinfo("Fingerprint Capture", "Please scan the student's finger now.")
    root.update()  # Refresh UI
    time.sleep(2)  # Simulate scanning delay
    return f"fingerprint_{random.randint(1000, 9999)}"


def simulate_student_fingerprint_scan():
    """
    Simulate the fingerprint scanning process for a student.
    Instead of randomly selecting a registered record, this function now
    prompts the student to enter the fingerprint token (as captured during registration).
    This allows a deterministic matching process.
    """
    scanned_token = simpledialog.askstring("Fingerprint Scan",
                                           "Please place your finger on the sensor.\nFor simulation, enter your fingerprint token:")
    if scanned_token:
        for student_id, data in registered_fingerprints.items():
            if data["token"] == scanned_token:
                return scanned_token, student_id
    return None, None


def authenticate_fingerprint():
    """
    Simulate fingerprint authentication for attendance.
    The student is prompted (via the simulated sensor) to enter the token.
    If the token matches a registered record, attendance is recorded.
    """
    scanned_token, student_id = simulate_student_fingerprint_scan()
    if scanned_token is not None and student_id is not None:
        student_info = registered_fingerprints[student_id]
        student_name = student_info["name"]
        messagebox.showinfo("Fingerprint Verified",
                            f"Fingerprint recognized for {student_name} (ID: {student_id}).")
        mark_attendance(student_id, student_name, method="Fingerprint")
    else:
        messagebox.showerror("Fingerprint Error",
                             "Fingerprint not recognized. Please register with the admin if you haven't already.")


def verify_fingerprint():
    """
    Called when a student wants to record attendance via fingerprint.
    """
    authenticate_fingerprint()


# -----------------------------------------------------------------------------
# Admin Fingerprint Registration Functions
# -----------------------------------------------------------------------------
def admin_register_fingerprint():
    """
    Allows the admin to register a student's fingerprint.
    The admin must enter the password, then the student's details.
    The admin then prompts the system to scan the student's fingerprint,
    and the record is stored persistently in a JSON file.
    """
    pwd = simpledialog.askstring("Admin Authentication", "Enter admin password:", show="*")
    if pwd != ADMIN_PASSWORD:
        messagebox.showerror("Authentication Failed", "Incorrect admin password.")
        return

    # Create a registration window.
    reg_window = tk.Toplevel(root)
    reg_window.title("Fingerprint Registration")
    reg_window.geometry("400x350")

    tk.Label(reg_window, text="Register Student Fingerprint", font=font_title).pack(pady=10)

    tk.Label(reg_window, text="Student ID:", font=font_entry).pack(pady=5)
    entry_student_id = tk.Entry(reg_window, font=font_entry)
    entry_student_id.pack(pady=5)

    tk.Label(reg_window, text="Student Name:", font=font_entry).pack(pady=5)
    entry_student_name = tk.Entry(reg_window, font=font_entry)
    entry_student_name.pack(pady=5)

    # Dictionary to hold the captured fingerprint token.
    captured_token = {"token": None}

    def scan_fingerprint():
        token = simulate_admin_fingerprint_scan()
        captured_token["token"] = token
        messagebox.showinfo("Fingerprint Captured", f"Fingerprint token captured: {token}")

    def register_student():
        student_id = entry_student_id.get().strip()
        student_name = entry_student_name.get().strip()
        token = captured_token["token"]
        if not student_id or not student_name:
            messagebox.showerror("Input Error", "Please enter both student ID and name.")
            return
        if not token:
            messagebox.showerror("Fingerprint Not Captured", "Please scan the fingerprint first.")
            return
        # Save record in the in-memory database and persist it.
        registered_fingerprints[student_id] = {"name": student_name, "token": token}
        save_registered_fingerprints(registered_fingerprints)
        messagebox.showinfo("Registration Successful",
                            f"Fingerprint registered for {student_name} (ID: {student_id}).\nToken: {token}")
        reg_window.destroy()

    tk.Button(reg_window, text="Scan Fingerprint", font=font_button, bg=button_bg, fg=button_fg,
              command=scan_fingerprint).pack(pady=15)
    tk.Button(reg_window, text="Register Student", font=font_button, bg=button_bg, fg=button_fg,
              command=register_student).pack(pady=10)


# -----------------------------------------------------------------------------
# ID Card Camera Scan Functions (with OCR)
# -----------------------------------------------------------------------------
def scan_id_with_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Unable to access the camera.")
        return

    messagebox.showinfo("ID Camera Scanner", "Press 's' to scan your ID, or 'q' to cancel.")
    captured_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("ID Card Scanner - Press 's' to scan", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            captured_frame = frame.copy()
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured_frame is not None:
        process_id_camera_scan(captured_frame)
    else:
        messagebox.showinfo("Cancelled", "ID scanning cancelled.")


def process_id_camera_scan(image):
    try:
        ocr_text = pytesseract.image_to_string(image)
    except Exception as e:
        messagebox.showerror("OCR Error", f"Tesseract OCR error: {e}\n"
                                          "Please ensure Tesseract is installed and in your PATH.")
        return

    lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
    if lines:
        student_name = lines[0]
        student_id = "Unknown"  # Extend OCR logic as needed.
        messagebox.showinfo("ID Scanned",
                            f"ID card recognized:\nName: {student_name}\nID: {student_id}")
        mark_attendance(student_id, student_name, method="ID Camera Scan")
    else:
        messagebox.showerror("Scan Failed", "No text recognized on the ID. Please try again.")


# -----------------------------------------------------------------------------
# Attendance Recording Functions
# -----------------------------------------------------------------------------
def mark_attendance(student_id, student_name, method):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    record = {"id": student_id, "name": student_name, "time": timestamp, "method": method}
    attendance_records.append(record)

    # Attempt to post the record to the backend API.
    try:
        response = requests.post(ATTENDANCE_REPORT_API, json=record)
        if response.status_code == 200:
            messagebox.showinfo("Attendance Recorded",
                                f"Attendance marked for {student_name} at {timestamp}.")
        else:
            messagebox.showerror("Server Error", "Failed to record attendance on the server.")
    except Exception as e:
        # If the API call fails, log and notify but still update locally.
        print(f"API call failed: {e}")
        messagebox.showinfo("Attendance Recorded",
                            f"Attendance marked locally for {student_name} at {timestamp}.")

    update_attendance_report()


def update_attendance_report():
    attendance_text.config(state=tk.NORMAL)
    attendance_text.delete("1.0", tk.END)
    if not attendance_records:
        attendance_text.insert(tk.END, "No attendance records available.")
    else:
        for record in attendance_records:
            line = f"{record['time']} - {record['name']} (ID: {record['id']}) via {record['method']}\n"
            attendance_text.insert(tk.END, line)
    attendance_text.config(state=tk.DISABLED)


# -----------------------------------------------------------------------------
# Navigation Functions
# -----------------------------------------------------------------------------
def hide_all_frames():
    for frame in (frame_fingerprint, frame_id_camera, frame_attendance_report):
        frame.pack_forget()


def show_fingerprint_frame():
    hide_all_frames()
    frame_fingerprint.pack(pady=20, fill=tk.BOTH, expand=True)


def show_id_camera_frame():
    hide_all_frames()
    frame_id_camera.pack(pady=20, fill=tk.BOTH, expand=True)


def show_attendance_report_frame():
    hide_all_frames()
    frame_attendance_report.pack(pady=20, fill=tk.BOTH, expand=True)
    update_attendance_report()


# -----------------------------------------------------------------------------
# Main Window Setup
# -----------------------------------------------------------------------------
root = tk.Tk()
root.title("Real-Time Student Attendance System")
root.geometry("1000x600")
root.configure(bg="darkblue")

# -----------------------------------------------------------------------------
# Style Settings
# -----------------------------------------------------------------------------
font_title = ("Helvetica", 18, "bold")
font_header = ("Helvetica", 24, "bold")
font_entry = ("Helvetica", 12)
font_button = ("Helvetica", 12, "bold")
button_bg = "#4CAF50"
button_fg = "white"

# -----------------------------------------------------------------------------
# Main Dashboard Frame
# -----------------------------------------------------------------------------
frame_dashboard = tk.Frame(root, bg="darkblue")
frame_dashboard.pack(fill=tk.BOTH, expand=True)

header_label = tk.Label(frame_dashboard, text="Real-Time Student Attendance System",
                        font=font_header, bg="darkblue", fg="white")
header_label.pack(pady=20)

# -----------------------------------------------------------------------------
# Navigation Bar
# -----------------------------------------------------------------------------
frame_nav = tk.Frame(frame_dashboard, bg="darkblue")
frame_nav.pack(pady=10)

btn_fingerprint = tk.Button(frame_nav, text="Fingerprint Sensor",
                            command=show_fingerprint_frame, font=font_button, bg=button_bg, fg=button_fg)
btn_id_camera = tk.Button(frame_nav, text="Scan ID with Camera",
                          command=show_id_camera_frame, font=font_button, bg=button_bg, fg=button_fg)
btn_attendance_report = tk.Button(frame_nav, text="Attendance Report",
                                  command=show_attendance_report_frame, font=font_button, bg=button_bg, fg=button_fg)
btn_admin_register = tk.Button(frame_nav, text="Admin Registration",
                               command=admin_register_fingerprint, font=font_button, bg=button_bg, fg=button_fg)

btn_fingerprint.pack(side=tk.LEFT, padx=10)
btn_id_camera.pack(side=tk.LEFT, padx=10)
btn_attendance_report.pack(side=tk.LEFT, padx=10)
btn_admin_register.pack(side=tk.LEFT, padx=10)

# -----------------------------------------------------------------------------
# Frame Definitions
# -----------------------------------------------------------------------------

# Fingerprint Sensor Frame
frame_fingerprint = tk.Frame(frame_dashboard, bg="#1E1E1E", bd=2, relief="groove")
label_fingerprint = tk.Label(frame_fingerprint, text="Fingerprint Sensor",
                             font=font_title, bg="#1E1E1E", fg="white")
label_fingerprint.pack(pady=10)
# Display a simulated fingerprint icon.
canvas_fingerprint = tk.Canvas(frame_fingerprint, width=200, height=200, bg="white")
canvas_fingerprint.create_text(100, 100, text="Fingerprint\nSensor", fill="gray", font=("Helvetica", 12))
canvas_fingerprint.pack(pady=10)
btn_scan_fingerprint = tk.Button(frame_fingerprint, text="Scan Fingerprint",
                                 font=font_button, bg=button_bg, fg=button_fg, command=verify_fingerprint)
btn_scan_fingerprint.pack(pady=20)

# ID Camera Scan Frame
frame_id_camera = tk.Frame(frame_dashboard, bg="#1E1E1E", bd=2, relief="groove")
label_id_camera = tk.Label(frame_id_camera, text="ID Card Scanner (Camera)",
                           font=font_title, bg="#1E1E1E", fg="white")
label_id_camera.pack(pady=10)
label_camera_info = tk.Label(frame_id_camera, text="Your laptop camera will activate to scan your ID card.",
                             font=font_entry, bg="#1E1E1E", fg="white")
label_camera_info.pack(pady=5)
btn_scan_id_camera = tk.Button(frame_id_camera, text="Scan ID with Camera",
                               font=font_button, bg=button_bg, fg=button_fg, command=scan_id_with_camera)
btn_scan_id_camera.pack(pady=20)

# Attendance Report Frame
frame_attendance_report = tk.Frame(frame_dashboard, bg="#1E1E1E", bd=2, relief="groove")
label_attendance_report = tk.Label(frame_attendance_report, text="Attendance Report",
                                   font=font_title, bg="#1E1E1E", fg="white")
label_attendance_report.pack(pady=10)
attendance_text = scrolledtext.ScrolledText(frame_attendance_report, wrap=tk.WORD,
                                            font=font_entry, bg="white", fg="black", height=15, state=tk.DISABLED)
attendance_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# -----------------------------------------------------------------------------
# Show Default Frame (Fingerprint Sensor)
# -----------------------------------------------------------------------------
show_fingerprint_frame()

root.mainloop()
