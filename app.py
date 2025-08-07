import tkinter as tk
from tkinter import messagebox, ttk
from database import create_tables, register_user, login_user, add_event, get_events

create_tables()

class EventApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Management System")
        self.root.geometry("700x500")
        self.login_screen()

    def login_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=10)

        self.username = tk.Entry(self.root)
        self.username.pack(pady=5)
        self.username.insert(0, "Username")

        self.password = tk.Entry(self.root, show="*")
        self.password.pack(pady=5)
        self.password.insert(0, "Password")

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.signup_screen).pack()

    def signup_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Sign Up", font=("Arial", 20)).pack(pady=10)

        self.new_username = tk.Entry(self.root)
        self.new_username.pack(pady=5)
        self.new_username.insert(0, "Username")

        self.new_password = tk.Entry(self.root, show="*")
        self.new_password.pack(pady=5)
        self.new_password.insert(0, "Password")

        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def dashboard(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to Event Dashboard", font=("Arial", 18)).pack(pady=10)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_entry.insert(0, "Search event...")
        tk.Button(self.root, text="Search", command=self.load_events).pack(pady=5)

        self.event_list = tk.Listbox(self.root, width=80)
        self.event_list.pack(pady=10)

        tk.Button(self.root, text="Add Event", command=self.add_event_screen).pack(pady=5)
        self.load_events()

    def add_event_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Add New Event", font=("Arial", 18)).pack(pady=10)

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack(pady=5)
        self.title_entry.insert(0, "Title")

        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.pack(pady=5)
        self.desc_entry.insert(0, "Description")

        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack(pady=5)
        self.date_entry.insert(0, "Date (YYYY-MM-DD)")

        self.location_entry = tk.Entry(self.root)
        self.location_entry.pack(pady=5)
        self.location_entry.insert(0, "Location")

        tk.Button(self.root, text="Save", command=self.save_event).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.dashboard).pack()

    def load_events(self):
        self.event_list.delete(0, tk.END)
        filter_text = self.search_entry.get()
        events = get_events(filter_text)
        for e in events:
            self.event_list.insert(tk.END, f"{e[1]} - {e[3]} @ {e[4]}")

    def save_event(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        date = self.date_entry.get()
        loc = self.location_entry.get()
        add_event(title, desc, date, loc)
        messagebox.showinfo("Success", "Event added successfully")
        self.dashboard()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if login_user(user, pwd):
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        user = self.new_username.get()
        pwd = self.new_password.get()
        if register_user(user, pwd):
            messagebox.showinfo("Success", "Registered successfully. Please log in.")
            self.login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EventApp(root)
    root.mainloop()
