import json
from datetime import datetime, timedelta
import os

class DataManager:
    def __init__(self):
        self.data_file = "usage_data.json"
        self.load_data()
        
    def load_data(self):
        """Load usage data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.initialize_data()
        else:
            self.initialize_data()
            
    def initialize_data(self):
        """Initialize empty data structure"""
        self.data = {
            "usage": {},
            "limits": {},
            "settings": {
                "notification_enabled": True
            }
        }
        
    def save_data(self):
        """Save usage data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f)
            
    def update_app_usage(self, app_name, seconds):
        """Update usage time for an app"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if app_name not in self.data["usage"]:
            self.data["usage"][app_name] = {}
            
        if today not in self.data["usage"][app_name]:
            self.data["usage"][app_name][today] = 0
            
        self.data["usage"][app_name][today] += seconds
        
    def get_today_usage(self, app_name):
        """Get today's usage for an app"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.data["usage"].get(app_name, {}).get(today, 0)
        
    def get_weekly_usage(self, app_name):
        """Get weekly usage for an app"""
        usage = {}
        today = datetime.now()
        
        for i in range(7):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            usage[date] = self.data["usage"].get(app_name, {}).get(date, 0)
            
        return usage
        
    def set_app_limit(self, app_name, limit_minutes):
        """Set daily time limit for an app"""
        self.data["limits"][app_name] = limit_minutes
        self.save_data()
        
    def get_app_limit(self, app_name):
        """Get daily time limit for an app"""
        return self.data["limits"].get(app_name, 0)
