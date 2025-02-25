import time
import psutil
from datetime import datetime
import win32gui
import win32process

class UsageMonitor:
    def __init__(self, data_manager, notification_system):
        self.data_manager = data_manager
        self.notification_system = notification_system
        self.running = False
        self.tracked_apps = {
            "chrome.exe": "Google Chrome",
            "firefox.exe": "Firefox",
            "msedge.exe": "Microsoft Edge",
            "netflix.exe": "Netflix",
            "youtube.com": "YouTube"
        }
        
    def get_active_window_process(self):
        """Get the currently active window process name"""
        try:
            window = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            return process.name(), win32gui.GetWindowText(window)
        except:
            return None, None
            
    def start_monitoring(self):
        """Start monitoring app usage"""
        self.running = True
        while self.running:
            process_name, window_title = self.get_active_window_process()
            
            if process_name:
                current_time = datetime.now()
                
                # Check for tracked apps
                for app_process, app_name in self.tracked_apps.items():
                    if app_process.lower() in process_name.lower() or app_process.lower() in window_title.lower():
                        self.data_manager.update_app_usage(app_name, 1)  # Add 1 second
                        
                        # Check limits and notify if exceeded
                        daily_limit = self.data_manager.get_app_limit(app_name)
                        if daily_limit:
                            current_usage = self.data_manager.get_today_usage(app_name)
                            if current_usage >= daily_limit * 60:  # Convert minutes to seconds
                                self.notification_system.show_notification(
                                    f"{app_name} Usage Limit",
                                    f"You have exceeded your daily limit for {app_name}"
                                )
                
            time.sleep(1)  # Check every second
            
    def stop_monitoring(self):
        """Stop monitoring app usage"""
        self.running = False
