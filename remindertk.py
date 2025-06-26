import tkinter as tk
from tkinter import simpledialog, messagebox
import calendar
import datetime
import json
import os

# ----- Reminder file setup -----
FILENAME = "reminders.json"
if not os.path.exists(FILENAME):
    with open(FILENAME, "w") as f:
        json.dump({}, f)

def load_reminders():
    with open(FILENAME, "r") as f:
        return json.load(f)

def save_reminders(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

# ----- Main App -----
class CalendarReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📆 Calendar Reminder App")

        self.today = datetime.date.today()
        self.year = self.today.year
        self.month = self.today.month

        self.reminders = load_reminders()

        self.create_widgets()

    def create_widgets(self):
        # Title
        header = tk.Label(self.root, text=calendar.month_name[self.month] + " " + str(self.year),
                          font=("Segoe UI", 16, "bold"))
        header.pack(pady=10)

        # Calendar frame
        frame = tk.Frame(self.root)
        frame.pack()

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for idx, day in enumerate(days):
            tk.Label(frame, text=day, font=("Segoe UI", 10, "bold")).grid(row=0, column=idx)

        month_days = calendar.monthcalendar(self.year, self.month)
        for r, week in enumerate(month_days, start=1):
            for c, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(frame, text=str(day), width=5, height=2,
                                    command=lambda d=day: self.add_reminder(d))
                    btn.grid(row=r, column=c, padx=2, pady=2)

        # Reminder display
        self.reminder_label = tk.Label(self.root, text="", font=("Segoe UI", 11), fg="blue")
        self.reminder_label.pack(pady=10)

    def add_reminder(self, day):
        date_str = f"{self.year}-{self.month:02d}-{day:02d}"
        reminder = simpledialog.askstring("Add Reminder", f"Enter reminder for {date_str}:")
        if reminder:
            if date_str not in self.reminders:
                self.reminders[date_str] = []
            self.reminders[date_str].append(reminder)
            save_reminders(self.reminders)
            self.reminder_label.config(text=f"📌 Reminders for {date_str}: " + " | ".join(self.reminders[date_str]))
        else:
            self.reminder_label.config(text=f"No reminder added for {date_str}.")

# Run the app
root = tk.Tk()
app = CalendarReminderApp(root)
root.mainloop()
