from tkinter import messagebox
import platform
import os

class NotificationSystem:
    def __init__(self):
        self.system = platform.system()

    def show_notification(self, title, message):
        """Show a system notification"""
        # Use tkinter messagebox for all platforms in Replit environment
        messagebox.showinfo(title, message)