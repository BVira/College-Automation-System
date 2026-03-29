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

def admin_window():
    admin_root = CTk.CTk()
    admin_root.title("Admin Panel")
    admin_root.geometry("1000x600")

    left_frame = CTk.CTkFrame(admin_root)
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    CTk.CTkLabel(left_frame, text="Admin Functions", font=("Poppins bold", 20)).pack(pady=10)

    CTk.CTkLabel(left_frame, text="Select Subject to View CSV:", font=("Poppins", 16)).pack(pady=5)
    subject_list = [f.split("_")[0] for f in os.listdir() if f.endswith("_file.csv")]
    subject_var = CTk.StringVar(value=subject_list[0] if subject_list else "")
    subject_dropdown = CTk.CTkOptionMenu(left_frame, values=subject_list, variable=subject_var)
    subject_dropdown.pack(pady=5)

    display_frame = CTk.CTkFrame(left_frame)
    display_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def show_subject_csv():
        for widget in display_frame.winfo_children():
            widget.destroy()
        filename = f"{subject_var.get()}_file.csv"
        if os.path.exists(filename):
            with open(filename, newline='') as f:
                reader = list(csv.reader(f))
                if not reader:
                    return

                canvas = CTk.CTkCanvas(display_frame)
                canvas.pack(side="left", fill="both", expand=True)

                x_scroll = CTk.CTkScrollbar(display_frame, orientation="horizontal", command=canvas.xview)
                y_scroll = CTk.CTkScrollbar(display_frame, orientation="vertical", command=canvas.yview)
                canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

                x_scroll.pack(side="bottom", fill="x")
                y_scroll.pack(side="right", fill="y")

                inner_frame = CTk.CTkFrame(canvas)
                canvas.create_window((0, 0), window=inner_frame, anchor='nw')

                for r, row in enumerate(reader):
                    for c, val in enumerate(row):
                        CTk.CTkLabel(inner_frame, text=val, width=15).grid(row=r, column=c, padx=2, pady=2)

                inner_frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))

    CTk.CTkButton(left_frame, text="Continue", command=show_subject_csv).pack(pady=10)

    right_frame = CTk.CTkFrame(admin_root)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    CTk.CTkLabel(right_frame, text="Send Announcement", font=("Poppins bold", 18)).pack(pady=(10, 5))
    announcement_entry = CTk.CTkTextbox(right_frame, height=150, width=300)
    announcement_entry.pack(pady=5)

    def send_announcement():
        announcement = announcement_entry.get("1.0", "end").strip()
        if announcement:
            with open("announcements.txt", "a") as file:
                file.write(announcement + "\n")
            announcement_entry.delete("1.0", "end")

    CTk.CTkButton(right_frame, text="Send", command=send_announcement).pack(pady=10)

    admin_root.mainloop()

if __name__ == "__main__":
    admin_window()
