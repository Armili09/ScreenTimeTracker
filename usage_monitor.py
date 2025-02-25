import time
import psutil
from datetime import datetime

class UsageMonitor:
    def __init__(self, data_manager, notification_system):
        self.data_manager = data_manager
        self.notification_system = notification_system
        self.running = False
        self.tracked_apps = {
            "chrome": "Google Chrome",
            "firefox": "Firefox",
            "msedge": "Microsoft Edge",
            "netflix": "Netflix",
            "youtube": "YouTube"
        }

    def get_active_window_process(self):
        """Get the currently active window process name"""
        try:
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    process_name = proc.info['name'].lower()
                    cmdline = proc.info['cmdline']

                    # Check for browser processes
                    if cmdline and any('youtube.com' in arg.lower() for arg in cmdline):
                        return 'youtube.com', 'YouTube'
                    if cmdline and any('netflix.com' in arg.lower() for arg in cmdline):
                        return 'netflix.com', 'Netflix'

                    # Return process name for other tracked apps
                    return process_name, process_name
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
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
                    if app_process in str(process_name).lower():
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