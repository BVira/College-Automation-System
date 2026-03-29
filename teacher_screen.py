import customtkinter as CTk
import csv

# Global data storage
data = {
    "components": {},  # {"Component Name": Total Marks}
    "roll_range": (None, None),  # (start_roll, end_roll)
    "dropouts": set(),  # {roll_number}
    "student_marks": {},  # {"Component Name": {roll_no: marks}}
    "subject": "Unknown"  # Default subject, should be set dynamically
}

def teacher_window(subject="Unknown"):
    data["subject"] = subject  # Set subject for the session

    main_root = CTk.CTk()
    main_root.configure()
    main_root.title(f"Teacher Window - {subject}")
    main_root.geometry("800x500")

    def enter_roll_numbers():
        roll_window = CTk.CTkToplevel(main_root)
        roll_window.title("Enter Roll Numbers")
        roll_window.geometry("400x350")

        CTk.CTkLabel(roll_window, text="Enter Roll Number Range", font=("Poppins bold", 20)).pack(pady=10)

        start_entry, end_entry, dropout_entry = CTk.CTkEntry(roll_window), CTk.CTkEntry(roll_window), CTk.CTkEntry(roll_window)

        for label, entry in [("Start Roll No:", start_entry), ("End Roll No:", end_entry), ("Dropout Roll No (comma-separated):", dropout_entry)]:
            CTk.CTkLabel(roll_window, text=label, font=("Poppins", 16)).pack()
            entry.pack()

        def save_roll_numbers():
            start, end, dropouts = start_entry.get().strip(), end_entry.get().strip(), dropout_entry.get().strip()
            if start.isdigit() and end.isdigit() and int(start) < int(end):
                data["roll_range"] = (int(start), int(end))
                data["dropouts"] = {int(r) for r in dropouts.split(",") if r.strip().isdigit()}
                roll_window.destroy()
            else:
                CTk.CTkLabel(roll_window, text="Invalid input!", text_color="red").pack()

        CTk.CTkButton(roll_window, text="Save", command=save_roll_numbers).pack(pady=10)

    def add_component():
        comp_window = CTk.CTkToplevel(main_root)
        comp_window.title("Add Component")
        comp_window.geometry("400x300")

        CTk.CTkLabel(comp_window, text="Component Name:").pack()
        comp_entry, marks_entry = CTk.CTkEntry(comp_window), CTk.CTkEntry(comp_window)
        comp_entry.pack()
        CTk.CTkLabel(comp_window, text="Total Marks:").pack()
        marks_entry.pack()

        def save_component():
            title, marks = comp_entry.get().strip(), marks_entry.get().strip()
            if title and marks.isdigit():
                data["components"][title] = int(marks)
                data["student_marks"][title] = {}
                comp_window.destroy()
                update_ui()
            else:
                CTk.CTkLabel(comp_window, text="Invalid input!", text_color="red").pack()

        CTk.CTkButton(comp_window, text="Add", command=save_component).pack(pady=10)

    def enter_marks(component):
        start, end = data["roll_range"]
        if not start:
            print("Roll numbers not set!")
            return

        marks_window = CTk.CTkToplevel(main_root)
        marks_window.title(f"Enter Marks for {component}")
        marks_window.geometry("400x500")

        CTk.CTkLabel(marks_window, text=f"Enter Marks for {component}", font=("Poppins bold", 20)).pack(pady=10)
        scroll_frame = CTk.CTkScrollableFrame(marks_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        entries = {}
        for roll in range(start, end + 1):
            if roll not in data["dropouts"]:
                row = CTk.CTkFrame(scroll_frame)
                row.pack(fill="x", padx=10, pady=5)
                CTk.CTkLabel(row, text=f"Roll {roll}:").pack(side="left")
                entry = CTk.CTkEntry(row, width=100)
                entry.pack(side="right")
                entries[roll] = entry

        def save_marks():
            for roll, entry in entries.items():
                marks = entry.get().strip()
                if marks.isdigit():
                    data["student_marks"].setdefault(component, {})[roll] = int(marks)
            marks_window.destroy()

        CTk.CTkButton(marks_window, text="Save Marks", command=save_marks).pack(pady=10)

    def update_ui():
        for widget in content_section.winfo_children():
            widget.destroy()
        for component in data["components"]:
            frame = CTk.CTkFrame(content_section)
            frame.pack(fill="x", padx=10, pady=5)
            CTk.CTkLabel(frame, text=component, font=("Poppins bold", 18)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            CTk.CTkButton(frame, text="Add Marks", command=lambda c=component: enter_marks(c)).grid(row=0, column=1, padx=10, pady=10, sticky="e")

    def generate_csv():
        start, end = data["roll_range"]
        if not start or not data["components"]:
            print("No data to export!")
            return

        filename = f"{data['subject'].lower()}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            headers = ["Roll Number"] + list(data["components"].keys()) + ["Total Marks"]
            writer.writerow(headers)
            for roll in range(start, end + 1):
                if roll not in data["dropouts"]:
                    marks_list = [data["student_marks"].get(c, {}).get(roll, 0) for c in data["components"]]
                    total_marks = sum(marks_list)
                    row = [roll] + marks_list + [total_marks]
                    writer.writerow(row)
        print(f"CSV Exported Successfully as {filename}!")

    CTk.CTkButton(main_root, text="Enter Roll Numbers", command=enter_roll_numbers).pack(pady=5)
    CTk.CTkButton(main_root, text="Add Component", command=add_component).pack(pady=5)
    CTk.CTkButton(main_root, text="Generate CSV", command=generate_csv).pack(pady=5)

    layout = CTk.CTkFrame(main_root)
    layout.pack(fill="both", expand=True)

    content_section = CTk.CTkFrame(layout, width=500)
    content_section.pack(side="left", fill="both", expand=True)

    announcement_section = CTk.CTkFrame(layout, width=300)
    announcement_section.pack(side="right", fill="y")

    CTk.CTkLabel(announcement_section, text="Announcements", font=("Poppins bold", 18)).pack(pady=10)
    announcement_textbox = CTk.CTkTextbox(announcement_section, height=400, width=280)
    announcement_textbox.pack(padx=10, pady=5)
    announcement_textbox.configure(state="normal")

    try:
        with open("announcements.txt", "r") as f:
            content = f.read()
            announcement_textbox.insert("0.0", content)
    except FileNotFoundError:
        announcement_textbox.insert("0.0", "No announcements found.")

    announcement_textbox.configure(state="disabled")

    update_ui()

    main_root.mainloop()

if __name__ == "__main__":
    from tkinter.simpledialog import askstring
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    subject_input = askstring("Login", "Enter the subject name:")
    if subject_input:
        teacher_window(subject_input)
