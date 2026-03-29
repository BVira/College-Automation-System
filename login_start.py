import customtkinter as CTk
import subprocess
import sys
import csv
import os

def login():
    CTk.set_appearance_mode("dark")
    root = CTk.CTk()
    root.geometry("500x600")
    root.title("Login Window")

    details = {"admin": "1234", "student": "3456", "teacher": "4567"}

    txt_color = "#F7F7F7"
    primary_color = "#274472"

    def load_credentials(role):
        credentials = {}
        filename = f"{role}.csv"
        if os.path.exists(filename):
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    credentials[row["id"]] = row["password"]
        return credentials

    def ask_id_password(role):
        for widget in frame.winfo_children():
            widget.destroy()

        CTk.CTkLabel(frame, text=f"{role.capitalize()} Login", font=("Poppins", 25, "bold"), text_color=txt_color).pack(pady=10)

        id_label = CTk.CTkLabel(frame, text="ID:", text_color=txt_color, font=("Poppins", 15))
        id_label.pack()
        id_entry = CTk.CTkEntry(frame)
        id_entry.pack(pady=5)

        password_label = CTk.CTkLabel(frame, text="Password:", text_color=txt_color, font=("Poppins", 15))
        password_label.pack()
        pw_entry = CTk.CTkEntry(frame, show="*")
        pw_entry.pack(pady=5)

        status = CTk.CTkLabel(frame, text="", text_color="red", font=("Poppins", 13))
        status.pack(pady=5)

        def verify_id_password():
            credentials = load_credentials(role)
            user_id = id_entry.get()
            pw = pw_entry.get()
            if user_id in credentials and credentials[user_id] == pw:
                status.configure(text="Login successful!", text_color="green")

                def proceed():
                    root.destroy()
                    if role == "admin":
                        subprocess.Popen([sys.executable, "admin_page.py"])
                    elif role == "teacher":
                        subprocess.Popen([sys.executable, "teacher_screen.py"])
                    elif role == "student":
                        subprocess.Popen([sys.executable, "student_screen.py"])

                root.after(2000, proceed)  # Wait for 2 seconds then proceed
            else:
                status.configure(text="Invalid ID or Password", text_color="red")


        CTk.CTkButton(frame, text="Submit", fg_color=primary_color, text_color="white", font=("Poppins", 15), command=verify_id_password).pack(pady=10)

    def validate_role_password():
        role = username_entry.get().lower()
        password = password_entry.get()
        if role in details:
            if details[role] == password:
                ask_id_password(role)
            else:
                status_label.configure(text="Incorrect role password!", text_color="red")
        else:
            status_label.configure(text="Invalid role!", text_color="red")

    frame = CTk.CTkFrame(root, width=300, height=400)
    frame.pack(padx=20, pady=20)

    CTk.CTkLabel(frame, text="Select Role", font=("Poppins", 30, "bold"), text_color=txt_color).pack(pady=10)

    CTk.CTkLabel(frame, text="Role (admin/teacher/student):", text_color=txt_color, font=("Poppins", 15)).pack()
    username_entry = CTk.CTkEntry(frame)
    username_entry.pack(pady=5)

    CTk.CTkLabel(frame, text="Password:", text_color=txt_color, font=("Poppins", 15)).pack()
    password_entry = CTk.CTkEntry(frame, show="*")
    password_entry.pack(pady=5)

    CTk.CTkButton(frame, text="Continue", fg_color=primary_color, text_color="white", font=("Poppins", 15), command=validate_role_password).pack(pady=10)

    status_label = CTk.CTkLabel(frame, text="", text_color=txt_color, font=("Poppins", 13))
    status_label.pack(pady=5)

    root.mainloop()

login()