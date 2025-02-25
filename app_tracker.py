import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime, timedelta
import threading
from usage_monitor import UsageMonitor
from data_manager import DataManager
from notification_system import NotificationSystem
from ui_components import StatsFrame, SettingsFrame, CustomStyle

class AppTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App Usage Tracker")
        self.root.geometry("900x700")  # Increased window size
        self.root.configure(bg=CustomStyle.BG_COLOR)

        # Apply custom styling
        CustomStyle.apply()

        # Initialize components
        self.data_manager = DataManager()
        self.notification_system = NotificationSystem()
        self.usage_monitor = UsageMonitor(self.data_manager, self.notification_system)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Create main frames
        self.stats_frame = StatsFrame(self.notebook, self.data_manager)
        self.settings_frame = SettingsFrame(self.notebook, self.data_manager)

        # Add frames to notebook
        self.notebook.add(self.stats_frame, text="Statistics")
        self.notebook.add(self.settings_frame, text="Settings")

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.usage_monitor.start_monitoring, daemon=True)
        self.monitor_thread.start()

        # Schedule periodic updates
        self.schedule_updates()

    def schedule_updates(self):
        """Schedule periodic UI updates"""
        self.stats_frame.update_stats()
        self.root.after(60000, self.schedule_updates)  # Update every minute

    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Handle application closing"""
        self.usage_monitor.stop_monitoring()
        self.data_manager.save_data()
        self.root.destroy()

if __name__ == "__main__":
    app = AppTracker()
    app.run()