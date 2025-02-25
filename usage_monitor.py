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
                    cmdline = proc.info.get('cmdline', [])

                    # Check for browser processes with specific URLs
                    if cmdline:
                        for arg in cmdline:
                            if isinstance(arg, str):
                                if 'youtube.com' in arg.lower():
                                    return 'youtube', 'YouTube'
                                if 'netflix.com' in arg.lower():
                                    return 'netflix', 'Netflix'

                    # Check for browser processes
                    for app_name in ['chrome', 'firefox', 'msedge']:
                        if app_name in process_name:
                            return app_name, self.tracked_apps[app_name]

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None, None
        except Exception as e:
            print(f"Error in get_active_window_process: {e}")
            return None, None

    def start_monitoring(self):
        """Start monitoring app usage"""
        self.running = True
        while self.running:
            process_name, app_name = self.get_active_window_process()

            if process_name and app_name:
                current_time = datetime.now()

                # Update usage time
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