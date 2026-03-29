import customtkinter as CTk
import csv
import os

# Global data storage
data = {
    "components": {},  # {"Component Name": Total Marks}
    "roll_range": (None, None),  # (start_roll, end_roll)
    "dropouts": set(),  # {roll_number}
    "student_marks": {},  # {"Component Name": {roll_no: marks}}
    "subject": "Unknown"  # Default subject, should be set dynamically
}

def student_window():
    def load_student_marks():
        roll_number = roll_entry.get().strip()
        for widget in marks_scroll_frame.winfo_children():
            widget.destroy()
        if not roll_number.isdigit():
            CTk.CTkLabel(marks_scroll_frame, text="Invalid roll number.", font=("Poppins", 14)).pack()
            return

        roll_number = int(roll_number)
        for subject in ["python", "math", "physics", "man"]:
            filename = f"{subject}.csv"
            if not os.path.exists(filename):
                continue

            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                student_data = None
                for row in reader:
                    if row.get("Roll Number") == str(roll_number):
                        student_data = row
                        break

                if student_data:
                    CTk.CTkLabel(marks_scroll_frame, text=f"Subject: {subject.title()}", font=("Poppins bold", 18)).pack(anchor="w", pady=(10, 5))
                    for key, value in student_data.items():
                        if key != "Roll Number":
                            CTk.CTkLabel(marks_scroll_frame, text=f"{key}: {value}", font=("Poppins", 14)).pack(anchor="w")

    def submit_feedback():
        subject = subject_dropdown.get().strip().lower()
        feedback = feedback_entry.get().strip()
        roll_number = roll_entry.get().strip()
        if subject and feedback and roll_number.isdigit():
            with open(f"{subject}_feedback.txt", "a") as f:
                f.write(f"Roll {roll_number}: {feedback}\n")
            feedback_entry.delete(0, 'end')

    student_root = CTk.CTk()
    student_root.title("Student Marks Viewer")
    student_root.geometry("900x600")

    top_frame = CTk.CTkFrame(student_root)
    top_frame.pack(fill="x", padx=10, pady=5)

    CTk.CTkLabel(top_frame, text="Enter Roll Number:", font=("Poppins", 14)).pack(side="left", padx=5)
    roll_entry = CTk.CTkEntry(top_frame, width=120)
    roll_entry.pack(side="left", padx=5)
    CTk.CTkButton(top_frame, text="Load Marks", command=load_student_marks).pack(side="left", padx=5)

    main_frame = CTk.CTkFrame(student_root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)

    left_frame = CTk.CTkFrame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    right_frame = CTk.CTkFrame(main_frame, width=250)
    right_frame.pack(side="right", fill="y", padx=10, pady=10)

    marks_scroll_frame = CTk.CTkScrollableFrame(left_frame)
    marks_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    CTk.CTkLabel(right_frame, text="Announcements", font=("Poppins bold", 18)).pack(pady=(10, 5))
    announcement_box = CTk.CTkScrollableFrame(right_frame, width=250, height=300)
    announcement_box.pack(fill="x", padx=5, pady=5)

    if os.path.exists("announcements.txt"):
        with open("announcements.txt", "r") as f:
            for line in f.readlines():
                CTk.CTkLabel(announcement_box, text=line.strip(), anchor="w", font=("Poppins", 12), wraplength=220, justify="left").pack(anchor="w", padx=5, pady=2)

    CTk.CTkLabel(right_frame, text="Give Feedback", font=("Poppins bold", 18)).pack(pady=(10, 5))

    subject_dropdown = CTk.CTkComboBox(right_frame, values=["python", "math", "physics", "man"], width=220)
    subject_dropdown.pack(pady=5)
    subject_dropdown.set("Select Subject")

    feedback_entry = CTk.CTkEntry(right_frame, placeholder_text="Enter your feedback", width=220)
    feedback_entry.pack(pady=5)

    CTk.CTkButton(right_frame, text="Submit Feedback", command=submit_feedback).pack(pady=5)

    student_root.mainloop()


if __name__ == "__main__":
    student_window()