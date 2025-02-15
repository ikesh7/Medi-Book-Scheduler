import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import smtplib
from email.mime.text import MIMEText

class AppointmentScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Medi Book Scheduler")
        self.create_database()
        
        # UI Elements
        self.label_title = tk.Label(root, text="Doctor Appointment Scheduler", font=("Arial", 16))
        self.label_title.pack(pady=10)
        
        self.btn_book = tk.Button(root, text="Book Appointment", command=self.book_appointment)
        self.btn_book.pack(pady=5)
        
        self.btn_view = tk.Button(root, text="View Appointments", command=self.view_appointments)
        self.btn_view.pack(pady=5)
        
        self.btn_search = tk.Button(root, text="Search Appointment", command=self.search_appointment)
        self.btn_search.pack(pady=5)
        
        self.btn_export = tk.Button(root, text="Export to CSV", command=self.export_to_csv)
        self.btn_export.pack(pady=5)
        
        self.btn_email = tk.Button(root, text="Send Email Reminder", command=self.send_email_reminder)
        self.btn_email.pack(pady=5)
        
        self.btn_exit = tk.Button(root, text="Exit", command=root.quit)
        self.btn_exit.pack(pady=5)

    def create_database(self):
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            patient_name TEXT NOT NULL,
                            doctor_name TEXT NOT NULL,
                            appointment_date TEXT NOT NULL,
                            email TEXT,
                            status TEXT DEFAULT 'Scheduled')''')
        conn.commit()
        conn.close()

    def book_appointment(self):
        def save_appointment():
            patient_name = entry_patient.get()
            doctor_name = entry_doctor.get()
            appointment_date = entry_date.get()
            email = entry_email.get()
            
            if not patient_name or not doctor_name or not appointment_date or not email:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            conn = sqlite3.connect("appointments.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO appointments (patient_name, doctor_name, appointment_date, email) VALUES (?, ?, ?, ?)",
                           (patient_name, doctor_name, appointment_date, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Appointment booked successfully!")
            book_window.destroy()
        
        book_window = tk.Toplevel(self.root)
        book_window.title("Book Appointment")
        
        tk.Label(book_window, text="Patient Name:").pack()
        entry_patient = tk.Entry(book_window)
        entry_patient.pack()
        
        tk.Label(book_window, text="Doctor Name:").pack()
        entry_doctor = tk.Entry(book_window)
        entry_doctor.pack()
        
        tk.Label(book_window, text="Appointment Date (YYYY-MM-DD):").pack()
        entry_date = tk.Entry(book_window)
        entry_date.pack()
        
        tk.Label(book_window, text="Email:").pack()
        entry_email = tk.Entry(book_window)
        entry_email.pack()
        
        tk.Button(book_window, text="Save", command=save_appointment).pack(pady=5)

    def view_appointments(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Appointments")
        
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()
        conn.close()
        
        for app in appointments:
            tk.Label(view_window, text=f"ID: {app[0]}, Patient: {app[1]}, Doctor: {app[2]}, Date: {app[3]}, Status: {app[5]}").pack()

    def search_appointment(self):
        def perform_search():
            name = entry_search.get()
            conn = sqlite3.connect("appointments.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments WHERE patient_name LIKE ?", ('%' + name + '%',))
            results = cursor.fetchall()
            conn.close()
            
            for widget in result_frame.winfo_children():
                widget.destroy()
            
            if results:
                for app in results:
                    tk.Label(result_frame, text=f"ID: {app[0]}, Patient: {app[1]}, Doctor: {app[2]}, Date: {app[3]}, Status: {app[5]}").pack()
            else:
                tk.Label(result_frame, text="No matching appointments found.").pack()
        
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Appointment")
        
        tk.Label(search_window, text="Enter Patient Name:").pack()
        entry_search = tk.Entry(search_window)
        entry_search.pack()
        
        tk.Button(search_window, text="Search", command=perform_search).pack()
        
        result_frame = tk.Frame(search_window)
        result_frame.pack()

    def export_to_csv(self):
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()
        conn.close()
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Patient Name", "Doctor Name", "Appointment Date", "Email", "Status"])
            writer.writerows(appointments)
        
        messagebox.showinfo("Success", "Appointments exported successfully!")

    def send_email_reminder(self):
        messagebox.showinfo("Info", "Email reminder functionality is not implemented yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentScheduler(root)
    root.mainloop()
