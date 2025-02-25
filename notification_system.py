from tkinter import messagebox
import platform
import os

class NotificationSystem:
    def __init__(self):
        self.system = platform.system()
        
    def show_notification(self, title, message):
        """Show a system notification"""
        if self.system == "Windows":
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)
            except:
                messagebox.showinfo(title, message)
        elif self.system == "Darwin":  # macOS
            os.system(f"""
                osascript -e 'display notification "{message}" with title "{title}"'
            """)
        else:  # Linux
            try:
                os.system(f'notify-send "{title}" "{message}"')
            except:
                messagebox.showinfo(title, message)
